"""Opt-in saved-edit/export/replay check using a disposable note and isolated runtime."""
import argparse
import contextlib
import hashlib
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


def run(vault, output):
    client = Client(vault)
    identity = uuid.uuid4().hex
    note = 'workspace/drawings/apply-preview-' + identity + '.md'
    request_ids = []
    created = False
    output = str(Path(output).resolve())
    with tempfile.TemporaryDirectory(prefix='bridge-live-apply-preview-') as directory:
        runtime = Path(directory) / 'bridge.cjs'
        loader = Path(directory) / 'loader.cjs'
        shutil.copy(client.module, runtime)
        shutil.copy(Path(client.module).with_name('loader.cjs'), loader)
        client.module = str(runtime)
        client._runtime = lambda: (f'require({json.dumps(str(loader))})', json.dumps(str(runtime)))
        bridge = Bridge(vault, client_factory=lambda *args: client)
        args = {'path': note}

        def apply(operations, preview, request_id):
            observed = bridge.call('observe', args)
            edit = dict(args, revision=observed['revision'], pageId=observed['currentPageId'],
                        operations=operations, preview=preview)
            request_ids.append(request_id)
            result = bridge.call('apply', edit, request_id)
            assert result['revision'] == result['preview']['revision'] == result['persistence']['revision']
            assert result['persistence']['saved']
            assert result['preview']['sha256'] == hashlib.sha256(Path(output).read_bytes()).hexdigest()
            assert bridge.call('apply', edit, request_id) == result
            assert bridge.status(request_id)['result'] == result
            return result

        def rich(text):
            return {'type': 'doc', 'content': [{'type': 'paragraph', 'content': [{'type': 'text', 'text': text}]}]}

        try:
            # doctor checks the explicitly selected vault before any mutation.
            assert bridge.call('doctor')['supported']
            bridge.call('create', args)
            created = True
            nodes = [{'id': 'shape:' + name, 'type': 'geo', 'x': x, 'y': 100,
                      'props': {'w': 220, 'h': 100, 'font': 'sans', 'size': 'm',
                                'align': 'start', 'richText': rich(name.title())}}
                     for name, x in [('client', 60), ('service', 440)]]
            arrow = {'id': 'shape:request', 'type': 'arrow', 'x': 280, 'y': 150,
                     'props': {'start': {'x': 0, 'y': 0}, 'end': {'x': 160, 'y': 0},
                               'dash': 'solid', 'arrowheadEnd': 'arrow'}}
            bindings = [{'id': 'binding:' + terminal, 'type': 'arrow', 'fromId': 'shape:request',
                         'toId': 'shape:' + target, 'props': {'terminal': terminal,
                         'normalizedAnchor': {'x': x, 'y': .5}, 'isExact': False, 'isPrecise': True}}
                        for terminal, target, x in [('start', 'client', 1), ('end', 'service', 0)]]
            preview = {'output': output}
            apply([{'op': 'createShapes', 'shapes': nodes + [arrow]},
                   {'op': 'createBindings', 'bindings': bindings}], preview, 'setup-' + identity)
            baseline = bridge.call('state', args)
            protected = {r['id']: r for r in baseline['records'] if r['id'] == 'shape:service' or r['typeName'] == 'binding'}
            client_text = next(r for r in baseline['records'] if r['id'] == 'shape:client')['props']['richText']

            # Repeated local edits exercise whole-page, bounds and ID exports.
            for index, props in enumerate([{'color': 'blue'}, {'w': 250}, {'color': 'black'}]):
                options = dict(preview)
                if index == 1:
                    options['bounds'] = {'x': 20, 'y': 60, 'w': 700, 'h': 200}
                if index == 2:
                    options['ids'] = ['shape:client', 'shape:request', 'shape:service']
                result = apply([{'op': 'updateShapes', 'shapes': [
                    {'id': 'shape:client', 'type': 'geo', 'props': props}]}], options, f'edit-{index}-{identity}')
                current = {r['id']: r for r in bridge.call('state', args)['records']}
                assert all(current[key] == value for key, value in protected.items())
                assert current['shape:client']['props']['richText'] == client_text
                assert result['revision'] == bridge.call('saved', args)['revision']

            # The standalone exporter must produce the same pixels at this revision.
            standalone = str(Path(directory) / 'standalone.webp')
            receipt = bridge.call('preview', dict(args, output=standalone, revision=result['revision']))
            assert Path(standalone).read_bytes() == Path(output).read_bytes()
            assert receipt['revision'] == result['revision']

            observed = bridge.call('observe', args)
            edit = dict(args, revision=observed['revision'], operations=[{'op': 'updateShapes', 'shapes': [
                {'id': 'shape:client', 'type': 'geo', 'props': {'color': 'blue'}}]}],
                preview={'output': output, 'ids': ['shape:missing']})
            failed_id = 'failed-' + identity
            request_ids.append(failed_id)
            try:
                bridge.call('apply', edit, failed_id)
                raise AssertionError('Missing post-edit selection was accepted')
            except BridgeError as error:
                assert error.code == 'EDIT_PREVIEW_FAILED' and error.outcome == 'applied', error.as_dict()
                assert error.details['result']['persistence']['saved']
            failed = bridge.status(failed_id)
            try:
                bridge.call('apply', edit, failed_id)
                raise AssertionError('Failed replay unexpectedly succeeded')
            except BridgeError:
                assert bridge.status(failed_id) == failed

            # Recover by exporting only, without reapplying the failed request.
            before = bridge.call('state', args)
            recovered = bridge.call('preview', dict(args, output=output, revision=before['revision']))
            assert recovered['revision'] == bridge.call('saved', args)['revision']
            assert bridge.call('state', args)['records'] == before['records']
            # Exercise the real CLI adapter on a new, independent edit.
            with patch('obsidian_tldraw_bridge.cli.Client', return_value=client), \
                    patch('sys.stdin', io.StringIO(json.dumps([{'op': 'updateShapes', 'shapes': [
                        {'id': 'shape:client', 'type': 'geo', 'props': {'color': 'black'}}]}]))), \
                    contextlib.redirect_stdout(io.StringIO()) as stdout:
                request_ids.append('cli-' + identity)
                assert main(['--vault', vault, '--request-id', request_ids[-1], 'apply', note,
                    '--revision', before['revision'], '--input', '-', '--preview-output', output]) == 0
                result = json.loads(stdout.getvalue())
            assert result['preview']['revision'] == result['persistence']['revision']
            print(json.dumps({'preview': output, 'passed': ['saved-revision-export', 'repeated-local-edits',
                'bindings-and-unrelated-node-preserved', 'whole-bounds-and-ID-exports', 'replay-and-status',
                'standalone-identical-bytes', 'applied-export-failure', 'failed-replay', 'live-CLI']}, indent=2))
        finally:
            if created:
                client.call('close', args)
                slot = 'app[' + json.dumps('apply-preview-cleanup-' + identity) + ']'
                client.evaluate('(()=>{' + slot + '={done:false};const file=app.vault.getAbstractFileByPath('
                    + json.dumps(note) + ');Promise.resolve(file?app.vault.delete(file):null).then(()=>{'
                    + slot + '={done:true}}).catch(e=>{' + slot + '={done:true,error:String(e)}});})()', True)
                try:
                    for _ in range(100):
                        status = client.evaluate('JSON.stringify(' + slot + ')')
                        if status['done']:
                            assert 'error' not in status, status
                            break
                        time.sleep(.1)
                    else:
                        raise AssertionError('Temporary note cleanup not confirmed: ' + note)
                finally:
                    client.evaluate('JSON.stringify(delete ' + slot + ')')
            for request_id in request_ids:
                client.forget(request_id)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--vault', required=True)
    parser.add_argument('--output', default=str(Path(tempfile.gettempdir()) / 'bridge-apply-preview.webp'))
    options = parser.parse_args()
    run(options.vault, options.output)
