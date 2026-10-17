"""File-backed CLI evaluations; only a short bootstrap is passed as argv."""
import base64
from contextlib import contextmanager
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
import uuid

class BridgeError(RuntimeError):
    def __init__(self, message, code="BRIDGE_ERROR", outcome="unknown", request_id=None, details=None):
        super().__init__(message)
        self.code, self.outcome, self.request_id = code, outcome, request_id
        self.details = details or {}

    def as_dict(self):
        result = {"code": self.code, "message": str(self), "outcome": self.outcome}
        if self.request_id:
            result["requestId"] = self.request_id
        if self.details:
            result["details"] = self.details
        return result

class _CliLaunchError(OSError):
    """The child process was never created; delivery cannot be pending."""


def _capture_reader_opener(path, flags):
    # Windows O_TEMPORARY shares delete access with NamedTemporaryFile's writer.
    return os.open(path, flags | getattr(os, "O_TEMPORARY", 0))


@contextmanager
def _capture_output():
    # Reopen by name: dup() would share the inherited writer's file position.
    with tempfile.NamedTemporaryFile() as writer:
        with open(writer.name, "rb", opener=_capture_reader_opener) as reader:
            yield writer, reader


DEFAULT_CLI = Path("/Applications/Obsidian.app/Contents/MacOS/obsidian-cli")

def find_cli(explicit=None):
    override = explicit or os.environ.get("OBSIDIAN_CLI")
    if override:
        resolved = Path(shutil.which(override) or override).resolve()
        if resolved.is_file():
            return str(resolved)
        raise BridgeError("Specified Obsidian CLI not found: " + str(override))

    for candidate in (shutil.which("obsidian"), shutil.which("obsidian-cli"), DEFAULT_CLI):
        if not candidate:
            continue
        resolved = Path(candidate).resolve()
        # Older PATH registrations point at the GUI executable. Use the CLI
        # from that same app bundle rather than launching another GUI process.
        if resolved.name.lower() == "obsidian" and resolved.parent.name == "MacOS":
            resolved = resolved.with_name("obsidian-cli")
        if resolved.is_file():
            return str(resolved)
    raise BridgeError("Obsidian CLI not found. Update the Obsidian installer and enable its CLI, or pass --obsidian.")

class Client:
    def __init__(self, vault, executable=None, timeout=30):
        self.vault = vault
        self.executable = find_cli(executable)
        self.timeout = timeout
        self.module = str(Path(__file__).resolve().parent / "runtime" / "bridge.cjs")
        self._evaluation_files = set()

    def _evaluation_details(self):
        # Only report files still present, including previous unacknowledged polls.
        for path in tuple(self._evaluation_files):
            try:
                path.stat()
            except FileNotFoundError:
                self._evaluation_files.discard(path)
            except OSError:
                pass  # Inaccessible files still require inspection.
        return {"evaluationFiles": sorted(str(path) for path in self._evaluation_files)} if self._evaluation_files else {}

    def _discard_evaluation(self, path):
        try:
            path.unlink()
        except OSError:
            pass  # Cleanup must not hide an evaluation result or its original error.

    def _run_cli(self, argv, timeout):
        process = None
        try:
            # Regular files avoid pipe EOF waits; independent readers never move
            # the positions of writers inherited by descendants.
            with _capture_output() as (stdout, stdout_reader), _capture_output() as (stderr, stderr_reader):
                process = subprocess.Popen(argv, stdout=stdout, stderr=stderr)
                with process:
                    try:
                        process.wait(timeout=timeout)
                    except BaseException:
                        process.kill()
                        process.wait()
                        raise
                # Snapshot the direct child's completed output. Do not follow
                # later writes from descendants or wait for their handles to close.
                stdout_size = os.fstat(stdout.fileno()).st_size
                stderr_size = os.fstat(stderr.fileno()).st_size
                return subprocess.CompletedProcess(argv, process.returncode,
                                                   stdout_reader.read(stdout_size), stderr_reader.read(stderr_size))
        except OSError as exc:
            if process is None:
                raise _CliLaunchError(str(exc)) from exc
            raise

    def evaluate(self, code, missing_ok=False):
        payload = None
        delivery = "prepared"
        try:
            # Close the file before Obsidian reads it (also required on Windows).
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n",
                                             prefix="obsidian-tldraw-eval-", suffix=".js", delete=False) as source:
                payload = Path(source.name)
                self._evaluation_files.add(payload)
                source.write(code)
            encoded_path = base64.b64encode(str(payload).encode("utf-8")).decode("ascii")
            # Keep argv short and independent of quoting in the evaluation source.
            bootstrap = ("(()=>{const fs=require('node:fs');const p=Buffer.from('" + encoded_path +
                         "','base64').toString('utf8');const code=fs.readFileSync(p,'utf8');"
                         "try{fs.unlinkSync(p)}catch{};return eval(code)})()")
            delivery = "unacknowledged"
            proc = self._run_cli([self.executable, "vault=" + self.vault, "eval", "code=" + bootstrap],
                                 timeout=self.timeout)
            # Decode explicitly so response encoding never depends on the locale.
            stdout = proc.stdout.decode("utf-8")
            stderr = proc.stderr.decode("utf-8")
            values = [line[3:] for line in stdout.splitlines() if line.startswith("=> ")]
            if values:
                delivery = "acknowledged"
        except _CliLaunchError as exc:
            delivery = "prepared"
            self._discard_evaluation(payload)
            raise BridgeError("Could not start Obsidian CLI: " + str(exc),
                              details=self._evaluation_details()) from exc
        except subprocess.TimeoutExpired as exc:
            raise BridgeError("Obsidian CLI timed out; the request may still be running. Do not blindly repeat mutations.",
                              details=self._evaluation_details()) from exc
        except UnicodeError as exc:
            if payload is not None and delivery == "prepared":
                self._discard_evaluation(payload)
            raise BridgeError("Obsidian CLI transport requires valid UTF-8",
                              details=self._evaluation_details()) from exc
        except OSError as exc:
            if payload is not None and delivery == "prepared":
                self._discard_evaluation(payload)
            raise BridgeError("Could not invoke Obsidian CLI: " + str(exc),
                              details=self._evaluation_details()) from exc
        finally:
            # Preserve unread files only if a receiver could still consume them.
            if payload is not None and delivery != "unacknowledged":
                self._discard_evaluation(payload)
            self._evaluation_details()
        if proc.returncode or (not values and not missing_ok):
            raise BridgeError("CLI evaluation failed: " + (stdout + stderr).strip(),
                              details=self._evaluation_details())
        if not values:
            return None
        try:
            return json.loads(values[-1])
        except json.JSONDecodeError as exc:
            raise BridgeError("Unexpected CLI response: " + values[-1],
                              details=self._evaluation_details()) from exc

    def _runtime(self):
        loader = str(Path(__file__).resolve().parent / "runtime" / "loader.cjs")
        return f"require({json.dumps(loader)})", json.dumps(self.module)

    def _runtime_evaluate(self, expression, request_id=None, missing_ok=False):
        # Preserve admission/status errors as data instead of parsing CLI error text.
        wrapped = ("(()=>{try{return " + expression + ";}catch(e){return JSON.stringify({_bridgeError:{"
                   "code:e?.code||'RUNTIME_ERROR',message:e?.message||String(e),"
                   "outcome:e?.outcome||'unknown'}})}})()")
        try:
            result = self.evaluate(wrapped, missing_ok)
        except BridgeError as exc:
            if exc.code != "BRIDGE_ERROR":
                raise
            raise BridgeError(str(exc), code="RESULT_UNKNOWN", request_id=request_id, details={**exc.details, **self._evaluation_details()}) from exc
        if isinstance(result, dict) and "_bridgeError" in result:
            error = result["_bridgeError"]
            raise BridgeError(error["message"], code=error["code"], outcome=error["outcome"], request_id=request_id, details={**(error.get("details") or {}), **self._evaluation_details()})
        return result

    def status(self, request_id):
        loader, module = self._runtime()
        job = self._runtime_evaluate(f"{loader}.poll(app,{module},{json.dumps(request_id)})", request_id)
        return {key: value for key, value in job.items() if key != "request"}

    def forget(self, request_id):
        loader, module = self._runtime()
        return self._runtime_evaluate(f"{loader}.forget(app,{module},{json.dumps(request_id)})", request_id)

    def _release_automatic(self, job_id, request_id):
        if request_id is None:
            try:
                self.forget(job_id)
            except BridgeError:
                # A cleanup failure must not hide a committed edit or its result.
                # The runtime admission limit still bounds retained receipts.
                pass

    def call(self, action, args=None, request_id=None):
        job_id = request_id or "bridge-" + uuid.uuid4().hex
        loader, module = self._runtime()
        identity = json.dumps(job_id)
        self._runtime_evaluate(f"{loader}.dispatch(app,{module},{json.dumps(action)},{json.dumps(args or {})},{identity})", job_id, True)
        deadline = time.monotonic() + self.timeout
        while time.monotonic() < deadline:
            job = self._runtime_evaluate(f"{loader}.poll(app,{module},{identity})", job_id, True)
            if job and job.get("status") == "failed":
                failure = job.get("failure", {})
                if failure.get("outcome", "unknown") == "not_applied":
                    self._release_automatic(job_id, request_id)
                raise BridgeError(job["error"] + " (request " + job_id + ")",
                                  code=failure.get("code", "BRIDGE_ERROR"),
                                  outcome=failure.get("outcome", "unknown"), request_id=job_id,
                                  details={**(failure.get("details") or {}), **self._evaluation_details()})
            if job and job.get("status") == "complete":
                self._release_automatic(job_id, request_id)
                return job["result"]
            time.sleep(0.1)
        raise BridgeError("Request timed out; use status or resume with the same --request-id: " + job_id, code="RESULT_UNKNOWN", request_id=job_id, details=self._evaluation_details())
