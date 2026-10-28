"""Opt-in runtime reload check on a dedicated diagram; leaves document records unchanged."""
import argparse
from contextlib import contextmanager
import json
from pathlib import Path
import sys
import tempfile
import shutil
import time
import uuid
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from obsidian_tldraw_bridge.obsidian import Client, BridgeError

p = argparse.ArgumentParser()
p.add_argument('--vault', required=True)
p.add_argument('--path', required=True)
p.add_argument('--multi-page-copy', action='store_true', help='Test page preservation on a temporary diagram copy')
a = p.parse_args()
c = Client(a.vault)
source = Path(c.module).read_text(encoding="utf-8")
loader_source = Path(c.module).with_name('loader.cjs')

pending = None
completed_ids = set()


@contextmanager
def runtime_directory():
    directory = Path(tempfile.mkdtemp(prefix='bridge-live-reload-'))
    try:
        yield directory
    except BaseException:
        print('Test failed; runtime and recovery files retained: ' + str(directory),
              file=sys.stderr, flush=True)
        raise
    else:
        shutil.rmtree(directory)


def call(action, args=None, request_id=None):
    global pending
    request_id = request_id or 'reload-' + uuid.uuid4().hex
    pending = {'kind': 'request', 'requestId': request_id, 'action': action, 'args': args}
    (directory / 'pending.json').write_text(json.dumps(pending), encoding='utf-8')
    try:
        result = c.call(action, args, request_id)
    except BridgeError as error:
        if error.outcome != 'unknown':
            pending = None
        raise
    pending = None
    completed_ids.add(request_id)
    (directory / 'pending.json').unlink()
    return result


def vault_task(code):
    global pending
    key = 'bridge-live-reload-' + uuid.uuid4().hex
    slot = 'app[' + json.dumps(key) + ']'
    pending = {'kind': 'evaluation', 'slot': key, 'code': code}
    (directory / 'pending.json').write_text(json.dumps(pending), encoding='utf-8')
    c.evaluate(f"(()=>{{{slot}={{status:'running'}}; Promise.resolve().then(async()=>{{{code}; {slot}={{status:'complete'}}}}).catch(e=>{slot}={{status:'failed',error:String(e)}});}})()", True)
    for _ in range(100):
        status = c.evaluate(f'JSON.stringify({slot})')
        if status['status'] != 'running':
            pending = None
            if status['status'] == 'failed':
                raise RuntimeError(status['error'])
            (directory / 'pending.json').unlink()
            return
        time.sleep(.1)
    raise RuntimeError('Vault operation timed out; inspect evaluation slot ' + key)


with runtime_directory() as directory:
    runtime = Path(directory) / 'bridge.cjs'
    # Test the loader on disk even when Obsidian has cached an older loader.
    loader = Path(directory) / 'loader.cjs'
    shutil.copy(loader_source, loader)
    c._runtime = lambda: (f'require({json.dumps(str(loader))})', json.dumps(c.module))
    def write(version):
        runtime.write_text(source.replace('return {vault: app.vault.getName(),',
            'return {runtimeTestVersion: ' + str(version) + ', vault: app.vault.getName(),'), encoding='utf-8')
    write(1)
    c.module = str(runtime)
    copied_path = 'Codex Bridge Reload ' + uuid.uuid4().hex + '.md' if a.multi_page_copy else None
    args = {'path': copied_path or a.path}
    (directory / 'manifest.json').write_text(json.dumps({
        'vault': a.vault, 'sourcePath': a.path, 'testPath': args['path'],
        'copiedPath': copied_path, 'runtime': str(runtime), 'loader': str(loader),
    }), encoding='utf-8')
    test_page = 'page:reload-' + uuid.uuid4().hex
    try:
        if copied_path:
            vault_task('await app.vault.create(' + json.dumps(copied_path) + ', await app.vault.read(app.vault.getAbstractFileByPath(' + json.dumps(a.path) + ')))')
        before = call('open', args)
        if copied_path:
            before = call('script', args | {'full': True,
                'revision': before['revision'],
                'code': 'editor.createPage({id:' + json.dumps(test_page) + ',name:"Reload second page"});editor.setCurrentPage(' + json.dumps(test_page) + ');',
            })
        assert call('doctor')['runtimeTestVersion'] == 1
        request_id = 'reload-receipt-test'
        first = call('state', args, request_id)
        write(2)
        pending_status = call('doctor')
        assert pending_status['runtimeTestVersion'] == 1
        assert pending_status['pendingUpdate'] == {'reason': 'open_sessions', 'documents': [args['path']]}
        after = call('state', args)
        assert after['records'] == before['records']
        assert after['revision'] == before['revision']
        assert after['currentPageId'] == before['currentPageId']
        assert call('state', args, request_id) == first
        # The pending update leaves the existing Editor and selected page intact.
        checked = call('script', args | {'revision': after['revision'], 'code': 'editor.getTextOptions();'})
        assert checked['revision'] == before['revision']
        assert checked['persistence']['saved']
        if copied_path:
            shape_id = 'shape:reload-' + uuid.uuid4().hex
            edited = call('batch', args | {'full': True,'revision': after['revision'], 'operations': [
                {'method': 'createShapes', 'args': [[{'id': shape_id, 'type': 'geo', 'props': {'w': 80, 'h': 60}}]]},
            ]})
            assert next(r for r in edited['records'] if r['id'] == shape_id)['parentId'] == test_page
        call('close', args)
        updated = call('doctor')
        assert updated['runtimeTestVersion'] == 2 and updated['pendingUpdate'] is None
        reopened = call('open', dict(args, currentPageId=before['currentPageId']))
        expected = edited if copied_path else before
        assert reopened['records'] == expected['records']
        assert reopened['revision'] == expected['revision']
        assert reopened['currentPageId'] == before['currentPageId']
        assert call('state', args, request_id) == first
    finally:
        if pending is not None:
            # A timed-out open/edit/evaluation may still run. Keep its receipt
            # or slot and runtime files; do not race it with cleanup requests.
            print('Cleanup stopped: inspect pending.json before continuing.',
                  file=sys.stderr, flush=True)
        else:
            if args['path'] in call('doctor')['documents']:
                call('close', args)
            if copied_path:
                vault_task('const file=app.vault.getAbstractFileByPath(' + json.dumps(copied_path) + '); if(file) await app.vault.delete(file)')
            for completed_id in completed_ids:
                c.forget(completed_id)

    print(json.dumps({'updateDeferred': True, 'explicitCloseThenReload': True,
                          'recordsPreserved': True, 'receiptPreserved': True,
                          'selectedPagePreservedWhilePending': True, 'editOnSelectedPage': bool(copied_path)}))
