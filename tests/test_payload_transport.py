"""Bounded argv transport, receiver consumption, and uncertain-delivery recovery."""
import base64
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from obsidian_tldraw_bridge.obsidian import BridgeError, Client, _capture_output


def evaluation_path(argv):
    encoded = re.search(r"Buffer.from\('([^']+)','base64'\)", argv[-1]).group(1)
    return Path(base64.b64decode(encoded).decode("utf-8"))


class PayloadTransportTest(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix="bridge payload 日本語 'quoted' ")
        self.addCleanup(directory.cleanup)
        self.directory = Path(directory.name)
        patcher = patch("obsidian_tldraw_bridge.obsidian.tempfile.tempdir", directory.name)
        patcher.start()
        self.addCleanup(patcher.stop)
        with patch("obsidian_tldraw_bridge.obsidian.find_cli", return_value="unused-cli"):
            self.client = Client("Vault with spaces")

    def node(self, on_invoke=None, deny_cleanup=False):
        run = subprocess.run
        harness = r"""
const fs = require('node:fs');
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
const consumedPath = input.path;
const app = { label: 'scope preserved' };
if(input.denyCleanup) fs.unlinkSync=()=>{throw new Error('simulated sharing violation')};
process.stdout.write('=> ' + eval(input.code) + '\n');
"""
        def invoke(argv, **kwargs):
            path = evaluation_path(argv)
            if on_invoke:
                on_invoke(argv, path)
            return run(["node", "-e", harness],
                       input=json.dumps({"code": argv[-1][5:], "path": str(path), "denyCleanup": deny_cleanup}).encode("utf-8"), capture_output=True, **kwargs)
        return invoke

    def test_large_unicode_source_uses_short_argv_and_preserves_scope(self):
        text = ('日本語 🌿 "quoted" \\path\n' + "'single'; $() `backtick` ") * 5000
        source = "JSON.stringify({text:" + json.dumps(text, ensure_ascii=False) + ",scope:app.label})"
        paths = []
        def inspect(argv, path):
            paths.append(path)
            self.assertEqual(path.read_text(encoding="utf-8"), source)
            self.assertLess(len(argv[-1]), 2000)
            self.assertNotIn("日本語", argv[-1])
        with patch("obsidian_tldraw_bridge.obsidian.Client._run_cli", side_effect=self.node(inspect)):
            self.assertEqual(self.client.evaluate(source), {"text": text, "scope": "scope preserved"})
        self.assertTrue(paths)
        self.assertFalse(paths[0].exists())

    def test_receiver_removes_source_before_evaluation(self):
        with patch("obsidian_tldraw_bridge.obsidian.Client._run_cli", side_effect=self.node()):
            result = self.client.evaluate("JSON.stringify({exists:require('node:fs').existsSync(consumedPath)})")
        self.assertEqual(result, {"exists": False})

    def test_normal_return_cleans_up_when_receiver_did_not_consume(self):
        paths = []
        def invoke(argv, **kwargs):
            paths.append(evaluation_path(argv))
            return subprocess.CompletedProcess(argv, 0, b'=> {"ok":true}\n', b'')
        with patch("obsidian_tldraw_bridge.obsidian.Client._run_cli", side_effect=invoke):
            self.assertEqual(self.client.evaluate("null"), {"ok": True})
        self.assertFalse(paths[0].exists())

    def test_timeout_keeps_source_for_delayed_receiver_and_preserves_identity(self):
        invocations = []
        def timeout(argv, **kwargs):
            invocations.append(argv)
            raise subprocess.TimeoutExpired(argv, kwargs["timeout"])
        with patch("obsidian_tldraw_bridge.obsidian.Client._run_cli", side_effect=timeout):
            with self.assertRaises(BridgeError) as raised:
                self.client._runtime_evaluate("JSON.stringify({delivered:true})", "delayed-job")
        error = raised.exception
        path = evaluation_path(invocations[0])
        self.assertTrue(path.exists())
        self.assertEqual((error.code, error.outcome, error.request_id), ("RESULT_UNKNOWN", "unknown", "delayed-job"))
        self.assertEqual(error.details["evaluationFiles"], [str(path)])
        # Deliver the exact, unchanged invocation after the sender has timed out.
        self.assertIn(b'"delivered":true', self.node()(invocations[0], timeout=5).stdout)
        self.assertFalse(path.exists())

    def test_empty_output_keeps_source_for_late_consumption(self):
        invocations = []
        def no_output(argv, **kwargs):
            invocations.append(argv)
            return subprocess.CompletedProcess(argv, 0, b"", b"")
        with patch("obsidian_tldraw_bridge.obsidian.Client._run_cli", side_effect=no_output):
            self.assertIsNone(self.client.evaluate('JSON.stringify({late:true})', missing_ok=True))
        path = evaluation_path(invocations[0])
        self.assertTrue(path.exists())
        result = self.node()(invocations[0], timeout=5)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(b'"late":true', result.stdout)
        self.assertFalse(path.exists())

    def test_unacknowledged_cli_failure_reports_retained_source(self):
        result = subprocess.CompletedProcess([], 1, b"", b"CLI unavailable")
        with patch("obsidian_tldraw_bridge.obsidian.Client._run_cli", return_value=result):
            with self.assertRaises(BridgeError) as raised:
                self.client.evaluate('JSON.stringify({pending:true})')
        path = Path(raised.exception.details["evaluationFiles"][0])
        self.assertTrue(path.exists())
        self.assertEqual(path.read_text(encoding="utf-8"), 'JSON.stringify({pending:true})')

    def test_input_and_script_errors_leave_no_consumed_files(self):
        with patch("obsidian_tldraw_bridge.obsidian.Client._run_cli", side_effect=self.node()):
            with self.assertRaisesRegex(BridgeError, 'expected script failure'):
                self.client.evaluate("throw new Error('expected script failure')")
        self.assertEqual(list(self.directory.iterdir()), [])

    def test_receiver_cleanup_failure_does_not_block_evaluation(self):
        with patch("obsidian_tldraw_bridge.obsidian.Client._run_cli", side_effect=self.node(deny_cleanup=True)):
            self.assertEqual(self.client.evaluate('JSON.stringify({executed:true})'), {"executed": True})
        self.assertEqual(list(self.directory.iterdir()), [])

    def test_empty_output_deadline_reports_all_remaining_files(self):
        result = subprocess.CompletedProcess([], 0, b"", b"")
        with patch("obsidian_tldraw_bridge.obsidian.Client._run_cli", return_value=result), \
                patch("time.monotonic", side_effect=[0, 0, 31]), patch("time.sleep"):
            with self.assertRaises(BridgeError) as raised:
                self.client.call("doctor", {}, "unacknowledged-job")
        error = raised.exception
        paths = sorted(str(path) for path in self.directory.iterdir())
        self.assertEqual(len(paths), 2)  # Dispatch and poll.
        self.assertEqual(error.details["evaluationFiles"], paths)
        self.assertEqual((error.code, error.outcome, error.request_id),
                         ("RESULT_UNKNOWN", "unknown", "unacknowledged-job"))

    def test_real_launch_failure_discards_unsent_file(self):
        self.client.executable = str(self.directory / "nonexistent-cli")
        with self.assertRaises(BridgeError) as raised:
            self.client.call("doctor", {}, "not-started")
        self.assertIn("Could not start", str(raised.exception))
        self.assertNotIn("evaluationFiles", raised.exception.details)
        self.assertEqual(list(self.directory.iterdir()), [])
        self.assertEqual((raised.exception.outcome, raised.exception.request_id), ("unknown", "not-started"))

    def test_consumed_files_are_removed_from_diagnostics(self):
        result = subprocess.CompletedProcess([], 0, b"", b"")
        with patch("obsidian_tldraw_bridge.obsidian.Client._run_cli", return_value=result):
            self.client.evaluate('JSON.stringify({late:true})', missing_ok=True)
        argv = self.client._evaluation_details()["evaluationFiles"]
        self.assertEqual(len(argv), 1)
        Path(argv[0]).unlink()
        self.assertEqual(self.client._evaluation_details(), {})

    def test_invalid_source_cleans_up_before_reporting_error(self):
        with self.assertRaises(BridgeError):
            self.client.evaluate("\ud800")
        self.assertEqual(list(self.directory.iterdir()), [])
        self.assertEqual(self.client._evaluation_details(), {})

    def test_real_timed_out_child_is_killed_and_reaped(self):
        processes = []
        popen = subprocess.Popen
        def start(*args, **kwargs):
            process = popen(*args, **kwargs)
            processes.append(process)
            return process
        with patch("subprocess.Popen", side_effect=start):
            with self.assertRaises(subprocess.TimeoutExpired):
                self.client._run_cli([sys.executable, "-c", "import time; time.sleep(5)"], timeout=.05)
        self.assertEqual(len(processes), 1)
        self.assertIsNotNone(processes[0].poll())

    def test_descendant_output_handles_do_not_delay_return_or_timeout(self):
        for timeout_case in (False, True):
            with self.subTest(timeout=timeout_case), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                ready, release, finished = (root / name for name in ("ready", "release", "finished"))
                child = ("import os,time; from pathlib import Path; "
                         "ready=Path(" + repr(str(ready)) + "); "
                         "release=Path(" + repr(str(release)) + "); "
                         "finished=Path(" + repr(str(finished)) + "); "
                         "ready.write_text('ready');\n"
                         "while not release.exists(): time.sleep(.01)\n"
                         "os.close(1); os.close(2); finished.write_text('closed')")
                parent = ("import subprocess,sys,time; "
                          "sys.stdout.buffer.write(b'parent stdout');sys.stdout.flush(); "
                          "sys.stderr.buffer.write(b'parent stderr');sys.stderr.flush(); "
                          "subprocess.Popen([sys.executable,'-c'," + repr(child) + "]); "
                          + ("time.sleep(30)" if timeout_case else ""))
                popen = subprocess.Popen
                timers = []
                processes = []
                capture_names = set()
                def start(*args, **kwargs):
                    capture_names.update(stream.name.rsplit(os.sep, 1)[-1]
                                         for stream in (kwargs["stdout"], kwargs["stderr"])
                                         if isinstance(stream.name, str))
                    process = popen(*args, **kwargs)
                    processes.append(process)
                    deadline = time.monotonic() + 10
                    while not ready.exists():
                        if time.monotonic() >= deadline:
                            process.kill()
                            process.wait()
                            raise RuntimeError("Descendant did not become ready")
                        time.sleep(.01)
                    # Bound a regression's failure time without allowing it to pass
                    # just because the descendant happened to exit by itself.
                    timer = threading.Timer(3, lambda: release.write_text('release'))
                    timer.start()
                    timers.append(timer)
                    return process
                try:
                    with patch("subprocess.Popen", side_effect=start):
                        if timeout_case:
                            with self.assertRaises(subprocess.TimeoutExpired):
                                self.client._run_cli([sys.executable, "-c", parent], timeout=.05)
                        else:
                            result = self.client._run_cli([sys.executable, "-c", parent], timeout=.5)
                            self.assertEqual((result.returncode, result.stdout, result.stderr),
                                             (0, b"parent stdout", b"parent stderr"))
                    self.assertFalse(release.exists(), "Waited for descendant output handles to close")
                    self.assertIsNotNone(processes[0].poll())
                finally:
                    for timer in timers:
                        timer.cancel()
                        timer.join()
                    release.write_text('release')
                    deadline = time.monotonic() + 5
                    while not finished.exists() and time.monotonic() < deadline:
                        time.sleep(.01)
                    self.assertTrue(finished.exists(), "Descendant did not close inherited output handles")
                    # Windows finalizes delete-on-close when the descendant exits,
                    # slightly after it writes the finished marker. Only test
                    # teardown waits for that finalization; CLI return stays prompt.
                    deadline = time.monotonic() + 5
                    while capture_names.intersection(path.name for path in self.directory.iterdir()):
                        if time.monotonic() >= deadline:
                            self.fail("Capture files remained after descendant termination")
                        time.sleep(.01)

    def test_inherited_writer_cannot_move_reader_or_overwrite_response(self):
        with tempfile.TemporaryDirectory() as directory, _capture_output() as (writer, reader):
            root = Path(directory)
            ready, release = root / "ready", root / "release"
            response = b'=> {"ok":true}\n'
            code = ("import sys,time; from pathlib import Path; "
                    "sys.stdout.buffer.write(" + repr(response) + ");sys.stdout.flush(); "
                    "Path(" + repr(str(ready)) + ").touch();\n"
                    "while not Path(" + repr(str(release)) + ").exists():time.sleep(.01)\n"
                    "sys.stdout.buffer.write(b'LOG');sys.stdout.flush()")
            with subprocess.Popen([sys.executable, "-c", code], stdout=writer, stderr=subprocess.DEVNULL) as process:
                try:
                    deadline = time.monotonic() + 5
                    while not ready.exists() and time.monotonic() < deadline:
                        time.sleep(.01)
                    self.assertTrue(ready.exists(), "Writer did not produce its response")
                    # Split reading around a deterministic write by the inherited
                    # handle, after the reader has already moved its own offset.
                    prefix = reader.read(3)
                    self.assertEqual(prefix, b'=> ')
                    release.touch()
                    process.wait(timeout=5)
                    suffix = reader.read(len(response) - len(prefix))
                    self.assertEqual(prefix + suffix, response)
                    self.assertEqual(reader.read(), b'LOG')
                finally:
                    release.touch()
                    if process.poll() is None:
                        process.kill()
                        process.wait()

    def test_reader_open_failure_removes_capture_file(self):
        before = set(self.directory.iterdir())
        with patch("obsidian_tldraw_bridge.obsidian._capture_reader_opener", side_effect=PermissionError("denied")):
            with self.assertRaises(PermissionError):
                with _capture_output():
                    self.fail("Unexpected capture opened")
        self.assertEqual(set(self.directory.iterdir()), before)

    def test_capture_creation_failure_cleans_unsent_evaluation(self):
        with patch("obsidian_tldraw_bridge.obsidian._capture_output", side_effect=OSError("capture unavailable")):
            with self.assertRaises(BridgeError) as raised:
                self.client.evaluate("null")
        self.assertIn("Could not start", str(raised.exception))
        self.assertEqual(list(self.directory.iterdir()), [])
        self.assertNotIn("evaluationFiles", raised.exception.details)

    def test_cleanup_failure_does_not_hide_success(self):
        result = subprocess.CompletedProcess([], 0, b'=> {"saved":true}\n', b'')
        with patch("obsidian_tldraw_bridge.obsidian.Client._run_cli", return_value=result), patch.object(Path, "unlink", side_effect=PermissionError("locked")):
            self.assertEqual(self.client.evaluate("null"), {"saved": True})
            self.assertEqual(len(self.client._evaluation_details()["evaluationFiles"]), 1)


if __name__ == "__main__":
    unittest.main()
