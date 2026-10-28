"""Offline checks that interruption never races pending-update test cleanup."""
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


class LivePendingUpdateRecoveryTests(unittest.TestCase):
    def test_inflight_create_keeps_identity_and_files_without_cleanup(self):
        failures = [KeyboardInterrupt('interrupted after dispatch'),
                    BridgeError('Request timed out', code='RESULT_UNKNOWN', outcome='unknown'),
                    BridgeError('Transport outcome unavailable', code='OTHER_FAILURE', outcome='unknown')]
        for failure in failures:
            with self.subTest(failure=type(failure).__name__, code=getattr(failure, 'code', None)), \
                    tempfile.TemporaryDirectory() as root:
                calls = []
                directories = []
                original_mkdtemp = tempfile.mkdtemp

                def make_directory(*args, **kwargs):
                    kwargs['dir'] = root
                    directory = original_mkdtemp(*args, **kwargs)
                    directories.append(Path(directory))
                    return directory

                class FakeClient:
                    def __init__(self, *args, **kwargs):
                        self.module = str(ROOT / 'src/obsidian_tldraw_bridge/runtime/bridge.cjs')

                    def call(self, action, args=None, request_id=None):
                        calls.append((action, request_id))
                        if action == 'doctor':
                            return {'documents': [], 'runtimeTestVersion': 1}
                        if action == 'create':
                            # Recovery information must already be durable when
                            # the request can reach Obsidian.
                            recovery = json.loads((directories[0] / 'pending-request.json').read_text())
                            if recovery['requestId'] != request_id:
                                raise AssertionError('Request identity was not recorded before dispatch')
                            raise failure
                        raise AssertionError('Unexpected follow-up request: ' + action)

                    def evaluate(self, *args, **kwargs):
                        calls.append(('evaluate', None))
                        raise AssertionError('Cleanup must not follow an uncertain create')

                    def forget(self, request_id):
                        calls.append(('forget', request_id))
                        raise AssertionError('Receipts must be retained during an uncertain create')

                with patch('obsidian_tldraw_bridge.obsidian.Client', FakeClient), \
                        patch('tempfile.mkdtemp', side_effect=make_directory), \
                        contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    namespace = runpy.run_path(str(ROOT / 'tests/live_pending_update.py'), run_name='offline_test')
                    with self.assertRaises(type(failure)) as caught:
                        namespace['run']('mock')
                self.assertIs(caught.exception, failure)
                self.assertEqual([action for action, _ in calls], ['doctor', 'create'])
                directory = directories[0]
                pending = json.loads((directory / 'pending-request.json').read_text())
                self.assertEqual(pending['requestId'], calls[-1][1])
                self.assertEqual(pending['action'], 'create')
                self.assertEqual(json.loads((directory / 'manifest.json').read_text())['vault'], 'mock')
                self.assertTrue((directory / 'bridge.cjs').exists())
                self.assertTrue((directory / 'loader.cjs').exists())
