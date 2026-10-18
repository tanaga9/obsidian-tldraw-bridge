"""Opt-in image inspection, optional processing, and insertion check."""
import argparse
import base64
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from obsidian_tldraw_bridge.api import Bridge
from obsidian_tldraw_bridge.obsidian import Client, BridgeError

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--vault', required=True)
p.add_argument('--output', default=str(Path(tempfile.gettempdir()) / 'obsidian-tldraw-images.png'))
options = p.parse_args()
c = Client(options.vault, timeout=60)
bridge = Bridge(options.vault, timeout=60)
identity = 'images-' + uuid.uuid4().hex
path = 'workspace/drawings/' + identity + '.md'
requests = [identity + suffix for suffix in ('-create', '-webp', '-jpeg', '-png', '-processed', '-corrupt', '-size')]
created = False

with tempfile.TemporaryDirectory(prefix='bridge-images-') as directory:
    try:
        c.call('doctor')
        # Browser encoders provide real fixtures without installing Pillow or
        # codecs. These are test pixels, not conversions of a user's image.
        fixtures = c.evaluate('''JSON.stringify((()=>{
const canvas=document.createElement('canvas');canvas.width=160;canvas.height=96;
const ctx=canvas.getContext('2d');ctx.fillStyle='#e4ddff';ctx.fillRect(0,0,160,96);
ctx.fillStyle='#3468b2';ctx.fillRect(8,8,60,80);ctx.fillStyle='#d95147';ctx.fillRect(76,8,76,80);
ctx.fillStyle='#ffffff';ctx.font='bold 14px sans-serif';ctx.fillText('IMAGE',82,53);
return {webp:canvas.toDataURL('image/webp'),jpeg:canvas.toDataURL('image/jpeg'),png:canvas.toDataURL('image/png')};
})())''')
        files = {}
        for extension, source in fixtures.items():
            assert source.startswith('data:image/' + extension + ';base64,')
            files[extension] = Path(directory) / ('画像.' + extension)
            files[extension].write_bytes(base64.b64decode(source.split(',', 1)[1]))
        info = bridge.call('image-info', {'file': str(files['png'])})
        assert info['source']['bytes'] == files['png'].stat().st_size
        assert info['output']['dataUrlBytes'] == len(fixtures['png'])
        assert not info['transformed']
        processed_info = bridge.call('image-info', {'file': str(files['png']), 'maxDimension': 80, 'format': 'webp', 'quality': .7})
        assert (processed_info['output']['width'], processed_info['output']['height']) == (80, 48)
        assert processed_info['output']['mimeType'] == 'image/webp'
        print('image-info: byte counts, dimensions and optional processing inspected without a note', flush=True)
        try:
            opened = c.call('create', {'path': path}, requests[0])
        except BridgeError as error:
            if error.code != 'RESULT_UNKNOWN':
                raise
            receipt = c.status(requests[0])
            if receipt['status'] != 'complete':
                raise
            opened = receipt['result']
        created = True
        framed = c.call('apply', {'path': path, 'revision': opened['revision'], 'operations': [
            {'op': 'createShapes', 'shapes': [
                {'id': 'shape:images-frame', 'type': 'frame', 'props': {'w': 1390, 'h': 750, 'name': 'PNG / WebP / JPEG + 明示指定の縮小・変換'}}
            ]}
        ]})
        image_args = {}
        current = framed
        for index, extension in enumerate(('webp', 'jpeg', 'png')):
            args = {'path': path, 'revision': current['revision'], 'file': str(files[extension]),
                    'x': 40 + index * 450, 'y': 70, 'width': 400, 'parentId': 'shape:images-frame',
                    'shapeId': 'shape:' + extension, 'pageId': opened['currentPageId']}
            image_args[extension] = dict(args)
            if extension == 'webp':
                # Exercise the actual CLI as well as the shared Python API.
                result = subprocess.run([sys.executable, str(ROOT / 'bridge.py'), '--vault', options.vault,
                    '--timeout', '60', '--request-id', requests[index + 1], 'insert-image', path,
                    '--revision', args['revision'], '--file', args['file'], '--x', str(args['x']), '--y', '70',
                    '--width', '400', '--parent-id', args['parentId'], '--shape-id', args['shapeId'],
                    '--page-id', args['pageId']], capture_output=True, encoding='utf-8', check=True)
                current = json.loads(result.stdout)
            else:
                current = bridge.call('insert-image', args, requests[index + 1])
            assert current['persistence']['saved']
            assert (current['width'], current['height']) == (400, 240)
            assert current['mimeType'] == 'image/' + extension
            assert bridge.call('insert-image', args, requests[index + 1]) == current
            print(extension + ': inserted, saved, replayed without duplication', flush=True)
        processed = bridge.call('insert-image', {'path': path, 'revision': current['revision'],
            'file': str(files['png']), 'x': 40, 'y': 400, 'width': 400, 'parentId': 'shape:images-frame',
            'maxDimension': 80, 'format': 'webp', 'quality': .7, 'shapeId': 'shape:processed'}, requests[4])
        assert processed['image'] == processed_info
        assert files['png'].read_bytes() == base64.b64decode(fixtures['png'].split(',')[1])
        before = c.call('state', {'path': path})
        for extension in ('size', 'corrupt'):
            filename = files['png']
            if extension == 'corrupt':
                filename = Path(directory) / 'corrupt.webp'
                filename.write_bytes(b'RIFF\x04\0\0\0WEBPinvalid')
            try:
                extra = {'maxBytes': 1} if extension == 'size' else {}
                bridge.call('insert-image', {'path': path, 'revision': before['revision'], 'file': str(filename), **extra},
                            requests[5] if extension == 'corrupt' else requests[6])
                raise AssertionError('Invalid image accepted: ' + extension)
            except BridgeError as error:
                assert (error.code, error.outcome) == ('IMAGE_TOO_LARGE' if extension == 'size' else 'INVALID_INPUT', 'not_applied')
        assert c.call('state', {'path': path})['revision'] == before['revision']
        c.call('close', {'path': path})
        reopened = c.call('open', {'path': path})
        assets = [record for record in reopened['records'] if record['typeName'] == 'asset']
        assert len(assets) == 4
        assert {fixtures['webp'], fixtures['jpeg'], fixtures['png']} <= {asset['props']['src'] for asset in assets}
        transformed_asset = next(asset for asset in assets if asset['id'] == processed['assetId'])
        assert transformed_asset['props']['mimeType'] == 'image/webp'
        assert (transformed_asset['props']['w'], transformed_asset['props']['h']) == (80, 48)
        png_output = Path(options.output).resolve()
        png_preview = bridge.call('preview', {'path': path, 'revision': reopened['revision'], 'format': 'png', 'output': str(png_output)})
        assert png_preview['format'] == 'png' and png_output.read_bytes().startswith(b'\x89PNG\r\n\x1a\n')
        webp_output = png_output.with_suffix('.webp')
        webp_preview = bridge.call('preview', {'path': path, 'revision': reopened['revision'], 'ids': ['shape:images-frame'],
                                             'output': str(webp_output)})
        raw = webp_output.read_bytes()
        assert webp_preview['format'] == 'webp' and raw[:4] == b'RIFF' and raw[8:12] == b'WEBP'
        webp_info = bridge.call('image-info', {'file': str(webp_output)})
        assert webp_info['source']['mimeType'] == 'image/webp'
        assert webp_info['source']['width'] > 0 and webp_info['source']['height'] > 0
        cli_output = Path(directory) / 'cli-preview.webp'
        result = subprocess.run([sys.executable, str(ROOT / 'bridge.py'), '--vault', options.vault,
                                 '--timeout', '60', 'preview', path, '--quality', '.7',
                                 '--revision', reopened['revision'], '--output', str(cli_output)],
                                capture_output=True, encoding='utf-8', check=True)
        assert json.loads(result.stdout)['format'] == 'webp'
        assert cli_output.read_bytes()[:4] == b'RIFF' and cli_output.read_bytes()[8:12] == b'WEBP'
        assert c.call('state', {'path': path})['revision'] == reopened['revision']
        print('Explicit PNG, default API WebP, and CLI WebP with quality override decoded; document unchanged; WebP: ' + str(webp_output), flush=True)
        print('Size limit/corrupt input rejected; original and processed images retained; preview: ' + options.output, flush=True)
    finally:
        if created:
            if path in c.call('doctor')['documents']:
                c.call('close', {'path': path})
            slot = 'app[' + json.dumps(identity + '-cleanup') + ']'
            try:
                c.evaluate('(()=>{' + slot + '={done:false};Promise.resolve().then(async()=>{'
                    'const file=app.vault.getAbstractFileByPath(' + json.dumps(path) + ');if(file)await app.vault.delete(file);'
                    + slot + '={done:true}}).catch(e=>' + slot + '={error:String(e)});return JSON.stringify({scheduled:true});})()')
            except BridgeError:
                # A lost cleanup response must not cause the delete to be replayed.
                if c.evaluate('JSON.stringify(' + slot + '??null)') is None:
                    raise
            for _ in range(100):
                status = c.evaluate('JSON.stringify(' + slot + ')')
                if status.get('error'):
                    raise RuntimeError(status['error'])
                if status.get('done'):
                    break
                time.sleep(.1)
            else:
                raise RuntimeError('Fixture cleanup not confirmed')
            c.evaluate('JSON.stringify(delete ' + slot + ')')
            for request in requests:
                c.forget(request)
            print('Temporary note removed; session closed', flush=True)
