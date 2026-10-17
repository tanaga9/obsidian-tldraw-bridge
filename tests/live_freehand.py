"""Opt-in freehand edit/detail-preview check on an existing dedicated test note."""
import argparse
import json
from pathlib import Path
import sys
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from obsidian_tldraw_bridge.freehand import compile_script
from obsidian_tldraw_bridge.obsidian import BridgeError, Client

p = argparse.ArgumentParser()
p.add_argument('--vault', required=True)
p.add_argument('--path', required=True, help='Existing dedicated test diagram')
p.add_argument('--output', default='/tmp/freehand-live-detail.png')
a = p.parse_args()
c = Client(a.vault)
key = uuid.uuid4().hex
frame = 'shape:freehand-frame-' + key
curve = 'shape:freehand-curve-' + key
outline = 'shape:freehand-outline-' + key
part = 'detail-' + key
receipts = []
base = {'path': a.path}
c.call('open', base)


def state():
    return c.call('state', base)


def edit(code, revision=None, identity=None):
    if identity:
        receipts.append(identity)
    return c.call('script', {**base, 'revision': revision or state()['revision'], 'code': code}, identity)


try:
    before = state()
    c.call('batch', {**base, 'revision': before['revision'], 'operations': [
        {'method': 'createShapes', 'args': [[{'id': frame, 'type': 'frame',
          'x': 2000, 'y': 2000, 'props': {'w': 300, 'h': 300, 'name': 'Freehand test'}}]]},
    ]})
    code = compile_script({'strokes': [
        {'id': curve, 'parentId': frame, 'part': part, 'path': 'M40 80 Q80 40 120 80'},
        {'id': outline, 'parentId': frame, 'part': 'outline-' + key,
         'path': 'M20 60 C20 0 180 0 180 60 Z', 'color': 'light-blue', 'fill': 'fill', 'opacity': .4},
    ]})
    initial = state()
    identity = 'freehand-live-' + key
    result = edit(code, initial['revision'], identity)
    assert result['persistence']['saved'] and result['changes']['added'] == 2
    assert edit(code, initial['revision'], identity) == result
    first = {r['id']: r for r in state()['records']}
    assert first[outline]['props']['fill'] == 'fill'
    assert first[outline]['opacity'] == .4
    revised = compile_script({'strokes': [
        {'id': curve, 'part': part, 'path': 'M40 80 Q80 60 120 80', 'scale': .5},
    ]})
    changed = edit(revised)
    assert changed['changes'] == {'added': 0, 'updated': 1, 'removed': 0}
    current = state()
    records = {r['id']: r for r in current['records']}
    assert records[outline] == first[outline]
    assert records[curve]['parentId'] == frame
    assert records[curve]['props']['scale'] == .5
    try:
        edit(revised, initial['revision'])
        raise AssertionError('Stale revision accepted')
    except BridgeError as error:
        assert 'Revision conflict' in str(error)
    invalid = compile_script({'strokes': [
        {'id': 'shape:must-not-exist-' + key, 'path': 'M0 0 L20 20'},
        {'id': frame, 'path': 'M0 0 L20 20'},
    ]})
    try:
        edit(invalid)
        raise AssertionError('Non-draw target accepted')
    except BridgeError as error:
        assert 'non-draw shape' in str(error)
    assert state()['revision'] == current['revision']
    output = str(Path(a.output).resolve())
    preview = c.call('preview', {**base, 'part': part, 'scale': 3, 'output': output})
    assert Path(output).read_bytes().startswith(b'\x89PNG')
    assert preview['revision'] == current['revision']
    context_output = str(Path(output).with_name(Path(output).stem + '-context.png'))
    context = c.call('preview', {**base, 'bounds': {'x': 2020, 'y': 2020, 'w': 160, 'h': 100},
                                 'scale': 2, 'output': context_output})
    assert Path(context_output).read_bytes().startswith(b'\x89PNG')
    assert (context['width'], context['height']) == (320, 200)
    assert state()['revision'] == current['revision']
    print(json.dumps({'passed': ['native-curves', 'persistence', 'request-replay', 'targeted-redraw',
                                  'unrelated-stroke-preserved', 'stale-revision-rejection',
                                  'invalid-target-no-edits', 'part-preview', 'fill-and-opacity',
                                  'context-crop-no-document-change'], 'preview': preview, 'context': context}))
finally:
    current = state()
    if any(r['id'] == frame for r in current['records']):
        c.call('batch', {**base, 'revision': current['revision'], 'operations': [
            {'method': 'deleteShapes', 'args': [[frame]]},
        ]})
    c.call('close', base)
    for identity in set(receipts):
        c.forget(identity)
