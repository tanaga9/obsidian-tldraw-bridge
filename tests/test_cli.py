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


if __name__ == '__main__':
    unittest.main()
