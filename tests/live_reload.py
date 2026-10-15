"""Opt-in runtime reload check on a dedicated diagram; leaves document records unchanged."""
import argparse
import json
from pathlib import Path
import sys
import tempfile
import shutil
import time
import uuid
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from obsidian_tldraw_bridge.obsidian import Client

p = argparse.ArgumentParser()
p.add_argument('--vault', required=True)
p.add_argument('--path', required=True)
p.add_argument('--multi-page-copy', action='store_true', help='Test page preservation on a temporary diagram copy')
a = p.parse_args()
c = Client(a.vault)
source = Path(c.module).read_text()
loader_source = Path(c.module).with_name('loader.cjs')

def vault_task(code):
    key = 'bridge-live-reload-' + uuid.uuid4().hex
    slot = 'app[' + json.dumps(key) + ']'
    c.evaluate(f"(()=>{{{slot}={{status:'running'}}; Promise.resolve().then(async()=>{{{code}; {slot}={{status:'complete'}}}}).catch(e=>{slot}={{status:'failed',error:String(e)}});}})()", True)
    try:
        for _ in range(100):
            status = c.evaluate(f'JSON.stringify({slot})')
            if status['status'] == 'failed':
                raise RuntimeError(status['error'])
            if status['status'] == 'complete':
                return
            time.sleep(.1)
        raise RuntimeError('Vault operation timed out')
    finally:
        c.evaluate(f'JSON.stringify(delete {slot})')

with tempfile.TemporaryDirectory(prefix='bridge-live-reload-') as directory:
    runtime = Path(directory) / 'bridge.cjs'
    # Test the loader on disk even when Obsidian has cached an older loader.
    loader = Path(directory) / 'loader.cjs'
    shutil.copy(loader_source, loader)
    c._runtime = lambda: (f'require({json.dumps(str(loader))})', json.dumps(c.module))
    def write(version):
        runtime.write_text(source.replace('return {vault: app.vault.getName(),',
            'return {runtimeTestVersion: ' + str(version) + ', vault: app.vault.getName(),'))
    write(1)
    c.module = str(runtime)
    copied_path = 'Codex Bridge Reload ' + uuid.uuid4().hex + '.md' if a.multi_page_copy else None
    args = {'path': copied_path or a.path}
    test_page = 'page:reload-' + uuid.uuid4().hex
    try:
        if copied_path:
            vault_task('await app.vault.create(' + json.dumps(copied_path) + ', await app.vault.read(app.vault.getAbstractFileByPath(' + json.dumps(a.path) + ')))')
        before = c.call('open', args)
        if copied_path:
            before = c.call('script', args | {
                'revision': before['revision'],
                'code': 'editor.createPage({id:' + json.dumps(test_page) + ',name:"Reload second page"});editor.setCurrentPage(' + json.dumps(test_page) + ');',
            })
        assert c.call('doctor')['runtimeTestVersion'] == 1
        request_id = 'reload-receipt-test'
        first = c.call('state', args, request_id)
        write(2)
        assert c.call('doctor')['runtimeTestVersion'] == 2
        after = c.call('state', args)
        assert after['records'] == before['records']
        assert after['revision'] == before['revision']
        assert after['currentPageId'] == before['currentPageId']
        assert c.call('state', args, request_id) == first
        # Verify text initialization on the recreated real SDK Editor.
        checked = c.call('script', args | {'revision': after['revision'], 'code': 'editor.getTextOptions();'})
        assert checked['revision'] == before['revision']
        assert checked['persistence']['saved']
        if copied_path:
            shape_id = 'shape:reload-' + uuid.uuid4().hex
            edited = c.call('batch', args | {'revision': after['revision'], 'operations': [
                {'method': 'createShapes', 'args': [[{'id': shape_id, 'type': 'geo', 'props': {'w': 80, 'h': 60}}]]},
            ]})
            assert next(r for r in edited['records'] if r['id'] == shape_id)['parentId'] == test_page
        c.forget(request_id)
        print(json.dumps({'reloaded': True, 'recordsUnchanged': True, 'textOptions': True, 'receiptPreserved': True, 'selectedPagePreserved': True, 'editOnSelectedPage': bool(copied_path)}))
    finally:
        if args['path'] in c.call('doctor')['documents']:
            c.call('close', args)
        if copied_path:
            vault_task('const file=app.vault.getAbstractFileByPath(' + json.dumps(copied_path) + '); if(file) await app.vault.delete(file)')
