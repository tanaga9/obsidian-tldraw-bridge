"""CLI transport: argv only; requests never pass through a shell."""
import json
import os
from pathlib import Path
import shutil
import subprocess
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

    def evaluate(self, code, missing_ok=False):
        try:
            proc = subprocess.run([self.executable, "vault=" + self.vault, "eval", "code=" + code],
                                  text=True, capture_output=True, timeout=self.timeout)
        except subprocess.TimeoutExpired as exc:
            raise BridgeError("Obsidian CLI timed out; the request may still be running. Do not blindly repeat mutations.") from exc
        except OSError as exc:
            raise BridgeError("Could not invoke Obsidian CLI: " + str(exc)) from exc
        values = [line[3:] for line in proc.stdout.splitlines() if line.startswith("=> ")]
        if proc.returncode or (not values and not missing_ok):
            raise BridgeError("CLI evaluation failed: " + (proc.stdout + proc.stderr).strip())
        if not values:
            return None
        try:
            return json.loads(values[-1])
        except json.JSONDecodeError as exc:
            raise BridgeError("Unexpected CLI response: " + values[-1]) from exc

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
            raise BridgeError(str(exc), code="RESULT_UNKNOWN", request_id=request_id) from exc
        if isinstance(result, dict) and "_bridgeError" in result:
            error = result["_bridgeError"]
            raise BridgeError(error["message"], code=error["code"], outcome=error["outcome"], request_id=request_id)
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
                                  details=failure.get("details"))
            if job and job.get("status") == "complete":
                self._release_automatic(job_id, request_id)
                return job["result"]
            time.sleep(0.1)
        raise BridgeError("Request timed out; use status or resume with the same --request-id: " + job_id, code="RESULT_UNKNOWN", request_id=job_id)
