"""Opt-in transport test: creates and removes a temporary tldraw note."""
import argparse
import base64
import json
from pathlib import Path
import re
import subprocess
import sys
import time
import uuid
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from obsidian_tldraw_bridge.obsidian import BridgeError, Client

p = argparse.ArgumentParser()
p.add_argument('--vault', required=True)
p.add_argument('--obsidian', help='Explicit official CLI executable')
a = p.parse_args()
c = Client(a.vault, a.obsidian)
identity = uuid.uuid4().hex
requested = 'Bridge 転送試験 ' + identity + '.md'
actual = requested
shape_id = 'shape:transport-' + identity
create_id = 'transport-create-' + identity
edit_id = 'transport-script-' + identity
create_attempted = False
sources = []
lengths = []
run = c._run_cli


def invoke(argv, **kwargs):
    encoded = re.search(r"Buffer.from\('([^']+)','base64'\)", argv[-1]).group(1)
    sources.append(Path(base64.b64decode(encoded).decode('utf-8')))
    lengths.append(len(argv[-1]))
    assert lengths[-1] < 2000, 'Evaluation bootstrap unexpectedly large'
    return run(argv, **kwargs)


with patch('obsidian_tldraw_bridge.obsidian.Client._run_cli', side_effect=invoke):
    try:
        create_attempted = True
        opened = c.call('create', {'path': requested}, create_id)
        actual = opened['path']
        label = "日本語 🌿 / 引用符: \"double\" 'single'\nバックスラッシュ: \\path / 記号: $() `value`"
        padding = (label + '\n') * 2500
        rich_text = {'type': 'doc', 'content': [
            {'type': 'paragraph', 'content': [{'type': 'text', 'text': line}]} for line in label.split('\n')
        ]}
        applied = c.call('apply', {'path': actual, 'revision': opened['revision'], 'operations': [
            {'op': 'createShapes', 'shapes': [{'id': shape_id, 'type': 'geo',
                'meta': {'transportProbe': padding},
                'props': {'w': 900, 'h': 180, 'font': 'sans', 'richText': rich_text}}]}
        ]})
        assert applied['persistence']['saved']
        observed = c.call('observe', {'path': actual, 'ids': [shape_id]})
        assert observed['shapes'][0]['text'] == label
        state = c.call('state', {'path': actual})
        record = next(r for r in state['records'] if r['id'] == shape_id)
        assert record['meta']['transportProbe'] == padding
        code = '/*' + padding + '*/\neditor.updateShapes(' + json.dumps([
            {'id': shape_id, 'type': 'geo', 'props': {'color': 'blue'}}]) + ');'
        arguments = {'path': actual, 'revision': state['revision'], 'code': code}
        evaluate = c.evaluate
        lost = [False]
        def lose_dispatch_output(source, missing_ok=False):
            result = evaluate(source, missing_ok)
            if '.dispatch(app,' in source and not lost[0]:
                lost[0] = True
                return None
            return result
        c.evaluate = lose_dispatch_output
        try:
            edited = c.call('script', arguments, edit_id)
        finally:
            c.evaluate = evaluate
        assert lost[0] and edited['persistence']['saved']
        assert c.call('script', arguments, edit_id) == edited
        assert c.status(edit_id)['result'] == edited
        try:
            c.call('script', dict(arguments, code=code + ';'), edit_id)
            raise AssertionError('Changed request accepted under retained ID')
        except BridgeError as error:
            assert error.code == 'REQUEST_ID_REUSED' and error.outcome == 'not_applied'
        assert c.call('observe', {'path': actual, 'ids': [shape_id]})['shapes'][0]['props']['color'] == 'blue'
        print(json.dumps({'largeApply': True, 'scriptUtf8Bytes': len(code.encode('utf-8')),
                          'lostResponseRecovered': True, 'replayPreserved': True,
                          'changedRequestRejected': True, 'maxBootstrapCharacters': max(lengths)}))
    finally:
        # The chosen path is unique to this run. Close persistence before deletion.
        if actual in c.call('doctor')['documents']:
            c.call('close', {'path': actual})
        for request_id in (create_id, edit_id):
            c.forget(request_id)
        if create_attempted:
            c.evaluate('(async()=>{const file=app.vault.getAbstractFileByPath(' + json.dumps(actual) +
                       ');if(file)await app.vault.delete(file);})()', True)
            for _ in range(100):
                if not c.evaluate('JSON.stringify(!!app.vault.getAbstractFileByPath(' + json.dumps(actual) + '))'):
                    break
                time.sleep(.1)
            else:
                raise RuntimeError('Temporary note cleanup not confirmed: ' + actual)
        assert all(not path.exists() for path in sources), 'Consumed evaluation file remains'
        print('Temporary note, session and consumed evaluation files removed')
