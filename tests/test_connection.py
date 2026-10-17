"""Discovery, connection diagnostics and a shared request deadline."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from obsidian_tldraw_bridge.api import Bridge
from obsidian_tldraw_bridge.obsidian import BridgeError, Client, find_cli


class ConnectionTest(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        for p in (patch('obsidian_tldraw_bridge.obsidian.find_cli', return_value='test-cli'),
                  patch('obsidian_tldraw_bridge.obsidian.tempfile.tempdir', folder.name)):
            p.start()
            self.addCleanup(p.stop)
        self.client = Client('Vault')
        self.connected = {'vault': 'Vault', 'id': 'vault-id', 'pluginVersion': '1.32.0', 'installed': True}

    def test_paths_and_invalid_timeout_fail_before_discovery(self):
        paths = ['/vault', r'C:\vault', 'C:vault', r'\\host\vault', 'folder/vault', '..', 'V\n']
        for factory in (Client, Bridge):
            for vault in paths + ['', None]:
                with self.subTest(factory=factory, vault=vault), self.assertRaises(BridgeError) as raised:
                    factory(vault)
                self.assertEqual((raised.exception.code, raised.exception.outcome), ('INVALID_INPUT', 'not_applied'))
            for timeout in (0, -1, True, float('nan'), float('inf')):
                with self.subTest(timeout=timeout), self.assertRaises(BridgeError):
                    factory('Vault', timeout=timeout)
        # A colon in a macOS name is not necessarily a Windows drive.
        Client('Research: notes')

    def test_doctor_reports_each_successful_stage(self):
        result = {'vault': 'Vault', 'pluginVersion': '1.32.0', 'supported': True, 'documents': []}
        with patch.object(self.client, 'evaluate', side_effect=[self.connected, None,
                          {'status': 'complete', 'result': result}, {'forgotten': True}]):
            doctor = self.client.call('doctor')
        self.assertEqual([c['stage'] for c in doctor['checks']], ['cli', 'connection', 'vault', 'plugin', 'runtime'])
        self.assertTrue(all(c['ok'] for c in doctor['checks']))
        self.assertEqual(doctor['documents'], [])

    def test_vault_id_is_accepted_by_diagnostic(self):
        self.client.vault = 'vault-id'
        with patch.object(self.client, 'evaluate', return_value=self.connected):
            self.assertEqual(self.client._diagnose_connection(float('inf'))[-1]['name'], 'Vault')

    def test_doctor_stops_before_dispatch_for_missing_or_disabled_plugin(self):
        for installed in (False, True):
            with self.subTest(installed=installed), patch.object(self.client, 'evaluate', return_value={
                    **self.connected, 'pluginVersion': None, 'installed': installed}) as evaluate:
                with self.assertRaises(BridgeError) as raised:
                    self.client.call('doctor')
                self.assertEqual(evaluate.call_count, 1)
            self.assertEqual(raised.exception.code, 'TLDRAW_UNAVAILABLE')
            self.assertEqual(raised.exception.details['stage'], 'plugin')
            self.assertEqual('Install' in str(raised.exception), not installed)

    def test_doctor_stops_for_wrong_vault_and_invalid_response(self):
        for value, code, stage in (({**self.connected, 'vault': 'Other'}, 'VAULT_MISMATCH', 'vault'),
                                   (None, 'CLI_CONNECTION_FAILED', 'connection')):
            with self.subTest(value=value), patch.object(self.client, 'evaluate', return_value=value) as evaluate:
                with self.assertRaises(BridgeError) as raised:
                    self.client.call('doctor')
                self.assertEqual(evaluate.call_count, 1)
            self.assertEqual((raised.exception.code, raised.exception.details['stage']), (code, stage))

    def test_doctor_connection_failure_preserves_retained_files(self):
        with patch.object(self.client, 'evaluate', side_effect=BridgeError('No response', details={'evaluationFiles': ['pending.js']})):
            with self.assertRaises(BridgeError) as raised:
                self.client.call('doctor')
        self.assertEqual(raised.exception.details['stage'], 'connection')
        self.assertEqual(raised.exception.details['evaluationFiles'], ['pending.js'])
        self.assertEqual(raised.exception.outcome, 'unknown')

    def test_doctor_runtime_failure_preserves_receipt_and_stage(self):
        with patch.object(self.client, 'evaluate', side_effect=[self.connected, BridgeError('lost')]):
            with self.assertRaises(BridgeError) as raised:
                self.client.call('doctor', request_id='check')
        self.assertEqual((raised.exception.code, raised.exception.request_id), ('RESULT_UNKNOWN', 'check'))
        self.assertEqual(raised.exception.details['stage'], 'runtime')

    def test_doctor_unsupported_version_uses_runtime_support_policy(self):
        with patch.object(self.client, 'evaluate', side_effect=[{**self.connected, 'pluginVersion': '99.0'}, None,
                          {'status': 'complete', 'result': {'supported': False, 'pluginVersion': '99.0'}}]):
            with self.assertRaises(BridgeError) as raised:
                self.client.call('doctor', request_id='check')
        self.assertEqual(raised.exception.code, 'TLDRAW_UNSUPPORTED')
        self.assertEqual(raised.exception.details['pluginVersion'], '99.0')

    def test_disabled_cli_is_reported_without_polling_or_losing_identity(self):
        output = subprocess.CompletedProcess([], 0, b'Command line interface is not enabled. Please turn it on in Settings > General > Advanced.', b'')
        with patch.object(self.client, '_run_cli', return_value=output) as run:
            with self.assertRaises(BridgeError) as raised:
                self.client.call('apply', request_id='edit')
        self.assertEqual(run.call_count, 1)
        self.assertEqual((raised.exception.code, raised.exception.outcome, raised.exception.request_id),
                         ('CLI_DISABLED', 'unknown', 'edit'))
        self.assertTrue(Path(raised.exception.details['evaluationFiles'][0]).exists())

    def test_vault_guard_precedes_runtime_side_effects(self):
        # Execute the emitted wrapper, verifying a mismatched receiver never calls the expression.
        for requested in ('Vault', 'vault-id', 'Other'):
            self.client.vault = requested
            def evaluate(source, *args, **kwargs):
                harness = "const app={vault:{getName:()=> 'Vault'},appId:'vault-id'};let touched=false;const value=eval(" + json.dumps(source) + ");console.log(JSON.stringify({value:JSON.parse(value),touched}));"
                result = subprocess.run(['node', '-e', harness], capture_output=True, check=True)
                data = json.loads(result.stdout)
                self.assertEqual(data['touched'], requested != 'Other')
                return data['value']
            with self.subTest(requested=requested), patch.object(self.client, 'evaluate', side_effect=evaluate):
                if requested == 'Other':
                    with self.assertRaises(BridgeError) as raised:
                        self.client._runtime_evaluate("(touched=true,JSON.stringify({ok:true}))", 'edit')
                    self.assertEqual(raised.exception.code, 'VAULT_MISMATCH')
                else:
                    self.assertEqual(self.client._runtime_evaluate("(touched=true,JSON.stringify({ok:true}))"), {'ok': True})

    def test_dispatch_and_poll_share_budget(self):
        now = [100.0]
        budgets = []
        def evaluate(code, *args, timeout=None):
            budgets.append(timeout)
            now[0] += 12
            return None if '.dispatch(' in code else {'status': 'complete', 'result': {'saved': True}}
        with patch('time.monotonic', side_effect=lambda: now[0]), patch.object(self.client, 'evaluate', side_effect=evaluate):
            self.assertEqual(self.client.call('apply', request_id='edit'), {'saved': True})
        self.assertEqual(budgets, [30, 18])

    def test_expired_dispatch_does_not_start_another_poll(self):
        now = [100.0]
        def evaluate(*args, **kwargs):
            now[0] += 31
        with patch('time.monotonic', side_effect=lambda: now[0]), patch.object(self.client, 'evaluate', side_effect=evaluate) as run:
            with self.assertRaises(BridgeError) as raised:
                self.client.call('apply', request_id='edit')
            self.assertEqual(run.call_count, 1)
        self.assertEqual((raised.exception.code, raised.exception.request_id), ('RESULT_UNKNOWN', 'edit'))

    def test_cleanup_uses_remaining_budget_and_cannot_hide_success(self):
        now = [100.0]
        budgets = []
        def evaluate(code, *args, timeout=None):
            budgets.append(timeout)
            if '.dispatch(' in code:
                now[0] += 5
                return None
            if '.poll(' in code:
                now[0] += 20
                return {'status': 'complete', 'result': {'saved': True}}
            raise BridgeError('cleanup timed out')
        with patch('time.monotonic', side_effect=lambda: now[0]), patch.object(self.client, 'evaluate', side_effect=evaluate):
            self.assertEqual(self.client.call('apply'), {'saved': True})
        self.assertEqual(budgets, [30, 25, 5])

    def test_doctor_probe_consumes_the_same_budget(self):
        now = [0.0]
        budgets = []
        def evaluate(code, *args, timeout=None):
            budgets.append(timeout)
            now[0] += 5
            if 'pluginVersion:app.plugins' in code:
                return self.connected
            if '.dispatch(' in code:
                return None
            return {'status': 'complete', 'result': {'supported': True, 'pluginVersion': '1.32.0'}}
        with patch('time.monotonic', side_effect=lambda: now[0]), patch.object(self.client, 'evaluate', side_effect=evaluate):
            self.client.call('doctor', request_id='check')
        self.assertEqual(budgets, [30, 25, 20])

    def test_no_budget_for_cleanup_retains_success_without_another_cli_call(self):
        now = [0.0]
        def evaluate(code, *args, **kwargs):
            if '.dispatch(' in code:
                now[0] = 5
                return None
            now[0] = 30
            return {'status': 'complete', 'result': {'saved': True}}
        with patch('time.monotonic', side_effect=lambda: now[0]), patch.object(self.client, 'evaluate', side_effect=evaluate) as run:
            self.assertEqual(self.client.call('apply'), {'saved': True})
            self.assertEqual(run.call_count, 2)


class WindowsDiscoveryTest(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.commands = {}
        for p in (patch('obsidian_tldraw_bridge.obsidian.sys.platform', 'win32'),
                  patch.dict(os.environ, {}, clear=True),
                  patch('obsidian_tldraw_bridge.obsidian.shutil.which', side_effect=self.commands.get)):
            p.start()
            self.addCleanup(p.stop)

    def file(self, relative):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()
        return path

    def test_com_path_registration_precedes_gui_and_default_install(self):
        cli = self.file('registered/Obsidian.com')
        gui = self.file('other/Obsidian.exe')
        self.commands.update({'Obsidian.com': str(cli), 'obsidian': str(gui)})
        self.assertEqual(find_cli(), str(cli.resolve()))

    def test_gui_path_registration_selects_same_install_cli(self):
        gui = self.file('registered/Obsidian.exe')
        cli = self.file('registered/Obsidian.com')
        self.commands['obsidian'] = str(gui)
        self.assertEqual(find_cli(), str(cli.resolve()))

    def test_user_install_is_found_without_path_registration(self):
        cli = self.file('local/Programs/Obsidian/Obsidian.com')
        with patch.dict(os.environ, {'LOCALAPPDATA': str(self.root / 'local')}):
            self.assertEqual(find_cli(), str(cli.resolve()))

    def test_system_install_and_gui_only_skip(self):
        gui = self.file('old/Obsidian.exe')
        self.commands['obsidian'] = str(gui)
        cli = self.file('system/Obsidian/Obsidian.com')
        with patch.dict(os.environ, {'ProgramFiles': str(self.root / 'system')}):
            self.assertEqual(find_cli(), str(cli.resolve()))

    def test_explicit_windows_gui_is_rejected_before_launch(self):
        gui = self.file('explicit/Obsidian.exe')
        with self.assertRaises(BridgeError) as raised:
            find_cli(str(gui))
        self.assertEqual(raised.exception.code, 'CLI_EXECUTABLE_REQUIRED')
        self.assertIn('Obsidian.com', str(raised.exception))

    def test_missing_cli_has_typed_discovery_stage(self):
        with self.assertRaises(BridgeError) as raised:
            find_cli()
        self.assertEqual((raised.exception.code, raised.exception.outcome, raised.exception.details['stage']),
                         ('CLI_NOT_FOUND', 'not_applied', 'cli'))


if __name__ == '__main__':
    unittest.main()
