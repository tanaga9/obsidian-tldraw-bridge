"""Offline recovery checks for the opt-in live reload test; never connects to Obsidian."""
import contextlib
import io
import json
from pathlib import Path
import runpy
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from obsidian_tldraw_bridge.obsidian import BridgeError

ROOT = Path(__file__).resolve().parents[1]


class LiveReloadRecoveryTests(unittest.TestCase):
    def run_script(self, directory, scenario):
        clients = []
        runtime_paths = []
        original_mkdtemp = tempfile.mkdtemp

        def make_directory(*args, **kwargs):
            kwargs['dir'] = directory
            result = original_mkdtemp(*args, **kwargs)
            runtime_paths.append(Path(result))
            return result

        class FakeClient:
            def __init__(self, vault):
                self.module = str(ROOT / 'src/obsidian_tldraw_bridge/runtime/bridge.cjs')
                self.calls = []
                self.opens = 0
                self.version = 1
                self.session_open = False
                self.receipts = {}
                clients.append(self)

            def call(self, action, args=None, request_id=None):
                self.calls.append((action, request_id))
                if request_id in self.receipts:
                    return self.receipts[request_id]
                snapshot = {'records': [], 'revision': 'r', 'currentPageId': 'page:test',
                            'persistence': {'saved': True}}
                if action == 'open':
                    self.opens += 1
                    if self.opens == 2 and scenario == 'reopen_timeout':
                        raise BridgeError('Unknown reopen outcome', code='RESULT_UNKNOWN',
                                          outcome='unknown', request_id=request_id)
                    self.session_open = True
                    result = snapshot
                elif action == 'doctor':
                    if not self.session_open and 'runtimeTestVersion: 2' in Path(self.module).read_text():
                        self.version = 2
                    result = {'runtimeTestVersion': self.version,
                              'documents': ['test.md'] if self.session_open else [],
                              'pendingUpdate': {'reason': 'open_sessions', 'documents': ['test.md']}
                              if self.session_open and 'runtimeTestVersion: 2' in Path(self.module).read_text()
                              else None}
                    if scenario == 'assertion_failure':
                        result['runtimeTestVersion'] = 99
                elif action == 'close':
                    if self.opens == 2 and scenario == 'cleanup_timeout':
                        raise BridgeError('Unknown close outcome', code='RESULT_UNKNOWN',
                                          outcome='unknown', request_id=request_id)
                    self.session_open = False
                    result = {'closed': True}
                elif action in ('state', 'script'):
                    result = snapshot
                else:
                    raise AssertionError(action)
                self.receipts[request_id] = result
                return result

            def evaluate(self, code, *args):
                self.calls.append(('evaluate', None))
                raise BridgeError('Unknown vault evaluation outcome', code='RESULT_UNKNOWN', outcome='unknown')

            def forget(self, request_id):
                self.calls.append(('forget', request_id))
                return {'forgotten': self.receipts.pop(request_id, None) is not None}

        argv = ['live_reload.py', '--vault', 'mock', '--path', 'test.md']
        if scenario == 'evaluation_timeout':
            argv.append('--multi-page-copy')
        failure = None
        with patch('obsidian_tldraw_bridge.obsidian.Client', FakeClient), \
                patch('tempfile.mkdtemp', side_effect=make_directory), \
                patch.object(sys, 'argv', argv), \
                contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            try:
                runpy.run_path(str(ROOT / 'tests/live_reload.py'), run_name='__main__')
            except (BridgeError, AssertionError) as error:
                failure = error
        return clients[0], runtime_paths[0], failure

    def test_unknown_reopen_stops_cleanup_and_retains_request_and_runtime(self):
        with tempfile.TemporaryDirectory() as root:
            client, directory, failure = self.run_script(root, 'reopen_timeout')
            self.assertEqual(failure.code, 'RESULT_UNKNOWN')
            self.assertEqual(client.calls[-1][0], 'open')
            pending = json.loads((directory / 'pending.json').read_text())
            self.assertEqual(pending['requestId'], client.calls[-1][1])
            self.assertEqual(pending['action'], 'open')
            self.assertTrue((directory / 'bridge.cjs').exists())
            self.assertTrue((directory / 'loader.cjs').exists())
            self.assertEqual(json.loads((directory / 'manifest.json').read_text())['vault'], 'mock')

    def test_unknown_cleanup_close_retains_files_without_followup_requests(self):
        with tempfile.TemporaryDirectory() as root:
            client, directory, failure = self.run_script(root, 'cleanup_timeout')
            self.assertEqual(failure.code, 'RESULT_UNKNOWN')
            self.assertEqual(client.calls[-1][0], 'close')
            self.assertEqual(json.loads((directory / 'pending.json').read_text())['action'], 'close')
            self.assertTrue((directory / 'bridge.cjs').exists())

    def test_unknown_vault_evaluation_preserves_slot_without_cleanup(self):
        with tempfile.TemporaryDirectory() as root:
            client, directory, failure = self.run_script(root, 'evaluation_timeout')
            self.assertEqual(failure.code, 'RESULT_UNKNOWN')
            self.assertEqual(client.calls, [('evaluate', None)])
            pending = json.loads((directory / 'pending.json').read_text())
            self.assertEqual(pending['kind'], 'evaluation')
            self.assertTrue(pending['slot'].startswith('bridge-live-reload-'))
            self.assertTrue((directory / 'bridge.cjs').exists())

    def test_confirmed_assertion_failure_closes_session_and_preserves_diagnostics(self):
        with tempfile.TemporaryDirectory() as root:
            client, directory, failure = self.run_script(root, 'assertion_failure')
            self.assertIsInstance(failure, AssertionError)
            self.assertFalse(client.session_open)
            self.assertTrue((directory / 'manifest.json').exists())

    def test_success_cleans_sessions_receipts_and_temporary_directory(self):
        with tempfile.TemporaryDirectory() as root:
            client, directory, failure = self.run_script(root, 'success')
            self.assertIsNone(failure)
            self.assertFalse(client.session_open)
            self.assertFalse(client.receipts)
            self.assertFalse(directory.exists())
