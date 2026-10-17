"""Locale-independent UTF-8 at the CLI and Obsidian process boundaries."""
import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from obsidian_tldraw_bridge.cli import main
from obsidian_tldraw_bridge.obsidian import BridgeError, Client


class UnicodeCliTest(unittest.TestCase):
    text = "日本語の図 🌿"

    def test_utf8_and_bom_files_preserve_script_and_json(self):
        cases = [("script", "const title = " + json.dumps(self.text, ensure_ascii=False) + ";"),
                 ("batch", json.dumps([{"method": "deleteShapes", "args": [["shape:" + self.text]]}], ensure_ascii=False))]
        with tempfile.TemporaryDirectory() as directory:
            for command, source in cases:
                for bom in (b"", b"\xef\xbb\xbf"):
                    with self.subTest(command=command, bom=bool(bom)):
                        path = Path(directory) / (self.text + ".txt")
                        path.write_bytes(bom + source.encode("utf-8"))
                        with patch("obsidian_tldraw_bridge.cli.Client") as client:
                            client.return_value.call.return_value = {}
                            with contextlib.redirect_stdout(io.StringIO()):
                                self.assertEqual(main(["--vault", "Vault", command, "plan.md",
                                                       "--revision", "r", "--input", str(path)]), 0)
                            arguments = client.return_value.call.call_args.args[1]
                            self.assertEqual(arguments["code" if command == "script" else "operations"],
                                             source if command == "script" else json.loads(source))

    def test_redirected_stdio_uses_utf8_without_reconfiguring_streams(self):
        source = "// " + self.text
        for bom in (b"", b"\xef\xbb\xbf"):
            with self.subTest(bom=bool(bom)), contextlib.ExitStack() as stack:
                stdin = stack.enter_context(io.TextIOWrapper(io.BytesIO(bom + source.encode("utf-8")), encoding="ascii"))
                output = io.BytesIO()
                stdout = stack.enter_context(io.TextIOWrapper(output, encoding="ascii"))
                client = stack.enter_context(patch("obsidian_tldraw_bridge.cli.Client"))
                client.return_value.call.return_value = {"path": self.text + ".md"}
                stack.enter_context(patch("sys.stdin", stdin))
                stack.enter_context(contextlib.redirect_stdout(stdout))
                self.assertEqual(main(["--vault", "Vault", "script", "plan.md", "--revision", "r", "--input", "-"]), 0)
                self.assertEqual(client.return_value.call.call_args.args[1]["code"], source)
                self.assertEqual(json.loads(output.getvalue().decode("utf-8")), {"path": self.text + ".md"})
                self.assertEqual((stdin.encoding, stdout.encoding), ("ascii", "ascii"))

    def test_unicode_errors_are_utf8_json_on_stderr(self):
        output = io.BytesIO()
        with io.TextIOWrapper(output, encoding="ascii") as stderr, \
                contextlib.redirect_stderr(stderr), patch("obsidian_tldraw_bridge.cli.Client") as client:
            client.return_value.call.side_effect = BridgeError(self.text, code="RESULT_UNKNOWN", request_id="edit-1")
            self.assertEqual(main(["--vault", "Vault", "saved", "plan.md"]), 1)
            error = json.loads(output.getvalue().decode("utf-8"))["error"]
            self.assertEqual(error["message"], self.text)
            self.assertEqual((error["code"], error["outcome"], error["requestId"]),
                             ("RESULT_UNKNOWN", "unknown", "edit-1"))

    def test_invalid_utf8_inputs_fail_before_connecting(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.js"
            path.write_bytes(b"\xff")
            for input_path in (str(path), "-"):
                with self.subTest(input_path=input_path), io.TextIOWrapper(io.BytesIO(b"\xff"), encoding="ascii") as stdin, \
                        patch("sys.stdin", stdin), contextlib.redirect_stderr(io.StringIO()) as stderr, \
                        patch("obsidian_tldraw_bridge.cli.Client") as client:
                    self.assertEqual(main(["--vault", "Vault", "script", "plan.md",
                                           "--revision", "r", "--input", input_path]), 1)
                    client.assert_not_called()
                    error = json.loads(stderr.getvalue())["error"]
                    self.assertEqual((error["code"], error["outcome"]), ("INVALID_INPUT", "not_applied"))

    def test_real_process_ignores_ascii_stdio_environment(self):
        code = """
import sys
sys.path.insert(0, sys.argv[1])
from obsidian_tldraw_bridge import cli
class FakeClient:
    def __init__(self, *args): pass
    def call(self, action, arguments, request_id): return arguments
cli.Client = FakeClient
sys.exit(cli.main(['--vault', 'Vault', 'script', 'plan.md', '--revision', 'r', '--input', '-']))
"""
        environment = dict(os.environ, PYTHONIOENCODING="ascii", PYTHONUTF8="0", PYTHONDONTWRITEBYTECODE="1")
        source = "// " + self.text
        result = subprocess.run([sys.executable, "-c", code, str(ROOT / "src")],
                                input=source.encode("utf-8"), capture_output=True, env=environment)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout.decode("utf-8"))["code"], source)


class UnicodeTransportTest(unittest.TestCase):
    def client(self):
        with patch("obsidian_tldraw_bridge.obsidian.find_cli", return_value=sys.executable):
            return Client("Vault")

    def process(self, stdout, stderr=b"", returncode=0):
        # Exercise actual pipe decoding, rather than supplying pre-decoded mock text.
        code = ("import sys; sys.stdout.buffer.write(bytes.fromhex(" + repr(stdout.hex()) + ")); "
                "sys.stderr.buffer.write(bytes.fromhex(" + repr(stderr.hex()) + ")); "
                "sys.exit(" + str(returncode) + ")")
        run = subprocess.run
        return lambda argv, **kwargs: run([sys.executable, "-c", code], **kwargs)

    def test_utf8_stdout_and_stderr_decode_with_real_pipes(self):
        value = {"path": "図解/日本語 🌿.md"}
        stdout = ("=> " + json.dumps(value, ensure_ascii=False) + "\n").encode("utf-8")
        stderr = "日本語の警告 🌿".encode("utf-8")
        with patch("subprocess.run", side_effect=self.process(stdout, stderr)) as run:
            self.assertEqual(self.client().evaluate("null"), value)
            self.assertNotIn("text", run.call_args.kwargs)

    def test_unicode_cli_failure_keeps_diagnostic_text(self):
        message = "接続失敗 🌿"
        with patch("subprocess.run", side_effect=self.process(b"", message.encode("utf-8"), 1)):
            with self.assertRaisesRegex(BridgeError, message):
                self.client().evaluate("null")

    def test_invalid_utf8_after_dispatch_preserves_unknown_outcome_and_id(self):
        for stdout, stderr in ((b"\xff", b""), (b"", b"\xff")):
            with self.subTest(stderr=bool(stderr)):
                invalid = self.process(stdout, stderr)
                responses = iter([subprocess.CompletedProcess([], 0, b'=> {"status":"running"}\n', b'')])
                def run(argv, **kwargs):
                    first = next(responses, None)
                    return first if first is not None else invalid(argv, **kwargs)
                with patch("subprocess.run", side_effect=run):
                    with self.assertRaises(BridgeError) as raised:
                        self.client().call("apply", {}, "unicode-edit")
                error = raised.exception
                self.assertEqual((error.code, error.outcome, error.request_id),
                                 ("RESULT_UNKNOWN", "unknown", "unicode-edit"))
                self.assertIn("UTF-8", str(error))


if __name__ == "__main__":
    unittest.main()
