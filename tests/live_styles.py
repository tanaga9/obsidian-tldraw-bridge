"""Opt-in real SDK style/result check, using its own note and isolated runtime."""
import argparse
import contextlib
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import time
import uuid
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from obsidian_tldraw_bridge.api import Bridge
from obsidian_tldraw_bridge.cli import main
from obsidian_tldraw_bridge.obsidian import Client, BridgeError


def run(vault):
    client = Client(vault)
    identity = uuid.uuid4().hex
    path = 'workspace/drawings/style-probe-' + identity + '.md'
    request_ids = []
    created = False
    with tempfile.TemporaryDirectory(prefix='bridge-live-styles-') as directory:
        runtime = Path(directory) / 'bridge.cjs'
        loader = Path(directory) / 'loader.cjs'
        shutil.copy(client.module, runtime)
        shutil.copy(Path(client.module).with_name('loader.cjs'), loader)
        client.module = str(runtime)
        client._runtime = lambda: (f'require({json.dumps(str(loader))})', json.dumps(str(runtime)))
        bridge = Bridge(vault, client_factory=lambda *args: client)
        args = {'path': path}

        def script(code, full=False, request_id=None):
            revision = client.call('state', args)['revision']
            if request_id:
                request_ids.append(request_id)
            return bridge.call('script', dict(args, revision=revision, code=code, full=full), request_id)

        def markdown():
            return client.evaluate('JSON.stringify(require("node:fs").readFileSync('
                'app.vault.adapter.getFullPath(' + json.dumps(path) + '),"utf8"))')

        try:
            request_ids.append('create-' + identity)
            bridge.call('create', args, request_ids[-1])
            created = True
            baseline = client.call('state', args)
            text = markdown()
            spec = bridge.call('style-spec', dict(args, shapeType='geo'))
            props = spec['properties']['value']
            assert props['fill']['values']['status'] == 'available', spec
            assert 'tint' not in props['fill']['values']['value']
            if spec['pluginVersion'] == '1.32.0':
                assert props['fill']['values']['value'] == ['none','semi','solid','pattern','fill','lined-fill']
            assert props['fill']['shapeDefault']['value'] == 'none'
            assert props['dash']['values']['status'] == 'available'
            assert client.call('state', args)['revision'] == baseline['revision']
            assert client.call('state', args)['records'] == baseline['records']
            assert markdown() == text

            script('const style=[...editor.styleProps.geo].find(([s,key])=>key==="fill")[0];'
                   'editor.setStyleForNextShapes(style,"solid");')
            changed = bridge.call('style-spec', dict(args, shapeType='geo'))['properties']['value']['fill']
            assert changed['shapeDefault']['value'] == 'none'
            assert changed['nextShapeStyle']['value'] == 'solid'
            assert markdown() == text

            # Exercise the actual CLI parser/output and Python API over live transport.
            for full in (False, True):
                request_id = 'result-' + str(full) + '-' + identity
                request_ids.append(request_id)
                code = 'return {value:42,text:"青😀"}'
                edit_args = dict(args, revision=baseline['revision'])
                if full:
                    edit_args['full'] = True
                edit_args['code'] = code
                argv = ['--vault', vault, '--request-id', request_id, 'script', path,
                        '--revision', baseline['revision'], '--input', '-']
                if full:
                    argv.append('--full')
                with patch('obsidian_tldraw_bridge.cli.Client', return_value=client), \
                        patch('sys.stdin', io.StringIO(code)), contextlib.redirect_stdout(io.StringIO()) as output:
                    assert main(argv) == 0
                result = json.loads(output.getvalue())
                assert result['scriptResult'] == {'hasValue': True, 'value': {'value': 42, 'text': '青😀'}}
                assert result['persistence']['saved']
                assert ('records' in result) == full
                assert bridge.call('script', edit_args, request_id) == result
                assert client.status(request_id)['result'] == result

            for code, expected in [('return null', {'hasValue': True, 'value': None}),
                                   (';', {'hasValue': False}),
                                   ('return "青".repeat(21844)+"aa"', None)]:
                result = script(code)
                if expected is not None:
                    assert result['scriptResult'] == expected
                else:
                    assert len(json.dumps(result['scriptResult']['value'], ensure_ascii=False).encode('utf-8')) == 65536

            for suffix, code, error_code in [('invalid', 'return {bad:1n}', 'SCRIPT_RESULT_INVALID'),
                                            ('large', 'return "a".repeat(65535)', 'SCRIPT_RESULT_TOO_LARGE')]:
                before = client.call('state', args)
                try:
                    script('editor.updateDocumentSettings({gridSize:999});' + code,
                           request_id=suffix + '-' + identity)
                    raise AssertionError('Invalid result accepted')
                except BridgeError as error:
                    assert error.code == error_code and error.outcome == 'unknown', error.as_dict()
                    assert error.details['storeRevision'] == before['revision']
                assert client.call('state', args)['records'] == before['records']
                assert client.call('saved', args)['saved']
                shared = client.evaluate('JSON.stringify(Object.values(app.plugins.getPlugin("tldraw")'
                    '.tlDataDocumentStoreManager.storesManager.storeGroupMap.get(' + json.dumps(path) + ')'
                    '.main.store.getStoreSnapshot().store).sort((a,b)=>a.id.localeCompare(b.id)))')
                assert shared == before['records'], 'Shared Store was not restored'
                assert markdown() == text

            edited = script('editor.updateDocumentSettings({gridSize:20});return {savedEdit:true}')
            assert edited['changes']['updated'] == 1
            assert edited['scriptResult']['value']['savedEdit']
            assert edited['persistence']['saved']
            print(json.dumps({'pluginVersion': spec['pluginVersion'], 'passed': [
                'installed-style-enums', 'separate-defaults', 'read-only-discovery',
                'live-CLI-and-Python-results', 'full-and-compact', 'replay-and-status',
                'null-and-undefined', 'UTF-8-size-boundary', 'invalid-result-shared-rollback',
                'saved-edit-with-result']}, ensure_ascii=False))
        finally:
            if created:
                client.call('close', args)
                slot = 'app[' + json.dumps('style-cleanup-' + identity) + ']'
                client.evaluate('(()=>{' + slot + '={done:false};const file=app.vault.getAbstractFileByPath('
                    + json.dumps(path) + ');Promise.resolve(file?app.vault.delete(file):null).then(()=>{'
                    + slot + '={done:true}}).catch(e=>{' + slot + '={done:true,error:String(e)}});})()', True)
                try:
                    for _ in range(100):
                        status = client.evaluate('JSON.stringify(' + slot + ')')
                        if status['done']:
                            assert 'error' not in status, status
                            break
                        time.sleep(.1)
                    else:
                        raise AssertionError('Temporary note cleanup not confirmed: ' + path)
                finally:
                    client.evaluate('JSON.stringify(delete ' + slot + ')')
            for request_id in request_ids:
                client.forget(request_id)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--vault', required=True)
    run(parser.parse_args().vault)
