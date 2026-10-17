import contextlib
import io
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from obsidian_tldraw_bridge.api import Bridge
from obsidian_tldraw_bridge.obsidian import BridgeError
from obsidian_tldraw_bridge.cli import main


class SharedApiTest(unittest.TestCase):
    def test_validation_is_available_without_cli_or_transport(self):
        factory = Mock()
        bridge = Bridge('V', client_factory=factory)
        for action, args in [('apply', {'path': 'a.md'}),
                             ('observe', {'path': '../a.md'}),
                             ('observe', {'path': 'a.md', 'limit': 501}),
                             ('preview', {'path': 'a.md', 'bounds': {'x': 0, 'y': 0, 'w': 0, 'h': 3}})]:
            with self.subTest(action=action, args=args), self.assertRaises(BridgeError) as failure:
                bridge.call(action, args)
            self.assertEqual(failure.exception.code, 'INVALID_INPUT')
            self.assertEqual(failure.exception.outcome, 'not_applied')
        factory.assert_not_called()

    def test_apply_preserves_named_operations_and_request_identity(self):
        factory = Mock()
        bridge = Bridge('V', client_factory=factory)
        args = {'path': 'a.md', 'revision': 'r', 'operations': [{'op': 'deleteShapes', 'ids': ['shape:a']}]}
        bridge.call('apply', args, 'edit-1')
        factory.return_value.call.assert_called_once_with('apply', args, 'edit-1')

    def test_status_queries_instead_of_dispatching(self):
        factory = Mock()
        factory.return_value.status.return_value = {'status': 'running', 'id': 'edit-1'}
        self.assertEqual(Bridge('V', client_factory=factory).status('edit-1')['status'], 'running')
        factory.return_value.call.assert_not_called()

    def test_cli_reports_structured_errors(self):
        with patch('obsidian_tldraw_bridge.cli.Client') as client:
            client.return_value.call.side_effect = BridgeError('Save pending', code='SAVE_UNCONFIRMED',
                                                               outcome='applied', request_id='edit-1')
            output = io.StringIO()
            with contextlib.redirect_stderr(output):
                self.assertEqual(main(['--vault', 'V', 'saved', 'a.md']), 1)
            self.assertEqual(json.loads(output.getvalue())['error'], {
                'code': 'SAVE_UNCONFIRMED', 'message': 'Save pending', 'outcome': 'applied', 'requestId': 'edit-1'})

class InputContractTest(unittest.TestCase):
    def test_rejects_unknown_fields_and_unpinned_pagination_before_connecting(self):
        factory = Mock()
        bridge = Bridge('V', client_factory=factory)
        for args in ({'path': 'a.md', 'part': 'ignored'}, {'path': 'a.md', 'offset': 1},
                     {'path': 'a.md', 'offset': 1, 'revision': 'r'}):
            with self.subTest(args=args), self.assertRaises(BridgeError):
                bridge.call('observe', args)
        factory.assert_not_called()
