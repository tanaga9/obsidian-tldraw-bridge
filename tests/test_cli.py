import contextlib
import io
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
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
    def test_context_bounds_are_forwarded(self):
        with patch('obsidian_tldraw_bridge.cli.Client') as client:
            client.return_value.call.return_value = {'path': '/tmp/crop.png'}
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main(['--vault', 'V', 'preview', 'plan.md', '--bounds',
                                       '-10', '20', '200', '150', '--output', '/tmp/crop.png']), 0)
            self.assertEqual(client.return_value.call.call_args.args[1]['bounds'],
                             {'x': -10, 'y': 20, 'w': 200, 'h': 150})

    def test_invalid_bounds_fail_before_connecting(self):
        for bounds in [('nan', '0', '20', '20'), ('0', 'inf', '20', '20'),
                       ('0', '0', '0', '20'), ('0', '0', '20', '-1')]:
            with self.subTest(bounds=bounds), patch('obsidian_tldraw_bridge.cli.Client') as client:
                with contextlib.redirect_stderr(io.StringIO()):
                    self.assertEqual(main(['--vault', 'V', 'preview', 'plan.md', '--bounds',
                                           *bounds, '--output', '/tmp/crop.png']), 1)
                client.assert_not_called()

    def test_part_and_scale_are_forwarded(self):
        with patch('obsidian_tldraw_bridge.cli.Client') as client:
            client.return_value.call.return_value = {'path': '/tmp/detail.png'}
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main(['--vault', 'V', 'preview', 'plan.md', '--part', 'detail',
                                       '--scale', '3', '--output', '/tmp/detail.png']), 0)
            args = client.return_value.call.call_args.args[1]
            self.assertEqual(args['part'], 'detail')
            self.assertEqual(args['scale'], 3)

    def test_invalid_scale_fails_before_connecting(self):
        for scale in ('nan', 'inf', '0', '-1', '5'):
            with self.subTest(scale=scale), patch('obsidian_tldraw_bridge.cli.Client') as client:
                with contextlib.redirect_stderr(io.StringIO()):
                    self.assertEqual(main(['--vault', 'V', 'preview', 'plan.md', '--scale', scale,
                                           '--output', '/tmp/detail.png']), 1)
                client.assert_not_called()


if __name__ == '__main__':
    unittest.main()
