"""Vault discovery preserves registration identity and isolates unreadable files."""
import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from obsidian_tldraw_bridge.api import list_vaults
from obsidian_tldraw_bridge.cli import main
from obsidian_tldraw_bridge.obsidian import BridgeError


class VaultListTest(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        find = patch('obsidian_tldraw_bridge.vaults.find_cli', return_value='test-cli')
        self.find_cli = find.start()
        self.addCleanup(find.stop)
        runner = patch('obsidian_tldraw_bridge.obsidian.Client._run_cli')
        self.runner = runner.start()
        self.addCleanup(runner.stop)

    def vault(self, name, config_dir='.obsidian', installed=False, enabled=False):
        path = self.root / name
        config = path / config_dir
        config.mkdir(parents=True)
        (config / 'community-plugins.json').write_text(json.dumps(['tldraw'] if enabled else []), encoding='utf-8')
        if installed:
            plugin = config / 'plugins/tldraw'
            plugin.mkdir(parents=True)
            (plugin / 'manifest.json').write_text(json.dumps({'id': 'tldraw', 'version': '1.32.0'}), encoding='utf-8')
            (plugin / 'main.js').write_text('throw new Error("must not execute plugin code")', encoding='utf-8')
        return path

    def response(self, rows):
        # Duplicate names and Unicode line separators are valid registration data.
        self.runner.return_value = subprocess.CompletedProcess([], 0,
            ''.join(name + '\t' + str(path) + '\r\n' for name, path in rows).encode('utf-8'), b'')

    def test_lists_each_path_and_separates_installation_from_activation(self):
        a = self.vault('青\u2028😀 space', installed=True, enabled=True)
        b = self.vault('disabled', installed=True)
        c = self.vault('absent', enabled=True)
        self.response([('Same', a), ('Same', b), ('No plugin', c)])
        result = list_vaults(executable='override', timeout=2)
        self.find_cli.assert_called_once_with('override')
        self.runner.assert_called_once_with(['test-cli', 'vaults', 'verbose'], 2)
        vaults = result['vaults']
        self.assertEqual([v['path'] for v in vaults], [str(a), str(b), str(c)])
        self.assertEqual([v['tldraw']['status'] for v in vaults], ['installed', 'installed', 'not_installed'])
        self.assertEqual([v['tldraw']['enabled'] for v in vaults], [True, False, True])
        self.assertEqual(vaults[0]['tldraw']['version'], '1.32.0')
        self.assertEqual(vaults[0]['tldraw']['configDir'], str(a / '.obsidian'))

    def test_missing_vault_and_config_are_unknown_not_uninstalled(self):
        missing = self.root / 'missing'
        bare = self.root / 'bare'
        bare.mkdir()
        valid = self.vault('valid', installed=True)
        self.response([('missing', missing), ('bare', bare), ('valid', valid)])
        results = [v['tldraw'] for v in list_vaults()['vaults']]
        self.assertEqual([v['status'] for v in results], ['unknown', 'unknown', 'installed'])
        self.assertTrue(all(v['reason'] and v['enabled'] is None for v in results[:2]))

    def test_incomplete_and_corrupt_plugins_do_not_hide_activation_or_other_vaults(self):
        broken = self.vault('broken', installed=True, enabled=True)
        (broken / '.obsidian/plugins/tldraw/main.js').unlink()
        corrupt = self.vault('corrupt', installed=True)
        (corrupt / '.obsidian/plugins/tldraw/manifest.json').write_text('{bad', encoding='utf-8')
        self.response([('broken', broken), ('corrupt', corrupt)])
        results = [v['tldraw'] for v in list_vaults()['vaults']]
        self.assertEqual([v['status'] for v in results], ['incomplete', 'incomplete'])
        self.assertEqual([v['enabled'] for v in results], [True, False])

    def test_unreadable_plugin_is_unknown_and_unreadable_activation_does_not_hide_install(self):
        path = self.vault('vault', installed=True)
        self.response([('vault', path)])
        original = Path.read_text
        for filename in ('manifest.json', 'community-plugins.json'):
            def read(file, *args, **kwargs):
                if file.name == filename:
                    raise PermissionError('denied')
                return original(file, *args, **kwargs)
            with self.subTest(filename=filename), patch.object(Path, 'read_text', read):
                result = list_vaults()['vaults'][0]['tldraw']
                if filename == 'manifest.json':
                    self.assertEqual(result['status'], 'unknown')
                    self.assertIn('denied', result['reason'])
                else:
                    self.assertEqual(result['status'], 'installed')
                    self.assertIsNone(result['enabled'])
                    self.assertIn('denied', result['enabledReason'])

    def test_activation_missing_or_corrupt_is_distinct(self):
        path = self.vault('vault', installed=True)
        self.response([('vault', path)])
        activation = path / '.obsidian/community-plugins.json'
        activation.unlink()
        self.assertIs(list_vaults()['vaults'][0]['tldraw']['enabled'], False)
        for text in ('{broken', '{}', '[true]'):
            activation.write_text(text, encoding='utf-8')
            result = list_vaults()['vaults'][0]['tldraw']
            self.assertIsNone(result['enabled'])
            self.assertIn('enabledReason', result)
            self.assertEqual(result['status'], 'installed')

    def test_explicit_alternative_configuration_folder(self):
        path = self.vault('custom', config_dir='.custom', installed=True, enabled=True)
        self.response([('custom', path)])
        self.assertEqual(list_vaults()['vaults'][0]['tldraw']['status'], 'unknown')
        self.assertEqual(list_vaults(config_dir='.custom')['vaults'][0]['tldraw']['status'], 'installed')

    def test_invalid_configuration_and_timeout_fail_before_cli_discovery(self):
        for config in ('', '.', '..', '../other', '/absolute', 'x/y', 'x\\y', 'C:', None):
            with self.subTest(config=config), self.assertRaises(BridgeError):
                list_vaults(config_dir=config)
        for timeout in (0, -1, True, float('nan'), float('inf'), None):
            with self.subTest(timeout=timeout), self.assertRaises(BridgeError):
                list_vaults(timeout=timeout)
        self.find_cli.assert_not_called()
        self.runner.assert_not_called()

    def test_empty_registry_and_malformed_cli_output(self):
        self.response([])
        self.assertEqual(list_vaults()['vaults'], [])
        for stdout, stderr, code in [(b'Obsidian is not running', b'', 0),
                                     (b'Name\trelative/path\n', b'', 0),
                                     (b'Command line interface is not enabled', b'', 0),
                                     (b'', b'No connection', 0), (b'', b'error', 1),
                                     (b'\xff', b'', 0)]:
            self.runner.return_value = subprocess.CompletedProcess([], code, stdout, stderr)
            with self.subTest(stdout=stdout, stderr=stderr), self.assertRaises(BridgeError) as error:
                list_vaults()
            self.assertEqual(error.exception.outcome, 'not_applied')
            self.assertEqual(error.exception.code, 'VAULT_DISCOVERY_FAILED')
        for error in (OSError('not found'), subprocess.TimeoutExpired('test-cli', 1)):
            self.runner.side_effect = error
            with self.assertRaises(BridgeError):
                list_vaults()

    def test_cli_without_vault_uses_shared_api_and_preserves_output_failure(self):
        self.response([('vault', self.vault('vault', installed=True))])
        expected = list_vaults()
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(main(['vaults']), 0)
        self.assertEqual(json.loads(output.getvalue()), expected)
        class BrokenOutput(io.StringIO):
            def write(self, value):
                raise BrokenPipeError('closed')
        with contextlib.redirect_stdout(BrokenOutput()), contextlib.redirect_stderr(io.StringIO()) as errors:
            self.assertEqual(main(['vaults']), 1)
        error = json.loads(errors.getvalue())['error']
        self.assertEqual(error['code'], 'OUTPUT_FAILED')
        self.assertEqual(error['outcome'], 'not_applied')
        self.assertEqual(error['details']['result'], expected)

    def test_cli_requires_vault_for_document_operations_and_rejects_vault_on_listing(self):
        for argv in (['doctor'], ['--vault', 'V', 'vaults'], ['--request-id', 'x', 'vaults']):
            with self.subTest(argv=argv), contextlib.redirect_stderr(io.StringIO()) as errors:
                self.assertEqual(main(argv), 1)
            self.assertEqual(json.loads(errors.getvalue())['error']['code'], 'INVALID_INPUT')
        self.runner.assert_not_called()
