"""Read registered vaults and on-disk tldraw installation/configuration status."""
import json
from pathlib import Path
import stat
import subprocess
from .obsidian import BridgeError, Client, find_cli, validate_timeout


def _directory(path):
    return stat.S_ISDIR(path.stat().st_mode)


def _file(path):
    return stat.S_ISREG(path.stat().st_mode)


def _tldraw_status(vault_path, config_dir):
    config = vault_path / config_dir
    plugin = config / 'plugins' / 'tldraw'
    result = {'status': 'unknown', 'version': None, 'enabled': None,
              'configDir': str(config), 'source': 'filesystem'}
    try:
        if not _directory(vault_path) or not _directory(config):
            raise ValueError('Vault or configuration path is not a directory')
    except (OSError, ValueError) as error:
        result['reason'] = str(error)
        return result
    try:
        try:
            plugin_present = _directory(plugin)
        except FileNotFoundError:
            result['status'] = 'not_installed'
        else:
            if not plugin_present:
                raise ValueError('Plugin path is not a directory')
            manifest = json.loads((plugin / 'manifest.json').read_text(encoding='utf-8-sig'))
            if not isinstance(manifest, dict) or manifest.get('id') != 'tldraw':
                raise ValueError('Invalid tldraw manifest')
            version = manifest.get('version')
            if not isinstance(version, str) or not version.strip():
                raise ValueError('Missing plugin version')
            result['version'] = version
            if not _file(plugin / 'main.js'):
                raise ValueError('Plugin main.js is not a file')
            result['status'] = 'installed'
    except (FileNotFoundError, ValueError) as error:
        result.update(status='incomplete', reason=str(error))
    except OSError as error:
        result.update(status='unknown', reason=str(error))
    try:
        enabled = json.loads((config / 'community-plugins.json').read_text(encoding='utf-8-sig'))
        if not isinstance(enabled, list) or any(not isinstance(value, str) for value in enabled):
            raise ValueError('Expected an array of plugin IDs')
        result['enabled'] = 'tldraw' in enabled
    except FileNotFoundError:
        # No activation configuration has been saved in this config folder.
        result['enabled'] = False
    except (OSError, ValueError) as error:
        result['enabledReason'] = str(error)
    return result


def list_vaults(executable=None, timeout=30, config_dir='.obsidian'):
    """List known vaults without selecting or opening one; never load plugins.

    Installation and activation are filesystem observations in config_dir, not
    runtime support checks. Unknown/unreadable vaults do not hide other entries.
    """
    validate_timeout(timeout)
    if (not isinstance(config_dir, str) or not config_dir.strip() or
            config_dir in ('.', '..') or any(char in config_dir for char in '/\\') or
            any(ord(char) < 32 for char in config_dir) or ':' in config_dir):
        raise BridgeError('config_dir must be a vault-relative folder name',
                          code='INVALID_INPUT', outcome='not_applied')
    executable = find_cli(executable)
    try:
        response = Client._run_cli([executable, 'vaults', 'verbose'], timeout)
        stdout = response.stdout.decode('utf-8-sig')
        stderr = response.stderr.decode('utf-8-sig')
    except (OSError, UnicodeError, subprocess.TimeoutExpired) as error:
        raise BridgeError('Could not list Obsidian vaults: ' + str(error),
                          code='VAULT_DISCOVERY_FAILED', outcome='not_applied',
                          details={'stage': 'vaults'}) from error
    if (response.returncode or 'Command line interface is not enabled' in stdout + stderr
            or (not stdout.strip() and stderr.strip())):
        raise BridgeError('Could not list Obsidian vaults: ' + (stdout + stderr).strip(),
                          code='VAULT_DISCOVERY_FAILED', outcome='not_applied',
                          details={'stage': 'vaults'})
    vaults = []
    for line in stdout.split('\n'):
        line = line.removesuffix('\r')
        if not line:
            continue
        name, separator, path = line.partition('\t')
        if not separator or not name or not Path(path).is_absolute():
            raise BridgeError('Unexpected Obsidian vault list: ' + line,
                              code='VAULT_DISCOVERY_FAILED', outcome='not_applied',
                              details={'stage': 'vaults'})
        vaults.append({'name': name, 'path': path,
                       'tldraw': _tldraw_status(Path(path), config_dir)})
    return {'vaults': vaults, 'source': 'obsidian-cli vaults verbose'}
