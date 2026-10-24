"""Opt-in language workflow check; creates and removes only its own test Note."""
import argparse
import json
from pathlib import Path
import shutil
import sys
import tempfile
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from obsidian_tldraw_bridge.api import Bridge
from obsidian_tldraw_bridge.obsidian import Client, BridgeError


def run(vault):
    client = Client(vault)
    identity = uuid.uuid4().hex
    path = 'workspace/drawings/language-test-' + identity + '.md'
    created = False
    with tempfile.TemporaryDirectory(prefix='bridge-language-live-') as directory:
        runtime = Path(directory) / 'bridge.cjs'
        loader = Path(directory) / 'loader.cjs'
        shutil.copy(client.module, runtime)
        shutil.copy(Path(client.module).with_name('loader.cjs'), loader)
        client.module = str(runtime)
        client._runtime = lambda: (f'require({json.dumps(str(loader))})', json.dumps(str(runtime)))
        bridge = Bridge(vault, client_factory=lambda *args: client)
        args = {'path': path}

        def state():
            return bridge.call('state', args)

        def script(code):
            return bridge.call('script', dict(args, revision=state()['revision'], code=code))

        def report():
            return bridge.call('language-status', args)

        def target():
            return next(r for r in report()['diagrams'] if r['language'] == 'ja')

        try:
            bridge.call('create', args, 'create-language-' + identity)
            created = True
            result = script('''
const source = editor.getCurrentPageId();
editor.createPage({id:'page:ja',name:'日本語'});
const richText = text => ({type:'doc',content:[{type:'paragraph',content:[{type:'text',text}]}]});
editor.createShapes([
 {id:'shape:en',type:'geo',parentId:source,props:{richText:richText('Review')}},
 {id:'shape:ja',type:'geo',parentId:'page:ja',props:{richText:richText('確認')}}
]);
return {source};
''')
            source = result['scriptResult']['value']['source']
            # Exercise a valid ID that also exists on Object.prototype.
            checkpoint = {'diagramId': 'toString', 'editingSourcePageId': source,
                          'languages': {'en': source, 'ja': 'page:ja'}, 'targetLanguage': 'ja',
                          'kind': 'adopt', 'reason': 'Inspected both fixture labels', 'reviewed': True}
            before = state()
            request = dict(args, revision=before['revision'], checkpoint=checkpoint)
            request_id = 'adopt-language-' + identity
            adopted = bridge.call('language-checkpoint', request, request_id)
            assert adopted['persistence']['saved']
            assert bridge.call('language-checkpoint', request, request_id) == adopted
            current = state()
            shapes = lambda s: [r for r in s['records'] if r['typeName'] == 'shape']
            assert shapes(before) == shapes(current)
            assert target()['status'] == 'current'
            assert state()['revision'] == current['revision']
            assert state()['currentPageId'] == current['currentPageId']
            script("editor.updateShapes([{id:'shape:ja',type:'geo',x:80}]);")
            assert target()['status'] == 'presentation-review'
            layout = bridge.call('language-checkpoint', dict(args, revision=state()['revision'],
                checkpoint=dict(checkpoint, kind='layout', reason='Verified layout-only move')))
            assert layout['persistence']['saved']
            assert target()['status'] == 'current'
            script("editor.updateShapes([{id:'shape:ja',type:'geo',props:{richText:{type:'doc',content:[{type:'paragraph',content:[{type:'text',text:'変更'}]}]}}}]);")
            assert target()['status'] == 'target-content-changed'
            before_invalid = state()
            try:
                bridge.call('language-checkpoint', dict(args, revision=before_invalid['revision'],
                    checkpoint=dict(checkpoint, kind='layout', reason='Must reject content edit')))
                raise AssertionError('Layout checkpoint accepted text change')
            except BridgeError as error:
                assert 'Layout checkpoint cannot accept content changes' in str(error), error
            assert state()['records'] == before_invalid['records']
            assert bridge.call('saved', args)['saved']
            print(json.dumps({'checks': 'language status/checkpoint/replay/presentation/content/rollback/persistence passed',
                              'temporaryNote': path}))
        finally:
            if created:
                bridge.call('close', args)
                # Delete only the unique note created by this test.
                client.evaluate('app.vault.delete(app.vault.getAbstractFileByPath(' + json.dumps(path) + '))', True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--vault', required=True)
    run(parser.parse_args().vault)
