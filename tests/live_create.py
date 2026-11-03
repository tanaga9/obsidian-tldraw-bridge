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
        edited = c.call('apply', {'path': created_path, 'revision': result['revision'], 'operations': [
            {'op': 'createShapes', 'shapes': [{'id': shape, 'type': 'geo', 'props': {'w': 120, 'h': 60, 'richText': {'type': 'doc', 'content': [{'type': 'paragraph', 'content': [{'type': 'text', 'text': 'API label'}]}]}}}]},
        ]})
        assert edited['persistence']['saved']
        assert 'records' not in edited
        assert edited['changes']['added'] == 1
        observed = c.call('observe', {'path': created_path, 'ids': [shape]})
        assert observed['revision'] == edited['revision']
        assert observed['shapes'][0]['id'] == shape
        assert observed['shapes'][0]['bounds']['w'] > 0
        assert observed['shapes'][0]['text'] == 'API label'
        capabilities = c.call('capabilities')
        assert capabilities['apiVersion'] == 1 and 'geo' in capabilities['shapeTypes']
        assert c.status(request_id)['result'] == result
        try:
            c.call('apply', {'path': created_path, 'revision': result['revision'],
                            'operations': [{'op': 'deleteShapes', 'ids': [shape]}]})
            raise AssertionError('Stale revision accepted')
        except BridgeError as error:
            assert error.code == 'REVISION_CONFLICT' and error.outcome == 'not_applied'
        # Position edits can use compact context, without loading native records.
        position = observed['shapes'][0]['localPosition']
        moved = c.call('apply', {'path': created_path, 'revision': observed['revision'],
            'pageId': observed['currentPageId'], 'operations': [{'op': 'updateShapes', 'shapes': [
                {'id': shape, 'type': 'geo', 'x': position['x'] + 25, 'y': position['y']}
            ]}]})
        assert moved['persistence']['saved']
        assert c.call('observe', {'path': created_path, 'ids': [shape]})['shapes'][0]['localPosition']['x'] == position['x'] + 25

        c.evaluate('(()=>{for(const leaf of app.workspace.getLeavesOfType("tldraw-view"))'
            '{if(leaf.view.file?.path===' + json.dumps(created_path) + ')leaf.detach();}})()', True)
        assert c.call('state', {'path': created_path})['guiViews'] == 0
        try:
            c.call('reveal', {'path': created_path, 'shapeId': 'shape:missing'})
            raise AssertionError('Reveal accepted a missing shape')
        except BridgeError as error:
            assert error.code == 'SHAPE_NOT_FOUND'
        assert c.call('state', {'path': created_path})['guiViews'] == 0

        # Reveal explicitly opens the diagram even if creation had no GUI.
        for _ in range(2):
            assert c.call('reveal', {'path': created_path, 'shapeId': shape}) == {
                'path': created_path, 'shapeId': shape, 'pageId': observed['currentPageId'], 'visibleBoundsInView': True,
            }
            visible = c.evaluate('JSON.stringify((()=>{'
                'const editor=app.plugins.getPlugin("tldraw").currTldrawEditor;'
                'const bounds=editor.getShapePageBounds(' + json.dumps(shape) + ');'
                'return {path:app.workspace.getActiveFile()?.path,'
                'visible:editor.getViewportPageBounds().contains(bounds)};})())')
            assert visible == {'path': created_path, 'visible': True}
        revealed = c.call('state', {'path': created_path})
        assert revealed['guiViews'] == 1
        assert revealed['revision'] == moved['revision']
        assert revealed['currentPageId'] == observed['currentPageId']

        camera = 'app.plugins.getPlugin("tldraw").currTldrawEditor'
        c.evaluate(camera + '.setCameraOptions({isLocked:true})', True)
        try:
            c.call('reveal', {'path': created_path, 'shapeId': shape})
            raise AssertionError('Reveal accepted a locked camera')
        except BridgeError as error:
            assert error.code == 'CAMERA_LOCKED' and error.outcome == 'unknown'
            assert error.details['revealProgress'] == {
                'path': created_path, 'shapeId': shape, 'stage': 'tab_active',
            }
        finally:
            c.evaluate(camera + '.setCameraOptions({isLocked:false})', True)

        # Real SDK notifications are deferred: mutate the GUI and dispatch in the
        # same eval turn, without an animation frame or sleep between them.
        for iteration in range(5):
            seen = c.call('observe', {'path': created_path, 'ids': [shape]})
            identity = 'pending-gui-' + uuid.uuid4().hex
            text = 'GUI change ' + str(iteration)
            rich = {'type': 'doc', 'content': [{'type': 'paragraph', 'content': [{'type': 'text', 'text': text}]}]}
            gui_change = {'id': shape, 'type': 'geo', 'props': {'richText': rich}}
            edit = {'path': created_path, 'revision': seen['revision'], 'operations': [
                {'op': 'updateShapes', 'shapes': [{'id': shape, 'type': 'geo', 'props': {'color': 'red'}}]}
            ]}
            runtime_loader, runtime_module = c._runtime()
            c.evaluate('(()=>{const editor=app.plugins.getPlugin("tldraw").currTldrawEditor;'
                'if(!editor || editor.isDisposed || !editor.getShape(' + json.dumps(shape) + ')) throw new Error("Fixture GUI Editor required");'
                'editor.updateShapes([' + json.dumps(gui_change) + ']);'
                + runtime_loader + '.dispatch(app,' + runtime_module + ',"apply",' + json.dumps(edit) + ',' + json.dumps(identity) + ');})()', True)
            try:
                for _ in range(100):
                    receipt = c.status(identity)
                    if receipt['status'] != 'running':
                        break
                    time.sleep(.05)
                else:
                    raise AssertionError('Conflict request did not finish')
                assert receipt['status'] == 'failed', receipt
                assert receipt['failure']['code'] == 'REVISION_CONFLICT', receipt
                assert receipt['failure']['outcome'] == 'not_applied'
            finally:
                c.forget(identity)
            observed = c.call('observe', {'path': created_path, 'ids': [shape]})
            assert observed['shapes'][0]['text'] == text
            assert observed['shapes'][0]['props']['color'] != 'red'
            assert c.call('saved', {'path': created_path})['saved']

        # Inject a GUI edit at the async persistence boundary. The edit may have
        # been applied already, but must not be reported as a saved success.
        hook_key = 'save-conflict-' + uuid.uuid4().hex
        during = {'id': shape, 'type': 'geo', 'props': {'color': 'green'}}
        c.evaluate('(()=>{const original=app.vault.read;app[' + json.dumps(hook_key) + ']=original;'
            'app.vault.read=function(file,...args){if(file.path===' + json.dumps(created_path) + '){'
            'app.vault.read=original;delete app[' + json.dumps(hook_key) + '];'
            'app.plugins.getPlugin("tldraw").currTldrawEditor.updateShapes([' + json.dumps(during) + ']);}'
            'return original.call(this,file,...args);};})()', True)
        save_id = 'save-conflict-' + uuid.uuid4().hex
        try:
            try:
                c.call('apply', {'path': created_path, 'revision': observed['revision'], 'operations': [
                    {'op': 'updateShapes', 'shapes': [{'id': shape, 'type': 'geo', 'props': {'color': 'red'}}]}
                ]}, save_id)
                raise AssertionError('Superseded edit reported as saved success')
            except BridgeError as error:
                assert error.code == 'SAVE_CONFLICT' and error.outcome == 'applied', error.as_dict()
                assert error.details['revision'] != error.details['actualRevision']
            assert c.status(save_id)['failure']['code'] == 'SAVE_CONFLICT'
        finally:
            c.evaluate('(()=>{const original=app[' + json.dumps(hook_key) + '];if(original){app.vault.read=original;delete app[' + json.dumps(hook_key) + '];}})()', True)
            c.forget(save_id)
        recovered = c.call('observe', {'path': created_path, 'ids': [shape]})
        assert recovered['shapes'][0]['props']['color'] == 'green'
        assert c.call('saved', {'path': created_path})['saved']
        current = c.call('state', {'path': created_path})
        assert next(r for r in current['records'] if r['id'] == shape)['parentId'] == result['currentPageId']
        # Saving arbitrary drawing text must not interpret String.replace patterns.
        literal = "Literal $& $' $1 日本語"
        edited = c.call('apply', {'path': created_path, 'revision': current['revision'], 'operations': [
            {'op': 'updateShapes', 'shapes': [{'id': shape, 'type': 'geo', 'props': {
                'richText': {'type': 'doc', 'content': [{'type': 'paragraph', 'content': [
                    {'type': 'text', 'text': literal}]}]}}}]}
        ]})
        assert edited['persistence']['saved']
        c.call('close', {'path': created_path})
        # Release the GUI Store too, so reopening reads the persisted Markdown.
        c.evaluate('(()=>{for(const leaf of app.workspace.getLeavesOfType("tldraw-view"))'
            '{if(leaf.view.file?.path===' + json.dumps(created_path) + ')leaf.detach();}})()', True)
        reopened = c.call('open', {'path': created_path})
        assert reopened['revision'] == edited['revision']
        assert c.call('observe', {'path': created_path, 'ids': [shape]})['shapes'][0]['text'] == literal
        assert c.call('saved', {'path': created_path})['saved']
        other_page = 'page:reveal-target'
        target = 'shape:reveal-target'
        clipped = 'shape:reveal-clipped'
        other = c.call('script', {'path': created_path, 'revision': reopened['revision'], 'code':
            'editor.createPage(' + json.dumps({'id': other_page, 'name': 'Reveal target'}) + ');'
            'editor.createShapes(' + json.dumps([{
                'id': target, 'type': 'frame', 'parentId': other_page, 'x': 1500, 'y': 1500,
                'props': {'w': 240, 'h': 160},
            }, {
                'id': clipped, 'type': 'geo', 'parentId': target, 'x': 210, 'y': 20,
                'props': {'w': 120, 'h': 60},
            }]) + ');',
        })
        assert c.call('reveal', {'path': created_path, 'shapeId': shape})['pageId'] == reopened['currentPageId']
        assert c.call('reveal', {'path': created_path, 'shapeId': target})['pageId'] == other_page
        gui = c.evaluate('JSON.stringify((()=>{'
            'const editor=app.plugins.getPlugin("tldraw").currTldrawEditor;'
            'return {pageId:editor.getCurrentPageId(),visible:editor.getViewportPageBounds()'
            '.contains(editor.getShapePageBounds(' + json.dumps(target) + '))};})())')
        assert gui == {'pageId': other_page, 'visible': True}
        after_reveal = c.call('state', {'path': created_path})
        assert after_reveal['currentPageId'] == reopened['currentPageId']
        assert after_reveal['revision'] == other['revision']
        assert c.call('reveal', {'path': created_path, 'shapeId': clipped}) == {
            'path': created_path, 'shapeId': clipped, 'pageId': other_page, 'visibleBoundsInView': True,
        }
        clipping = c.evaluate('JSON.stringify((()=>{const editor=' + camera + ';'
            'const id=' + json.dumps(clipped) + ';'
            'const visible=editor.getShapeMaskedPageBounds(id);'
            'return {clipped:visible.w<editor.getShapePageBounds(id).w,'
            'inView:editor.getViewportPageBounds().contains(visible)};})())')
        assert clipping == {'clipped': True, 'inView': True}
        oversized = c.call('apply', {'path': created_path, 'revision': after_reveal['revision'], 'operations': [
            {'op': 'updateShapes', 'shapes': [{'id': target, 'type': 'frame', 'props': {'w': 100000, 'h': 100000}}]},
        ]})
        assert c.call('reveal', {'path': created_path, 'shapeId': target}) == {
            'path': created_path, 'shapeId': target, 'pageId': other_page, 'visibleBoundsInView': False,
        }
        assert c.call('state', {'path': created_path})['revision'] == oversized['revision']
        print(json.dumps({'created': True, 'nestedFolder': True, 'emptyNote': True, 'editable': True, 'replayPreserved': True, 'existingRejected': True, 'namedApply': True, 'observation': True, 'structuredConflict': True, 'status': True, 'compactPositionEdit': True, 'deferredGuiConflicts': 5, 'saveConflict': True, 'literalTextSaveReopen': True, 'reveal': True, 'crossPageReveal': True, 'lockedCamera': True, 'oversizedReveal': True, 'clippedReveal': True}))
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
