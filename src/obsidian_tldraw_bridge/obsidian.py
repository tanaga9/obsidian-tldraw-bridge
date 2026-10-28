"""File-backed CLI evaluations; only a short bootstrap is passed as argv."""
import base64
from contextlib import contextmanager
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
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


def _evaluation_response(stdout, token, *, final=False):
    """Decode only a complete response from this invocation, ignoring log lines."""
    lines = stdout.split(b"\n")
    if not final:
        lines = lines[:-1]
    for line in reversed(lines):
        if not line.startswith(b"=> "):
            continue
        try:
            envelope = json.loads(line[3:].decode("utf-8"))
        except (UnicodeError, ValueError):
            continue
        if not isinstance(envelope, dict) or envelope.get("bridgeResponseToken") != token:
            continue
        if "value" not in envelope:
            # JavaScript undefined has no JSON value; missing_ok retains its
            # normal meaning without mistaking console output for a response.
            return b""
        value = envelope["value"]
        text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
        return b"=> " + text.encode("utf-8") + b"\n"
    return None


DEFAULT_CLI = Path("/Applications/Obsidian.app/Contents/MacOS/obsidian-cli")

def validate_connection(vault, timeout):
    if (not isinstance(vault, str) or not vault.strip() or
            any(c in vault for c in ('/', '\\')) or any(ord(c) < 32 for c in vault) or
            (len(vault) >= 2 and vault[0].isalpha() and vault[1] == ':') or vault in ('.', '..')):
        raise BridgeError("Use an Obsidian vault name or id, not a filesystem path",
                          code="INVALID_INPUT", outcome="not_applied", details={"stage": "vault"})
    validate_timeout(timeout)


def validate_timeout(timeout):
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or not math.isfinite(timeout) or timeout <= 0:
        raise BridgeError("Timeout must be positive and finite", code="INVALID_INPUT", outcome="not_applied")


def _cli_candidates():
    # PATH registrations take precedence over standard installation locations.
    commands = ("Obsidian.com", "obsidian", "obsidian-cli") if sys.platform == "win32" else ("obsidian", "obsidian-cli")
    for command in commands:
        candidate = shutil.which(command)
        if candidate:
            yield Path(candidate)
    if sys.platform == "win32":
        for variable, suffix in (("LOCALAPPDATA", "Programs/Obsidian/Obsidian.com"),
                                 ("ProgramFiles", "Obsidian/Obsidian.com"),
                                 ("ProgramFiles(x86)", "Obsidian/Obsidian.com")):
            directory = os.environ.get(variable)
            if directory:
                yield Path(directory) / suffix
    else:
        yield DEFAULT_CLI


def find_cli(explicit=None):
    override = explicit or os.environ.get("OBSIDIAN_CLI")
    if override:
        resolved = Path(shutil.which(override) or override).resolve()
        if sys.platform == "win32" and resolved.name.lower() == "obsidian.exe":
            raise BridgeError("Select the official Windows CLI Obsidian.com, not Obsidian.exe",
                              code="CLI_EXECUTABLE_REQUIRED", outcome="not_applied", details={"stage": "cli"})
        if resolved.is_file():
            return str(resolved)
        raise BridgeError("Specified Obsidian CLI not found: " + str(override),
                          code="CLI_NOT_FOUND", outcome="not_applied", details={"stage": "cli"})

    for candidate in _cli_candidates():
        resolved = candidate.resolve()
        # Older registrations point at a GUI. Select the CLI in the same install.
        if resolved.name.lower() == "obsidian" and resolved.parent.name == "MacOS":
            resolved = resolved.with_name("obsidian-cli")
        elif resolved.name.lower() == "obsidian.exe":
            resolved = resolved.with_suffix(".com")
        if resolved.is_file():
            return str(resolved)
    raise BridgeError("Obsidian CLI not found. Update the Obsidian installer and enable its CLI, or pass --obsidian.",
                      code="CLI_NOT_FOUND", outcome="not_applied", details={"stage": "cli"})

class Client:
    def __init__(self, vault, executable=None, timeout=30):
        validate_connection(vault, timeout)
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

    @staticmethod
    def _run_cli(argv, timeout, *, response_token=None):
        process = None
        try:
            # Independent readers never move the positions of writers inherited
            # by descendants. A tagged eval reply, rather than CLI exit, confirms
            # delivery; Obsidian may reply and then leave its CLI process alive.
            with _capture_output() as (stdout, stdout_reader), _capture_output() as (stderr, stderr_reader):
                process = subprocess.Popen(argv, stdout=stdout, stderr=stderr)
                response = None
                response_reaped = False
                with process:
                    try:
                        if response_token is None:
                            process.wait(timeout=timeout)
                        else:
                            deadline = time.monotonic() + timeout
                            last_size = -1
                            while True:
                                size = os.fstat(stdout.fileno()).st_size
                                if size != last_size:
                                    stdout_reader.seek(0)
                                    response = _evaluation_response(stdout_reader.read(size), response_token)
                                    last_size = size
                                if response is not None:
                                    # Preserve normal CLI exit failures when it
                                    # exits promptly, and reap only this child if
                                    # a confirmed reply outlives its exit grace.
                                    try:
                                        process.wait(timeout=min(.05, max(0, deadline - time.monotonic())))
                                    except subprocess.TimeoutExpired:
                                        process.kill()
                                        process.wait()
                                        response_reaped = True
                                    break
                                if process.poll() is not None:
                                    break
                                remaining = deadline - time.monotonic()
                                if remaining <= 0:
                                    raise subprocess.TimeoutExpired(argv, timeout)
                                time.sleep(min(.01, remaining))
                    except BaseException:
                        process.kill()
                        process.wait()
                        raise
                stdout_reader.seek(0)
                raw_stdout = stdout_reader.read(os.fstat(stdout.fileno()).st_size)
                raw_stderr = stderr_reader.read(os.fstat(stderr.fileno()).st_size)
                if response_token is not None:
                    response = _evaluation_response(raw_stdout, response_token, final=True)
                    # Unmatched frames are logs, never an evaluation response.
                    raw_stdout = response if response is not None else b"\n".join(
                        line for line in raw_stdout.split(b"\n") if not line.startswith(b"=> "))
                result = subprocess.CompletedProcess(argv, process.returncode, raw_stdout, raw_stderr)
                result.response_received = response_token is not None and response is not None
                result.response_reaped = response_reaped
                return result
        except OSError as exc:
            if process is None:
                raise _CliLaunchError(str(exc)) from exc
            raise

    def evaluate(self, code, missing_ok=False, *, timeout=None):
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
            response_token = uuid.uuid4().hex
            bootstrap = ("(()=>{const fs=require('node:fs');const p=Buffer.from('" + encoded_path +
                         "','base64').toString('utf8');const code=fs.readFileSync(p,'utf8');"
                         "try{fs.unlinkSync(p)}catch{};return JSON.stringify({bridgeResponseToken:" +
                         json.dumps(response_token) + ",value:eval(code)})})()")
            delivery = "unacknowledged"
            proc = self._run_cli([self.executable, "vault=" + self.vault, "eval", "code=" + bootstrap],
                                 timeout=self.timeout if timeout is None else timeout, response_token=response_token)
            # Decode explicitly so response encoding never depends on the locale.
            stdout = proc.stdout.decode("utf-8")
            stderr = proc.stderr.decode("utf-8")
            # Split LF/CRLF output without treating Unicode characters inside
            # JSON strings (NEL, line separator, paragraph separator) as framing.
            values = [line[3:] for line in stdout.split("\n") if line.startswith("=> ")]
            if values or getattr(proc, "response_received", False):
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
        if not values and "Command line interface is not enabled" in stdout + stderr:
            raise BridgeError("Enable the official Obsidian CLI in Settings > General > Advanced.",
                              code="CLI_DISABLED", details={"stage": "connection", **self._evaluation_details()})
        if (proc.returncode and not getattr(proc, "response_reaped", False)) or (not values and not missing_ok):
            diagnostic = (stdout + stderr).strip() or "No evaluation response; check that Obsidian is running, the vault name/id is correct, and local CLI communication is permitted."
            raise BridgeError("CLI evaluation failed: " + diagnostic,
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

    def _runtime_evaluate(self, expression, request_id=None, missing_ok=False, *, deadline=None):
        # Preserve admission/status errors as data instead of parsing CLI error text.
        guard = ("if(![app.vault.getName(),app.appId].includes(" + json.dumps(self.vault) + "))"
                 "throw Object.assign(new Error('Connected vault does not match --vault'),"
                 "{code:'VAULT_MISMATCH',outcome:'unknown'});")
        wrapped = ("(()=>{try{" + guard + "return " + expression + ";}catch(e){return JSON.stringify({_bridgeError:{"
                   "code:e?.code||'RUNTIME_ERROR',message:e?.message||String(e),"
                   "outcome:e?.outcome||'unknown'}})}})()")
        try:
            if deadline is None:
                result = self.evaluate(wrapped, missing_ok)
            else:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise BridgeError("Request timeout budget exhausted")
                result = self.evaluate(wrapped, missing_ok, timeout=remaining)
        except BridgeError as exc:
            if exc.code != "BRIDGE_ERROR":
                raise BridgeError(str(exc), code=exc.code, outcome=exc.outcome,
                                  request_id=request_id, details=exc.details) from exc
            raise BridgeError(str(exc), code="RESULT_UNKNOWN", request_id=request_id, details={**exc.details, **self._evaluation_details()}) from exc
        if isinstance(result, dict) and "_bridgeError" in result:
            error = result["_bridgeError"]
            raise BridgeError(error["message"], code=error["code"], outcome=error["outcome"], request_id=request_id, details={**(error.get("details") or {}), **self._evaluation_details()})
        return result

    def status(self, request_id):
        loader, module = self._runtime()
        job = self._runtime_evaluate(f"{loader}.poll(app,{module},{json.dumps(request_id)})", request_id)
        return {key: value for key, value in job.items() if key != "request"}

    def forget(self, request_id, *, deadline=None):
        loader, module = self._runtime()
        return self._runtime_evaluate(f"{loader}.forget(app,{module},{json.dumps(request_id)})", request_id, deadline=deadline)

    def _release_automatic(self, job_id, request_id, deadline):
        if request_id is None:
            try:
                self.forget(job_id, deadline=deadline)
            except BridgeError:
                # A cleanup failure must not hide a committed edit or its result.
                # The runtime admission limit still bounds retained receipts.
                pass

    def _diagnose_connection(self, deadline):
        checks = [{"stage": "cli", "ok": True, "executable": self.executable}]
        try:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise BridgeError("Connection diagnostic timeout budget exhausted")
            connected = self.evaluate("JSON.stringify({vault:app.vault.getName(),id:app.appId,"
                                      "pluginVersion:app.plugins.getPlugin('tldraw')?.manifest.version??null,"
                                      "installed:!!app.plugins.manifests?.tldraw})", timeout=remaining)
        except BridgeError as exc:
            raise BridgeError(str(exc), code=exc.code if exc.code != "BRIDGE_ERROR" else "CLI_CONNECTION_FAILED",
                              details={**exc.details, "stage": "connection", "checks": checks}) from exc
        if not isinstance(connected, dict) or not isinstance(connected.get("vault"), str):
            raise BridgeError("Unexpected connection diagnostic response", code="CLI_CONNECTION_FAILED",
                              details={"stage": "connection", "checks": checks})
        checks.append({"stage": "connection", "ok": True})
        if self.vault not in (connected["vault"], connected.get("id")):
            raise BridgeError("Connected vault does not match --vault", code="VAULT_MISMATCH", outcome="not_applied",
                              details={"stage": "vault", "actualVault": connected["vault"], "checks": checks})
        checks.append({"stage": "vault", "ok": True, "name": connected["vault"], "id": connected.get("id")})
        if connected.get("pluginVersion") is None:
            message = "Enable the tldraw community plugin" if connected.get("installed") else "Install and enable the tldraw community plugin"
            raise BridgeError(message, code="TLDRAW_UNAVAILABLE", outcome="not_applied",
                              details={"stage": "plugin", "checks": checks})
        return checks

    def call(self, action, args=None, request_id=None):
        # Dispatch, polling and best-effort receipt cleanup share one budget.
        deadline = time.monotonic() + self.timeout
        checks = self._diagnose_connection(deadline) if action == "doctor" else None
        try:
            result = self._call(action, args, request_id, deadline)
        except BridgeError as exc:
            if checks is None:
                raise
            raise BridgeError(str(exc), code=exc.code, outcome=exc.outcome, request_id=exc.request_id,
                              details={**exc.details, "stage": "runtime", "checks": checks}) from exc
        if checks is not None:
            if not result.get("supported"):
                missing = result.get("missingCapabilities", [])
                raise BridgeError("Required tldraw APIs are unavailable: " + ", ".join(missing),
                                  code="TLDRAW_UNSUPPORTED", outcome="not_applied",
                                  details={"stage": "plugin", "checks": checks, "pluginVersion": result.get("pluginVersion"),
                                           "missingCapabilities": missing})
            result = {**result, "checks": checks + [
                {"stage": "plugin", "ok": True, "version": result["pluginVersion"]},
                {"stage": "runtime", "ok": True}]}
        return result

    def _call(self, action, args, request_id, deadline):
        job_id = request_id or "bridge-" + uuid.uuid4().hex
        loader, module = self._runtime()
        identity = json.dumps(job_id)
        self._runtime_evaluate(f"{loader}.dispatch(app,{module},{json.dumps(action)},{json.dumps(args or {})},{identity})", job_id, True, deadline=deadline)
        while time.monotonic() < deadline:
            job = self._runtime_evaluate(f"{loader}.poll(app,{module},{identity})", job_id, True, deadline=deadline)
            if job and job.get("status") == "failed":
                failure = job.get("failure", {})
                if failure.get("outcome", "unknown") == "not_applied":
                    self._release_automatic(job_id, request_id, deadline)
                raise BridgeError(job["error"] + " (request " + job_id + ")",
                                  code=failure.get("code", "BRIDGE_ERROR"),
                                  outcome=failure.get("outcome", "unknown"), request_id=job_id,
                                  details={**(failure.get("details") or {}), **self._evaluation_details()})
            if job and job.get("status") == "complete":
                self._release_automatic(job_id, request_id, deadline)
                return job["result"]
            time.sleep(min(0.1, max(0, deadline - time.monotonic())))
        raise BridgeError("Request timed out; use status or resume with the same --request-id: " + job_id, code="RESULT_UNKNOWN", request_id=job_id, details=self._evaluation_details())
