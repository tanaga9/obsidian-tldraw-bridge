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
    def test_preview_format_and_quality_validation(self):
        factory = Mock()
        bridge = Bridge('V', client_factory=factory)
        for extra in ({'format': 'jpeg'}, {'format': None},
                      {'format': 'png', 'quality': .8},
                      *[{'format': 'webp', 'quality': q} for q in (True, None, '0.9', float('nan'), float('inf'), -1, 2, 10**1000)]):
            with self.subTest(extra=extra), self.assertRaises(BridgeError) as failure:
                bridge.call('preview', {'path': 'a.md', 'output': str(Path.cwd() / 'test.webp'), **extra})
            self.assertEqual(failure.exception.code, 'INVALID_INPUT')
        factory.assert_not_called()
        for quality in (0, .9, 1):
            bridge.call('preview', {'path': 'a.md', 'output': str(Path.cwd() / 'test.webp'),
                                    'format': 'webp', 'quality': quality})
            self.assertEqual(factory.return_value.call.call_args.args[1]['quality'], quality)
        bridge.call('preview', {'path': 'a.md', 'output': str(Path.cwd() / 'default.webp'), 'quality': .7})
        self.assertEqual(factory.return_value.call.call_args.args[1]['quality'], .7)

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

class StyleSpecAndScriptResultTest(unittest.TestCase):
    def test_style_spec_validates_before_connecting(self):
        factory = Mock()
        bridge = Bridge('V', client_factory=factory)
        for args in ({'path': 'a.md'}, {'path': 'a.md', 'shapeType': ''},
                     {'path': 'a.md', 'shapeType': None}, {'path': 'a.md', 'shapeType': '  '},
                     {'path': '../a.md', 'shapeType': 'geo'},
                     {'path': 'a.md', 'shapeType': 'geo', 'revision': 'r'}):
            with self.subTest(args=args), self.assertRaises(BridgeError):
                bridge.call('style-spec', args)
        factory.assert_not_called()

    def test_style_spec_cli_and_api_use_the_same_contract(self):
        args = {'path': 'a.md', 'shapeType': 'geo'}
        result = {'path': 'a.md', 'shapeType': 'geo', 'properties': {'status': 'available', 'value': {}}}
        factory = Mock()
        factory.return_value.call.return_value = result
        self.assertEqual(Bridge('V', client_factory=factory).call('style-spec', args), result)
        factory.return_value.call.assert_called_once_with('style-spec', args, None)
        with patch('obsidian_tldraw_bridge.cli.Client') as client, contextlib.redirect_stdout(io.StringIO()) as output:
            client.return_value.call.return_value = result
            self.assertEqual(main(['--vault', 'V', 'style-spec', 'a.md', '--shape-type', 'geo']), 0)
            client.return_value.call.assert_called_once_with('style-spec', args, None)
            self.assertEqual(json.loads(output.getvalue()), result)

    def test_script_result_passes_through_cli_api_and_output_failure(self):
        for full in (False, True):
            result = {'path': 'a.md', 'scriptResult': {'hasValue': True, 'value': {'value': 42, 'text': '青😀'}},
                      'persistence': {'saved': True}}
            args = {'path': 'a.md', 'revision': 'r', 'code': 'return {value:42,text:"青😀"}'}
            if full:
                args['full'] = True
                result['records'] = []
            factory = Mock()
            factory.return_value.call.return_value = result
            self.assertEqual(Bridge('V', client_factory=factory).call('script', args, 'result-id'), result)
            argv = ['--vault', 'V', '--request-id', 'result-id', 'script', 'a.md', '--revision', 'r', '--input', '-']
            if full:
                argv.append('--full')
            for broken in (False, True):
                output = Mock() if broken else io.StringIO()
                if broken:
                    output.buffer = None
                    output.write.side_effect = BrokenPipeError('closed')
                with patch('obsidian_tldraw_bridge.cli.Client') as client, patch('sys.stdin', io.StringIO(args['code'])), \
                        contextlib.redirect_stdout(output), contextlib.redirect_stderr(io.StringIO()) as errors:
                    client.return_value.call.return_value = result
                    self.assertEqual(main(argv), 1 if broken else 0)
                    client.return_value.call.assert_called_once_with('script', args, 'result-id')
                    actual = json.loads(errors.getvalue())['error']['details']['result'] if broken else json.loads(output.getvalue())
                    self.assertEqual(actual, result)
