"""Opt-in CLI rich-text and separate-arrow-label check on a disposable note.

Failures retain the note, isolated runtime, and request manifest for inspection;
never rerun an uncertain request as recovery. No existing note is edited.
"""
import argparse
import contextlib
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import uuid
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from obsidian_tldraw_bridge.cli import main
from obsidian_tldraw_bridge.obsidian import Client


def run(vault):
    identity = uuid.uuid4().hex
    directory = Path(tempfile.mkdtemp(prefix='bridge-rich-text-'))
    note = 'workspace/drawings/rich-text-' + identity + '.md'
    client = Client(vault)
    runtime = directory / 'bridge.cjs'
    loader = directory / 'loader.cjs'
    shutil.copy(client.module, runtime)
    shutil.copy(Path(client.module).with_name('loader.cjs'), loader)
    client.module = str(runtime)
    client._runtime = lambda: (f'require({json.dumps(str(loader))})', json.dumps(str(runtime)))
    requests = []

    def cli(*arguments, expect_error=None):
        request = 'rich-' + uuid.uuid4().hex
        requests.append(request)
        argv = ['--vault', vault, '--request-id', request, *arguments]
        (directory / 'manifest.json').write_text(json.dumps({'vault': vault, 'note': note,
            'runtime': str(runtime), 'loader': str(loader), 'requestId': request, 'requestIds': requests,
            'argv': argv}, indent=2), encoding='utf-8')
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

    def records():
        return {r['id']: r for r in cli('state', note)['records']}

    def revision():
        return cli('observe', note)['revision']

    def rich():
        return {'type': 'doc', 'content': [{'type': 'paragraph', 'content': [
            {'type': 'text', 'text': text}]} for text in ('Status: Ready / Ready', 'command()', 'Aside / Focus')]}

    def expected(highlight=True, bullet=True):
        def text(value, mark=None):
            return dict(type='text', text=value, **({'marks': [{'type': mark}]} if mark else {}))
        paragraphs = [{'type': 'paragraph', 'content': content} for content in [
            [text('Status: Ready / '), text('Ready', 'bold')], [text('command()', 'code')],
            [text('Aside', 'italic'), text(' / '), text('Focus', 'highlight' if highlight else None)]]]
        return {'type': 'doc', 'content': [{'type': 'bulletList', 'content': [
            {'type': 'listItem', 'content': [paragraph]} for paragraph in paragraphs]}] if bullet else paragraphs}

    def font_pixels(shape_id):
        result = cli('script', note, '--revision', revision(), '--input', str(font_script))
        return result['scriptResult']['value'][shape_id]

    font_script = directory / 'font-pixels.js'
    font_script.write_text('''
const result = {};
for (const id of ['shape:arrow', 'shape:arrow-label']) {
  const shape = editor.getShape(id);
  if (!shape) continue;
  const util = editor.getShapeUtil(shape), args = [editor, shape, editor.getCurrentTheme(), editor.getColorMode()];
  const style = {...util.options.getDefaultDisplayValues(...args), ...util.options.getCustomDisplayValues(...args)};
  result[id] = (shape.type === 'arrow' ? style.labelFontSize : style.fontSize) * shape.props.scale;
}
return result;
''', encoding='utf-8')

    try:
        diagnostic = cli('doctor')
        assert diagnostic['supported']
        cli('create', note)
        shapes = [
            {'id': 'shape:frame', 'type': 'frame', 'props': {'name': 'Text formatting', 'w': 1200, 'h': 850}},
            {'id': 'shape:text', 'type': 'text', 'parentId': 'shape:frame', 'x': 50, 'y': 80,
             'props': {'richText': rich(), 'font': 'sans', 'w': 470, 'autoSize': False}},
            {'id': 'shape:geo', 'type': 'geo', 'parentId': 'shape:frame', 'x': 630, 'y': 60,
             'props': {'richText': rich(), 'font': 'sans', 'w': 500, 'h': 270, 'align': 'start'}},
            {'id': 'shape:note', 'type': 'note', 'parentId': 'shape:frame', 'x': 50, 'y': 470,
             'props': {'richText': rich(), 'font': 'sans', 'size': 's'}},
            {'id': 'shape:arrow', 'type': 'arrow', 'parentId': 'shape:frame', 'x': 570, 'y': 700,
             'props': {'richText': rich(), 'font': 'sans', 'start': {'x': 0, 'y': 0}, 'end': {'x': 500, 'y': 0}}},
        ]
        for name, x in [('start', 510), ('end', 1070)]:
            shapes.append({'id': 'shape:' + name, 'type': 'geo', 'parentId': 'shape:frame', 'x': x, 'y': 670,
                           'props': {'w': 60, 'h': 60}})
        bindings = [{'id': 'binding:' + terminal, 'type': 'arrow', 'fromId': 'shape:arrow',
                     'toId': 'shape:' + terminal, 'props': {'terminal': terminal,
                     'normalizedAnchor': {'x': anchor, 'y': .5}, 'isExact': False, 'isPrecise': True}}
                    for terminal, anchor in [('start', 1), ('end', 0)]]
        source = directory / 'setup.json'
        source.write_text(json.dumps([{'op': 'createShapes', 'shapes': shapes},
                                      {'op': 'createBindings', 'bindings': bindings}]), encoding='utf-8')
        cli('apply', note, '--revision', revision(), '--input', str(source))
        baseline = records()
        for kind in ('text', 'geo', 'note', 'arrow'):
            target = 'shape:' + kind
            cli('format-text', note, '--revision', revision(), '--shape-id', target,
                '--text', 'Ready', '--bold', expect_error='TEXT_MATCH_FAILED')
            for phrase, flag, extra in [('Ready', '--bold', ['--occurrence', '2']),
                                        ('command()', '--code', []), ('Aside', '--italic', []),
                                        ('Focus', '--highlight', [])]:
                cli('format-text', note, '--revision', revision(), '--shape-id', target,
                    '--text', phrase, flag, *extra)
            cli('format-text', note, '--revision', revision(), '--shape-id', target, '--list', 'bullet')
            assert records()[target]['props']['richText'] == expected(), target
        cli('format-text', note, '--revision', revision(), '--shape-id', 'shape:text', '--list', 'none')
        assert records()['shape:text']['props']['richText'] == expected(bullet=False)
        cli('format-text', note, '--revision', revision(), '--shape-id', 'shape:text', '--list', 'bullet')
        # Remove only one mark and reapply it; list and other marks survive.
        cli('format-text', note, '--revision', revision(), '--shape-id', 'shape:text',
            '--text', 'Focus', '--no-highlight')
        assert records()['shape:text']['props']['richText'] == expected(highlight=False)
        cli('format-text', note, '--revision', revision(), '--shape-id', 'shape:text',
            '--text', 'Focus', '--highlight')
        before = records()
        assert all(before['shape:' + kind]['props']['richText'] == expected() for kind in ('text', 'geo', 'note', 'arrow'))
        original_font_pixels = font_pixels('shape:arrow')
        observed = cli('observe', note, '--ids', 'shape:geo', '--rich-text')
        assert observed['shapes'][0]['richText'] == before['shape:geo']['props']['richText']
        cli('preview', note, '--ids', 'shape:frame', '--scale', '.6', '--output', str(directory / 'before.webp'))
        source.write_text(json.dumps([{'op': 'separateArrowLabel', 'id': 'shape:arrow',
            'labelId': 'shape:arrow-label', 'x': 700, 'y': 550, 'width': 400}]), encoding='utf-8')
        result = cli('apply', note, '--revision', revision(), '--input', str(source), '--preview-output', str(directory / 'after.webp'),
                     '--preview-ids', 'shape:frame', '--preview-scale', '.6')
        assert result['revision'] == result['preview']['revision'] == result['persistence']['revision']
        assert result['persistence']['saved']
        assert client.status(requests[-1])['result'] == result
        after = records()
        assert abs(font_pixels('shape:arrow-label') - original_font_pixels) < 1e-8
        for key in ['binding:start', 'binding:end', 'shape:start', 'shape:end']:
            assert after[key] == baseline[key], key
        assert after['shape:arrow-label']['props']['richText'] == before['shape:arrow']['props']['richText']
        assert after['shape:arrow']['props'] == dict(before['shape:arrow']['props'], richText={
            'type': 'doc', 'content': [{'type': 'paragraph'}]})
        for kind in ('text', 'geo', 'note'):
            assert after['shape:' + kind] == before['shape:' + kind]
        cli('saved', note)
        # Release the disposable GUI Store as well, so reopening reads persisted data.
        cli('close', note)
        client.evaluate('JSON.stringify((()=>{for(const leaf of app.workspace.getLeavesOfType("tldraw-view"))'
                        '{if(leaf.view.file?.path===' + json.dumps(note) + ')leaf.detach()}return true})())')
        cli('open', note)
        assert records() == after
        cli('close', note)
        client.evaluate('JSON.stringify((()=>{for(const leaf of app.workspace.getLeavesOfType("tldraw-view"))'
                        '{if(leaf.view.file?.path===' + json.dumps(note) + ')leaf.detach()}return app.vault.getName()})())')
        # A confirmed, completed test can remove its own disposable file through the vault API.
        slot = 'app[' + json.dumps('rich-cleanup-' + identity) + ']'
        client.evaluate('(()=>{' + slot + '={done:false};app.vault.delete(app.vault.getAbstractFileByPath('
                        + json.dumps(note) + ')).then(()=>{' + slot + '={done:true}}).catch(e=>{'
                        + slot + '={done:true,error:String(e)}})})()', True)
        import time
        for _ in range(100):
            cleanup = client.evaluate('JSON.stringify(' + slot + ')')
            if cleanup.get('done'):
                assert not cleanup.get('error'), cleanup
                break
            time.sleep(.05)
        else:
            raise AssertionError('Cleanup is unconfirmed; inspect the retained manifest')
        for request in requests:
            client.forget(request)
        print(json.dumps({'pluginVersion': diagnostic['pluginVersion'], 'preview': str(directory / 'after.webp'),
                          'before': str(directory / 'before.webp'), 'passed': ['partial marks in four shape types',
                          'ambiguous-match rejection', 'list conversion', 'remove/reapply mark', 'rich-text observation',
                          'separate native arrow label', 'bindings and unrelated records preserved',
                          'saved export revision', 'disk reopen', 'temporary note removed']}, indent=2))
    except BaseException:
        print('Retained evidence: ' + str(directory / 'manifest.json'), file=sys.stderr)
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--vault', required=True)
    run(parser.parse_args().vault)
