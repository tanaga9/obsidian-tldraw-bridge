import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from obsidian_tldraw_bridge.cli import main


class CreateCommandTest(unittest.TestCase):
    def test_create_dispatches_path_and_request_id_without_revision(self):
        with patch('obsidian_tldraw_bridge.cli.Client') as client:
            client.return_value.call.return_value = {'path': 'Drawings/project-plan.md', 'created': True}
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                code = main(['--vault', 'Documents', '--request-id', 'create-plan', 'create', 'Drawings/project-plan.md'])
            self.assertEqual(code, 0)
            client.return_value.call.assert_called_once_with('create', {'path': 'Drawings/project-plan.md'}, 'create-plan')
            self.assertTrue(json.loads(output.getvalue())['created'])

    def test_create_rejects_invalid_paths_before_connecting(self):
        for path in ('../escape.md', '/absolute.md', 'folder/../escape.md', 'plan.tldr', 'folder\\plan.md'):
            with self.subTest(path=path), patch('obsidian_tldraw_bridge.cli.Client') as client:
                with contextlib.redirect_stderr(io.StringIO()):
                    self.assertEqual(main(['--vault', 'Documents', 'create', path]), 1)
                client.assert_not_called()


class EditOutputTest(unittest.TestCase):
    def test_real_broken_pipe_leaves_only_structured_stderr(self):
        source = '''
import sys
sys.path.insert(0, sys.argv[1])
from obsidian_tldraw_bridge import cli
class FakeClient:
    def __init__(self, *args): pass
    def call(self, *args): return {'path': 'plan.md', 'created': True}
cli.Client = FakeClient
sys.exit(cli.main(['--vault', 'V', '--request-id', 'created-note', 'create', 'plan.md']))
'''
        reader, writer = os.pipe()
        os.close(reader)
        with os.fdopen(writer, 'wb') as output:
            completed = subprocess.run([sys.executable, '-c', source,
                                        str(Path(__file__).resolve().parents[1] / 'src')],
                                       stdout=output, stderr=subprocess.PIPE)
        self.assertEqual(completed.returncode, 1, completed.stderr)
        failure = json.loads(completed.stderr)['error']
        self.assertEqual((failure['code'], failure['outcome'], failure['requestId']),
                         ('OUTPUT_FAILED', 'applied', 'created-note'))
        self.assertEqual(failure['details']['result'], {'path': 'plan.md', 'created': True})

    def test_output_io_failure_preserves_completed_edit_and_request_id(self):
        result = {'path': 'plan.md', 'revision': 'after-edit', 'persistence': {'saved': True}}
        for error in (OSError(28, 'No space left on device'), BrokenPipeError(32, 'Broken pipe')):
            for phase in ('write', 'flush'):
                for request_id in (None, 'completed-edit'):
                    with self.subTest(error=type(error).__name__, phase=phase, request_id=request_id):
                        output = Mock()
                        getattr(output.buffer, phase).side_effect = error
                        errors = io.StringIO()
                        argv = ['--vault', 'V']
                        if request_id:
                            argv += ['--request-id', request_id]
                        argv += ['script', 'plan.md', '--revision', 'before', '--input', '-']
                        with patch('obsidian_tldraw_bridge.cli.Client') as client, \
                                patch('sys.stdin', io.StringIO(';')), \
                                contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
                            client.return_value.call.return_value = result
                            self.assertEqual(main(argv), 1)
                            client.return_value.call.assert_called_once_with(
                                'script', {'path': 'plan.md', 'revision': 'before', 'code': ';'}, request_id)
                        failure = json.loads(errors.getvalue())['error']
                        self.assertEqual((failure['code'], failure['outcome']), ('OUTPUT_FAILED', 'applied'))
                        self.assertEqual(failure.get('requestId'), request_id)
                        self.assertEqual(failure['details']['result'], result)
                        self.assertEqual(failure['details']['command'], 'script')

    def test_output_encoding_failure_preserves_result_in_error(self):
        result = {'path': 'plan.md', 'revision': 'after-edit', 'text': '\ud800'}
        with patch('obsidian_tldraw_bridge.cli.Client') as client, \
                patch('sys.stdin', io.StringIO(';')), \
                io.TextIOWrapper(io.BytesIO(), encoding='utf-8') as output, \
                io.TextIOWrapper(io.BytesIO(), encoding='utf-8') as errors, \
                contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
            client.return_value.call.return_value = result
            self.assertEqual(main(['--vault', 'V', 'script', 'plan.md', '--revision', 'before', '--input', '-']), 1)
            failure = json.loads(errors.buffer.getvalue())['error']
            self.assertEqual((failure['code'], failure['outcome']), ('OUTPUT_FAILED', 'applied'))
            self.assertEqual(failure['details']['result'], result)

    def test_read_and_receipt_output_failures_preserve_their_results(self):
        for command, argument, method, result, outcome, request_id in (
                ('state', 'plan.md', 'call', {'revision': 'current'}, 'not_applied', None),
                ('status', 'pending-edit', 'status', {'status': 'running'}, 'unknown', 'pending-edit'),
                ('status', 'failed-edit', 'status', {'status': 'failed', 'failure': {'outcome': 'applied'}}, 'unknown', 'failed-edit'),
                ('forget', 'old-edit', 'forget', {'forgotten': True}, 'applied', 'old-edit')):
            with self.subTest(command=command, result=result):
                output = Mock()
                output.buffer.write.side_effect = BrokenPipeError(32, 'Broken pipe')
                errors = io.StringIO()
                with patch('obsidian_tldraw_bridge.cli.Client') as client, \
                        contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
                    getattr(client.return_value, method).return_value = result
                    self.assertEqual(main(['--vault', 'V', command, argument]), 1)
                    self.assertEqual(getattr(client.return_value, method).call_count, 1)
                failure = json.loads(errors.getvalue())['error']
                self.assertEqual((failure['code'], failure['outcome']), ('OUTPUT_FAILED', outcome))
                self.assertEqual(failure.get('requestId'), request_id)
                self.assertEqual(failure['details']['result'], result)

    def test_input_file_io_failure_remains_unapplied(self):
        with tempfile.TemporaryDirectory() as directory, patch('obsidian_tldraw_bridge.cli.Client') as client, \
                contextlib.redirect_stderr(io.StringIO()) as errors:
            self.assertEqual(main(['--vault', 'V', 'script', 'plan.md', '--revision', 'before',
                                   '--input', str(Path(directory) / 'missing.js')]), 1)
            client.assert_not_called()
            failure = json.loads(errors.getvalue())['error']
            self.assertEqual((failure['code'], failure['outcome']), ('INVALID_INPUT', 'not_applied'))

    def test_compact_and_full_edit_requests(self):
        for command, source in (('batch', '[]'), ('script', ';')):
            for full in (False, True):
                with self.subTest(command=command, full=full), patch('obsidian_tldraw_bridge.cli.Client') as client:
                    client.return_value.call.return_value = {'path': 'plan.md', 'revision': 'next', 'changes': {'added': 0, 'updated': 0, 'removed': 0}}
                    argv = ['--vault', 'Documents', command, 'plan.md', '--revision', 'before', '--input', '-']
                    if full:
                        argv.append('--full')
                    output = io.StringIO()
                    with patch('sys.stdin', io.StringIO(source)), contextlib.redirect_stdout(output):
                        self.assertEqual(main(argv), 0)
                    expected = {'path': 'plan.md', 'revision': 'before'}
                    expected['operations' if command == 'batch' else 'code'] = [] if command == 'batch' else source
                    if full:
                        expected['full'] = True
                    client.return_value.call.assert_called_once_with(command, expected, None)
                    self.assertIn('changes', json.loads(output.getvalue()))


class FreehandCommandTest(unittest.TestCase):
    def test_curve_definitions_use_existing_revision_and_request_id_contract(self):
        source = json.dumps({'strokes': [{'id': 'shape:curve', 'part': 'detail', 'path': 'M0 0 Q10 20 20 0'}]})
        with patch('obsidian_tldraw_bridge.cli.Client') as client:
            client.return_value.call.return_value = {'revision': 'after'}
            with patch('sys.stdin', io.StringIO(source)), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main(['--vault', 'V', '--request-id', 'draw-curve', 'freehand',
                                       'plan.md', '--revision', 'before', '--input', '-', '--full']), 0)
            action, args, identity = client.return_value.call.call_args.args
            self.assertEqual((action, identity), ('script', 'draw-curve'))
            self.assertEqual(args['revision'], 'before')
            self.assertTrue(args['full'])
            self.assertIsInstance(args['code'], str)

    def test_invalid_curves_fail_before_connecting(self):
        with patch('obsidian_tldraw_bridge.cli.Client') as client:
            with patch('sys.stdin', io.StringIO('{"strokes": []}')), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(main(['--vault', 'V', 'freehand', 'plan.md',
                                       '--revision', 'before', '--input', '-']), 1)
            client.assert_not_called()


class PreviewCommandTest(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix='bridge preview ')
        self.addCleanup(directory.cleanup)
        self.crop = str(Path(directory.name) / 'crop.png')
        self.detail = str(Path(directory.name) / 'detail.png')

    def test_context_bounds_are_forwarded(self):
        with patch('obsidian_tldraw_bridge.cli.Client') as client:
            client.return_value.call.return_value = {'path': self.crop}
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main(['--vault', 'V', 'preview', 'plan.md', '--bounds',
                                       '-10', '20', '200', '150', '--output', self.crop]), 0)
            self.assertEqual(client.return_value.call.call_args.args[1]['output'], str(Path(self.crop).resolve()))
            self.assertEqual(client.return_value.call.call_args.args[1]['bounds'],
                             {'x': -10, 'y': 20, 'w': 200, 'h': 150})

    def test_invalid_bounds_fail_before_connecting(self):
        for bounds in [('nan', '0', '20', '20'), ('0', 'inf', '20', '20'),
                       ('0', '0', '0', '20'), ('0', '0', '20', '-1')]:
            with self.subTest(bounds=bounds), patch('obsidian_tldraw_bridge.cli.Client') as client:
                with contextlib.redirect_stderr(io.StringIO()):
                    self.assertEqual(main(['--vault', 'V', 'preview', 'plan.md', '--bounds',
                                           *bounds, '--output', self.crop]), 1)
                client.assert_not_called()

    def test_part_and_scale_are_forwarded(self):
        with patch('obsidian_tldraw_bridge.cli.Client') as client:
            client.return_value.call.return_value = {'path': self.detail}
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main(['--vault', 'V', 'preview', 'plan.md', '--part', 'detail',
                                       '--scale', '3', '--output', self.detail]), 0)
            args = client.return_value.call.call_args.args[1]
            self.assertEqual(args['output'], str(Path(self.detail).resolve()))
            self.assertEqual(args['part'], 'detail')
            self.assertEqual(args['scale'], 3)

    def test_invalid_scale_fails_before_connecting(self):
        for scale in ('nan', 'inf', '0', '-1', '5'):
            with self.subTest(scale=scale), patch('obsidian_tldraw_bridge.cli.Client') as client:
                with contextlib.redirect_stderr(io.StringIO()):
                    self.assertEqual(main(['--vault', 'V', 'preview', 'plan.md', '--scale', scale,
                                           '--output', self.detail]), 1)
                client.assert_not_called()


if __name__ == '__main__':
    unittest.main()
