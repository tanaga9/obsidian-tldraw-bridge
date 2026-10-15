"""Opt-in create/edit/replay check. Creates and removes its own temporary note and folder."""
import argparse
import json
from pathlib import Path
import shutil
import sys
import tempfile
import time
import uuid
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from obsidian_tldraw_bridge.obsidian import Client, BridgeError

p = argparse.ArgumentParser()
p.add_argument('--vault', required=True)
a = p.parse_args()
c = Client(a.vault)
identity = uuid.uuid4().hex
folder = 'Codex Bridge Create Test ' + identity
requested = folder + '/new-note.md'
created_path = requested
request_id = 'create-test-' + identity

with tempfile.TemporaryDirectory(prefix='bridge-live-create-') as directory:
    runtime = Path(directory) / 'bridge.cjs'
    loader = Path(directory) / 'loader.cjs'
    shutil.copy(c.module, runtime)
    shutil.copy(Path(c.module).with_name('loader.cjs'), loader)
    c.module = str(runtime)
    c._runtime = lambda: (f'require({json.dumps(str(loader))})', json.dumps(c.module))
    try:
        result = c.call('create', {'path': requested}, request_id)
        created_path = result['path']
        assert created_path == requested
        assert result['created'] and result['persistence']['saved']
        assert not any(r['typeName'] == 'shape' for r in result['records'])
        assert c.call('create', {'path': requested}, request_id) == result
        try:
            c.call('create', {'path': requested})
            raise AssertionError('Existing note was not rejected')
        except BridgeError as error:
            assert 'already exists' in str(error)
        shape = 'shape:create-' + identity
        edited = c.call('batch', {'path': created_path, 'revision': result['revision'], 'operations': [
            {'method': 'createShapes', 'args': [[{'id': shape, 'type': 'geo', 'props': {'w': 120, 'h': 60}}]]},
        ]})
        assert edited['persistence']['saved']
        assert 'records' not in edited
        assert edited['changes']['added'] == 1
        current = c.call('state', {'path': created_path})
        assert next(r for r in current['records'] if r['id'] == shape)['parentId'] == result['currentPageId']
        print(json.dumps({'created': True, 'nestedFolder': True, 'emptyNote': True, 'editable': True, 'replayPreserved': True, 'existingRejected': True}))
    finally:
        if created_path in c.call('doctor')['documents']:
            c.call('close', {'path': created_path})
        c.forget(request_id)
        key = 'create-test-cleanup-' + identity
        slot = 'app[' + json.dumps(key) + ']'
        code = ('const file=app.vault.getAbstractFileByPath(' + json.dumps(created_path) + '); if(file) await app.vault.delete(file);'
                'const folder=app.vault.getAbstractFileByPath(' + json.dumps(folder) + '); if(folder && folder.children?.length===0) await app.vault.delete(folder,true);')
        c.evaluate(f"(()=>{{{slot}={{status:'running'}}; Promise.resolve().then(async()=>{{{code}; {slot}={{status:'complete'}}}}).catch(e=>{slot}={{status:'failed',error:String(e)}});}})()", True)
        try:
            for _ in range(100):
                status = c.evaluate(f'JSON.stringify({slot})')
                if status['status'] == 'failed':
                    raise RuntimeError(status['error'])
                if status['status'] == 'complete':
                    print('Temporary note and folder removed; session closed')
                    break
                time.sleep(.1)
            else:
                raise RuntimeError('Temporary fixture cleanup not confirmed')
        finally:
            c.evaluate(f'JSON.stringify(delete {slot})')
