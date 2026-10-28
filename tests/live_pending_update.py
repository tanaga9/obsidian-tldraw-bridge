"""Opt-in deleted-session update-deferral check using isolated runtimes and temporary notes."""
import argparse
from contextlib import contextmanager
import json
from pathlib import Path
import shutil
import sys
import tempfile
import time
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from obsidian_tldraw_bridge.obsidian import Client, BridgeError


@contextmanager
def runtime_directory():
    directory = tempfile.mkdtemp(prefix='bridge-live-migration-')
    try:
        yield directory
    except BaseException:
        print('Test failed; runtime files retained for receipt/session recovery: ' + directory,
              file=sys.stderr, flush=True)
        raise
    else:
        print('Verification evidence: ' + directory, flush=True)


def run(vault):
    client = Client(vault, timeout=120)
    identity = uuid.uuid4().hex
    paths = ['Bridge migration ' + identity + suffix + '.md' for suffix in ('-deleted', '-healthy', '-new')]
    created = []
    original = None
    pending = None
    completed_ids = set()
    evidence = None
    update_written = False
    verified = False

    def call(action, args=None, request_id=None):
        nonlocal pending
        request_id = request_id or 'pending-update-' + uuid.uuid4().hex
        pending = request_id
        recovery_path = evidence / 'pending-request.json'
        recovery_path.write_text(json.dumps({
            'requestId': request_id, 'action': action, 'args': args,
        }), encoding='utf-8')
        print('Bridge request: ' + action + ' ' + (args or {}).get('path', ''), flush=True)
        try:
            result = client.call(action, args, request_id)
        except BridgeError as error:
            if error.outcome != 'unknown':
                pending = None
                completed_ids.add(request_id)
                recovery_path.unlink()
            raise
        pending = None
        completed_ids.add(request_id)
        recovery_path.unlink()
        print('Completed: ' + action, flush=True)
        return result

    def vault_task(code):
        nonlocal pending
        key = 'bridge-migration-' + uuid.uuid4().hex
        slot = 'app[' + json.dumps(key) + ']'
        pending = 'evaluation:' + key
        if evidence:
            (evidence / 'pending-evaluation.json').write_text(json.dumps({'slot': key, 'code': code}), encoding='utf-8')
        client.evaluate(f'(()=>{{{slot}={{status:"running"}}; Promise.resolve().then(async()=>{{{code}; {slot}={{status:"complete"}}}}).catch(e=>{slot}={{status:"failed",error:String(e)}});}})()', True)
        for _ in range(100):
            status = client.evaluate(f'JSON.stringify({slot})')
            if status['status'] != 'running':
                pending = None
                if status['status'] == 'failed':
                    raise RuntimeError(status['error'])
                return
            time.sleep(.1)
        raise RuntimeError('Vault operation timed out; inspect ' + key)

    def detach_test_tabs():
        # Only leaves for this run's UUID-named notes can be detached. No user
        # views or production sessions are closed, including other tldraw views.
        vault_task('for(const leaf of app.workspace.getLeavesOfType("tldraw-view")) '
                   'if(' + json.dumps(paths) + '.includes(leaf.view.file?.path)) leaf.detach()')

    def saved_edit(path, shape_id):
        observed = call('observe', {'path': path})
        result = call('apply', {'path': path, 'revision': observed['revision'],
            'pageId': observed['currentPageId'], 'operations': [{'op': 'createShapes', 'shapes': [
                {'id': shape_id, 'type': 'geo', 'x': 40, 'y': 40, 'props': {'w': 180, 'h': 100}},
            ]}]}, 'edit-' + shape_id)
        assert result['persistence']['saved']
        saved_state = call('state', {'path': path})
        assert result['revision'] == saved_state['revision']
        assert any(record['id'] == shape_id for record in saved_state['records'])
        return saved_state

    with runtime_directory() as directory:
        evidence = Path(directory)
        print('Verification directory: ' + directory, flush=True)
        runtime = Path(directory) / 'bridge.cjs'
        loader = Path(directory) / 'loader.cjs'
        shutil.copy(client.module, runtime)
        shutil.copy(Path(client.module).with_name('loader.cjs'), loader)
        source = runtime.read_text(encoding='utf-8')
        def write(version):
            runtime.write_text(source.replace('return {vault: app.vault.getName(),',
                'return {runtimeTestVersion: ' + str(version) + ', vault: app.vault.getName(),'), encoding='utf-8')
        write(1)
        client.module = str(runtime)
        client._runtime = lambda: (f'require({json.dumps(str(loader))})', json.dumps(str(runtime)))
        try:
            initial = call('doctor')
            assert not initial['documents'] and initial['runtimeTestVersion'] == 1, initial
            (evidence / 'manifest.json').write_text(json.dumps({'vault': vault, 'paths': paths}), encoding='utf-8')
            for path in paths[:2]:
                created.append(path)  # Includes a note retained after initialization failure.
                result = call('create', {'path': path}, 'create-' + path)
                assert result['path'] == path and result['persistence']['saved']
            print('Temporary sessions created; testing deletion and deferred update', flush=True)
            before = saved_edit(paths[0], 'shape:retained-' + identity)
            healthy_before = saved_edit(paths[1], 'shape:healthy-' + identity)
            original = client.evaluate('JSON.stringify(require("node:fs").readFileSync(app.vault.adapter.getFullPath('
                                       + json.dumps(paths[0]) + '),"utf8"))')
            (Path(directory) / 'recovery.json').write_text(json.dumps({
                'vault': vault, 'paths': paths, 'state': before, 'markdown': original,
            }, ensure_ascii=False), encoding='utf-8')
            detach_test_tabs()
            vault_task('await app.vault.delete(app.vault.getAbstractFileByPath(' + json.dumps(paths[0]) + '))')
            write(2)
            update_written = True
            status = call('doctor')
            (evidence / 'pending-update-doctor.json').write_text(json.dumps(status), encoding='utf-8')
            assert status['runtimeTestVersion'] == 1, status
            assert status['pendingUpdate'] == {'reason': 'open_sessions', 'documents': paths[:2]}, status
            after = call('state', {'path': paths[0]})
            assert (after['records'], after['revision'], after['currentPageId']) == (
                before['records'], before['revision'], before['currentPageId'])
            try:
                call('close', {'path': paths[0]})
                raise AssertionError('Missing-file session closed without persistence')
            except BridgeError as error:
                assert error.code == 'ENOENT', error.as_dict()
            assert call('doctor')['runtimeTestVersion'] == 1
            healthy = call('state', {'path': paths[1]})
            assert healthy['records'] == healthy_before['records']
            edited_healthy = saved_edit(paths[1], 'shape:after-migration-' + identity)
            assert call('saved', {'path': paths[1]})['revision'] == edited_healthy['revision']
            created.append(paths[2])
            call('create', {'path': paths[2]}, 'create-' + paths[2])
            new_state = saved_edit(paths[2], 'shape:new-' + identity)
            assert call('saved', {'path': paths[2]})['revision'] == new_state['revision']
            preview = call('preview', {'path': paths[2], 'revision': new_state['revision'],
                                       'output': str(evidence / 'new-note.webp')})
            assert preview['revision'] == new_state['revision']
            assert client.evaluate('JSON.stringify(app.vault.getAbstractFileByPath(' + json.dumps(paths[0]) + ')===null)')
            assert call('doctor')['runtimeTestVersion'] == 1
            verified = True
            print(json.dumps({'updateDeferred': True, 'recordsPreserved': True,
                              'unrelatedSaved': True, 'newNoteSaved': True, 'deletedFileNotRecreated': True}))
        finally:
            if pending:
                # Preserve the original interruption/error and do not race an
                # in-flight request or evaluation with cleanup.
                print('Cleanup stopped: inspect the recorded request or evaluation before continuing.',
                      file=sys.stderr, flush=True)
            else:
                # Restore only our own deleted test note so normal close can verify persistence.
                detach_test_tabs()
                if original is not None:
                    vault_task('if(!app.vault.getAbstractFileByPath(' + json.dumps(paths[0]) + ')) await app.vault.create('
                               + json.dumps(paths[0]) + ',' + json.dumps(original) + ')')
                status = call('doctor')
                for path in created:
                    if path in status['documents']:
                        call('close', {'path': path})
                    vault_task('const file=app.vault.getAbstractFileByPath(' + json.dumps(path)
                               + '); if(file) await app.vault.delete(file)')
                final = call('doctor')
                assert not final['documents'] and final['pendingUpdate'] is None, final
                assert final['runtimeTestVersion'] == (2 if update_written else 1), final
                assert client.evaluate('JSON.stringify(' + json.dumps(paths) + '.every(p=>app.vault.getAbstractFileByPath(p)===null))')
                (evidence / 'result.json').write_text(json.dumps({'passed': verified, 'temporaryNotesAndSessionsRemoved': True}), encoding='utf-8')
                print(json.dumps({'temporaryNotesAndSessionsRemoved': True}), flush=True)
                for completed_id in completed_ids:
                    client.forget(completed_id)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--vault', required=True)
    run(parser.parse_args().vault)
