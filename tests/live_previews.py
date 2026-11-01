"""Opt-in CLI multi-page export check using a disposable note and runtime.

Failures retain a recovery manifest; success removes only the test note/session.
"""
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
from obsidian_tldraw_bridge.cli import main
from obsidian_tldraw_bridge.obsidian import Client


def run(vault):
    identity = uuid.uuid4().hex
    directory = Path(tempfile.mkdtemp(prefix='bridge-previews-'))
    note = 'workspace/drawings/preview-test-' + identity + '.md'
    client = Client(vault)
    runtime, loader = directory / 'bridge.cjs', directory / 'loader.cjs'
    shutil.copy(client.module, runtime)
    shutil.copy(Path(client.module).with_name('loader.cjs'), loader)
    client.module = str(runtime)
    client._runtime = lambda: (f'require({json.dumps(str(loader))})', json.dumps(str(runtime)))
    requests = []

    def cli(*arguments, expect_error=None, request_id=None):
        request = request_id or 'preview-' + uuid.uuid4().hex
        if request not in requests:
            requests.append(request)
        argv = ['--vault', vault, '--request-id', request, *arguments]
        (directory / 'manifest.json').write_text(json.dumps({'vault': vault, 'note': note,
            'runtime': str(runtime), 'loader': str(loader), 'requestId': request,
            'requestIds': requests, 'argv': argv}, indent=2), encoding='utf-8')
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch('obsidian_tldraw_bridge.cli.Client', return_value=client), \
                contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            status = main(argv)
        if expect_error:
            error = json.loads(stderr.getvalue())['error']
            assert status == 1 and error['code'] == expect_error, error
            return error
        assert status == 0, stderr.getvalue()
        return json.loads(stdout.getvalue())

    try:
        diagnostic = cli('doctor')
        assert diagnostic['supported']
        cli('create', note)
        before = cli('state', note)
        source = before['currentPageId']
        script = directory / 'fixture.js'
        script.write_text('''
const source = editor.getCurrentPageId();
editor.createPage({id:'page:second',name:'Second'});
const text = value => ({type:'doc',content:[{type:'paragraph',content:[{type:'text',text:value}]}]});
editor.createShapes([
 {id:'shape:first',type:'geo',parentId:source,props:{w:360,h:160,fill:'solid',color:'blue',font:'sans',richText:text('First page')}},
 {id:'shape:second',type:'geo',parentId:'page:second',props:{w:360,h:160,fill:'solid',color:'green',font:'sans',richText:text('Second page')}}
]);
''', encoding='utf-8')
        cli('script', note, '--revision', before['revision'], '--input', str(script))
        before = cli('state', note)
        shapes = cli('state', note, '--record-type', 'shape')
        assert shapes['revision'] == before['revision']
        assert shapes['records'] == [r for r in before['records'] if r['typeName'] == 'shape']
        single = cli('preview', note, '--revision', before['revision'], '--page-id', 'page:second',
                     '--output', str(directory / 'single.webp'))
        assert single['pageId'] == 'page:second'
        outputs = [{'pageId': source, 'output': str(directory / 'first.webp')},
                   {'pageId': 'page:second', 'ids': ['shape:second'], 'output': str(directory / 'second.webp')}]
        spec = directory / 'outputs.json'
        spec.write_text(json.dumps(outputs), encoding='utf-8')
        request_id = 'preview-many-' + identity
        argv = ('preview-many', note, '--revision', before['revision'], '--input', str(spec))
        batch = cli(*argv, request_id=request_id)
        assert batch['revision'] == before['revision'] == batch['persistence']['revision']
        assert batch['persistence']['saved']
        for output, receipt in zip(outputs, batch['previews']):
            assert receipt['pageId'] == output['pageId']
            assert receipt['revision'] == before['revision']
            assert hashlib.sha256(Path(receipt['path']).read_bytes()).hexdigest() == receipt['sha256']
        assert len({p['sha256'] for p in batch['previews']}) == 2
        assert single['sha256'] == batch['previews'][1]['sha256']
        assert cli(*argv, request_id=request_id) == batch
        invalid = [outputs[0], {**outputs[1], 'ids': ['shape:first']}]
        spec.write_text(json.dumps(invalid), encoding='utf-8')
        cli('preview-many', note, '--input', str(spec), expect_error='OPERATION_FAILED')
        for receipt in batch['previews']:
            assert hashlib.sha256(Path(receipt['path']).read_bytes()).hexdigest() == receipt['sha256']
        after = cli('state', note)
        assert after['currentPageId'] == source
        assert after['records'] == before['records'] and after['revision'] == before['revision']
        cli('close', note)
        client.evaluate('JSON.stringify((()=>{for(const leaf of app.workspace.getLeavesOfType("tldraw-view"))'
                        '{if(leaf.view.file?.path===' + json.dumps(note) + ')leaf.detach()}return true})())')
        slot = 'app[' + json.dumps('preview-cleanup-' + identity) + ']'
        client.evaluate('(()=>{' + slot + '={done:false};app.vault.delete(app.vault.getAbstractFileByPath('
                        + json.dumps(note) + ')).then(()=>{' + slot + '={done:true}}).catch(e=>{'
                        + slot + '={done:true,error:String(e)}})})()', True)
        for _ in range(100):
            cleanup = client.evaluate('JSON.stringify(' + slot + ')')
            if cleanup.get('done'):
                assert not cleanup.get('error'), cleanup
                break
            time.sleep(.05)
        else:
            raise AssertionError('Cleanup unconfirmed; inspect manifest')
        for request in requests:
            client.forget(request)
        print(json.dumps({'pluginVersion': diagnostic['pluginVersion'], 'previews': batch['previews'],
                          'checks': 'typed records, page restoration, saved revision, image hashes, replay, failure preservation, cleanup passed'}, indent=2))
    except BaseException:
        print('Retained evidence: ' + str(directory / 'manifest.json'), file=sys.stderr)
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--vault', required=True)
    run(parser.parse_args().vault)
