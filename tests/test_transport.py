import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from obsidian_tldraw_bridge.obsidian import Client, BridgeError, find_cli

class CliDiscoveryTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.default = self.root / "Applications/Obsidian.app/Contents/MacOS/obsidian-cli"
        self.commands = {}
        for patcher in (
            patch.dict("os.environ", {}, clear=True),
            patch("obsidian_tldraw_bridge.obsidian.DEFAULT_CLI", self.default),
            patch("obsidian_tldraw_bridge.obsidian.shutil.which", side_effect=self.commands.get),
        ):
            patcher.start()
            self.addCleanup(patcher.stop)

    def file(self, path):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()
        return str(path)

    def test_explicit_override_precedes_environment_and_discovery(self):
        explicit = self.file(self.root / "custom cli")
        with patch.dict("os.environ", {"OBSIDIAN_CLI": "/missing/environment"}):
            self.assertEqual(find_cli(explicit), str(Path(explicit).resolve()))

    def test_environment_override_resolves_command_name(self):
        cli = self.file(self.root / "custom-cli")
        self.commands["custom-command"] = cli
        with patch.dict("os.environ", {"OBSIDIAN_CLI": "custom-command"}):
            self.assertEqual(find_cli(), str(Path(cli).resolve()))

    def test_missing_override_does_not_silently_use_default(self):
        self.file(self.default)
        with self.assertRaisesRegex(BridgeError, "Specified Obsidian CLI not found"):
            find_cli(str(self.root / "missing"))
        with patch.dict("os.environ", {"OBSIDIAN_CLI": str(self.root / "missing-env")}):
            with self.assertRaisesRegex(BridgeError, "Specified Obsidian CLI not found"):
                find_cli()

    def test_registered_symlink_precedes_other_installations(self):
        target = self.root / "Other.app/Contents/MacOS/obsidian-cli"
        self.file(target)
        self.file(self.default)
        link = self.root / "bin/obsidian"
        link.parent.mkdir()
        link.symlink_to(target)
        self.commands["obsidian"] = str(link)
        self.commands["obsidian-cli"] = str(self.default)
        self.assertEqual(find_cli(), str(target.resolve()))

    def test_legacy_registration_uses_cli_in_same_bundle(self):
        gui = self.root / "Other.app/Contents/MacOS/Obsidian"
        self.file(gui)
        cli = gui.with_name("obsidian-cli")
        self.file(cli)
        self.file(self.default)
        link = self.root / "obsidian"
        link.symlink_to(gui)
        self.commands["obsidian"] = str(link)
        self.assertEqual(find_cli(), str(cli.resolve()))

    def test_legacy_gui_without_cli_is_skipped(self):
        self.commands["obsidian"] = self.file(self.root / "Old.app/Contents/MacOS/Obsidian")
        cli = self.file(self.root / "bin/obsidian-cli")
        self.commands["obsidian-cli"] = cli
        self.assertEqual(find_cli(), str(Path(cli).resolve()))

    def test_default_dedicated_cli_without_path_registration(self):
        self.file(self.default)
        self.assertEqual(find_cli(), str(self.default.resolve()))

    def test_gui_only_installation_is_not_a_fallback(self):
        gui = self.default.with_name("Obsidian")
        self.commands["obsidian"] = self.file(gui)
        with self.assertRaisesRegex(BridgeError, "Update the Obsidian installer"):
            find_cli()

    def test_explicit_gui_path_is_not_rewritten(self):
        gui = self.default.with_name("Obsidian")
        self.file(gui)
        self.file(self.default)
        self.assertEqual(find_cli(str(gui)), str(gui.resolve()))

class TransportTest(unittest.TestCase):
    def client(self):
        with patch("obsidian_tldraw_bridge.obsidian.find_cli", return_value="/app/obsidian"):
            return Client("Vault with spaces")

    def test_code_is_argv_not_shell(self):
        client = self.client()
        code = 'require("a path;$(touch nope)")'
        proc = subprocess.CompletedProcess([],0,'installer warning\n=> {"ok":true}\n','')
        with patch("subprocess.run", return_value=proc) as run:
            self.assertEqual(client.evaluate(code), {"ok":True})
            self.assertEqual(run.call_args.args[0][-1], "code="+code)
            self.assertNotIn("shell", run.call_args.kwargs)

    def test_dispatch_poll_and_forget_use_loader_with_runtime_path(self):
        client = self.client()
        with patch.object(client, "evaluate", side_effect=[None, {"status":"complete", "result":{}}, {"forgotten":True}]) as evaluate:
            client.call("doctor")
            calls = [item.args[0] for item in evaluate.call_args_list]
            for code in calls:
                self.assertIn("loader.cjs", code)
                self.assertIn(json.dumps(client.module), code)
            self.assertIn(".dispatch(app,", calls[0])
            self.assertIn(".poll(app,", calls[1])
            self.assertIn(".forget(app,", calls[2])

    def test_lost_dispatch_output_still_polls(self):
        client = self.client()
        with patch.object(client, "evaluate", side_effect=[None,{"status":"running"},{"status":"complete","result":{"saved":True}}]):
            self.assertEqual(client.call("saved",{},"test-id"), {"saved":True})

    def test_failures_are_not_retried(self):
        client = self.client()
        with patch.object(client,"evaluate",side_effect=[None,{"status":"failed","error":"Revision conflict"}]) as evaluate:
            with self.assertRaisesRegex(BridgeError,"Revision conflict"):
                client.call("batch",{},"test-id")
            self.assertEqual(evaluate.call_count,2)

    def test_automatic_results_are_released(self):
        client = self.client()
        with patch.object(client,"evaluate",side_effect=[None,{"status":"complete","result":{"saved":True}},{"forgotten":True}]) as evaluate:
            self.assertEqual(client.call("saved"),{"saved":True})
            self.assertIn(".forget(app,",evaluate.call_args.args[0])

    def test_cleanup_failure_does_not_hide_success(self):
        client = self.client()
        with patch.object(client,"evaluate",side_effect=[None,{"status":"complete","result":{"saved":True}},BridgeError("cleanup failed")]):
            self.assertEqual(client.call("saved"),{"saved":True})

    def test_failed_automatic_results_are_released(self):
        client = self.client()
        with patch.object(client,"evaluate",side_effect=[None,{"status":"failed","error":"conflict","failure":{"outcome":"not_applied"}},{"forgotten":True}]) as evaluate:
            with self.assertRaisesRegex(BridgeError,"conflict"):
                client.call("batch")
            self.assertIn(".forget(app,",evaluate.call_args.args[0])


class RequestRecoveryTest(unittest.TestCase):
    client = TransportTest.client
    def test_dispatch_timeout_reports_generated_identity(self):
        client = self.client()
        with patch.object(client, 'evaluate', side_effect=BridgeError('timeout')):
            with self.assertRaises(BridgeError) as failure:
                client.call('apply', {})
        self.assertEqual(failure.exception.code, 'RESULT_UNKNOWN')
        self.assertTrue(failure.exception.request_id.startswith('bridge-'))

    def test_applied_failure_receipt_is_retained(self):
        client = self.client()
        failure = {'status': 'failed', 'error': 'not saved',
                   'failure': {'code': 'SAVE_UNCONFIRMED', 'outcome': 'applied', 'details': {'revision': 'r'}}}
        with patch.object(client, 'evaluate', side_effect=[None, failure]) as evaluate:
            with self.assertRaises(BridgeError) as raised:
                client.call('apply')
            self.assertEqual(evaluate.call_count, 2)
        self.assertEqual(raised.exception.outcome, 'applied')
        self.assertEqual(raised.exception.details['revision'], 'r')

    def test_status_does_not_dispatch_or_release_and_omits_script(self):
        client = self.client()
        with patch.object(client, 'evaluate', return_value={'id': 'x', 'status': 'running', 'request': 'script contents'}) as evaluate:
            self.assertEqual(client.status('x'), {'id': 'x', 'status': 'running'})
            self.assertEqual(evaluate.call_count, 1)
            self.assertIn('.poll(', evaluate.call_args.args[0])

class RuntimeAdmissionTest(unittest.TestCase):
    client = TransportTest.client

    def test_typed_admission_error_is_not_relabelled_as_transport_timeout(self):
        client = self.client()
        with patch.object(client, 'evaluate', return_value={'_bridgeError': {
            'code': 'RUNTIME_BUSY', 'message': 'CLI job still running', 'outcome': 'not_applied'}}):
            with self.assertRaises(BridgeError) as failure:
                client.call('apply', {}, 'attempt')
        self.assertEqual(failure.exception.code, 'RUNTIME_BUSY')
        self.assertEqual(failure.exception.outcome, 'not_applied')
        self.assertEqual(failure.exception.request_id, 'attempt')

    def test_missing_receipt_does_not_look_like_an_unapplied_edit(self):
        client = self.client()
        with patch.object(client, 'evaluate', return_value={'_bridgeError': {
            'code': 'REQUEST_NOT_FOUND', 'message': 'Unknown CLI job', 'outcome': 'unknown'}}):
            with self.assertRaises(BridgeError) as failure:
                client.status('missing')
        self.assertEqual(failure.exception.code, 'REQUEST_NOT_FOUND')
        self.assertEqual(failure.exception.outcome, 'unknown')


class OsErrorRecoveryTest(unittest.TestCase):
    client = TransportTest.client

    def test_oserror_after_dispatch_keeps_unknown_outcome_and_request_id(self):
        for identity in (None, 'edit-1'):
            with self.subTest(identity=identity):
                client = self.client()
                dispatched = subprocess.CompletedProcess([], 0, '=> {"status":"running"}\n', '')
                with patch('subprocess.run', side_effect=[dispatched, FileNotFoundError('CLI replaced')]) as run:
                    with self.assertRaises(BridgeError) as failure:
                        client.call('apply', {}, identity)
                error = failure.exception
                self.assertEqual(error.code, 'RESULT_UNKNOWN')
                self.assertEqual(error.outcome, 'unknown')
                if identity is None:
                    self.assertTrue(error.request_id.startswith('bridge-'))
                else:
                    self.assertEqual(error.request_id, identity)
                self.assertIn(json.dumps(error.request_id), run.call_args_list[0].args[0][-1])
                self.assertEqual(run.call_count, 2)

    def test_cleanup_oserror_preserves_successful_edit(self):
        client = self.client()
        saved = {'revision': 'after', 'persistence': {'saved': True}}
        responses = [subprocess.CompletedProcess([], 0, '=> {"status":"running"}\n', ''),
                     subprocess.CompletedProcess([], 0, '=> ' + json.dumps({'status': 'complete', 'result': saved}) + '\n', ''),
                     PermissionError('CLI unavailable during cleanup')]
        with patch('subprocess.run', side_effect=responses) as run:
            self.assertEqual(client.call('apply'), saved)
        self.assertEqual(run.call_count, 3)
        self.assertIn('.forget(app,', run.call_args.args[0][-1])

    def test_status_oserror_preserves_queried_id(self):
        client = self.client()
        with patch('subprocess.run', side_effect=PermissionError('CLI unavailable')):
            with self.assertRaises(BridgeError) as failure:
                client.status('edit-1')
        self.assertEqual(failure.exception.code, 'RESULT_UNKNOWN')
        self.assertEqual(failure.exception.request_id, 'edit-1')
        self.assertEqual(failure.exception.outcome, 'unknown')


if __name__ == "__main__":
    unittest.main()
