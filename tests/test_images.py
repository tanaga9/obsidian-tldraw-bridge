import base64
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from obsidian_tldraw_bridge.api import Bridge
from obsidian_tldraw_bridge.cli import main
from obsidian_tldraw_bridge.obsidian import BridgeError


class ImageTest(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.factory = Mock()
        self.bridge = Bridge('Vault', client_factory=self.factory)

    def image(self, data, name='写真.webp'):
        path = self.root / name
        path.write_bytes(data)
        return str(path)

    def test_supported_bytes_are_sent_inline_without_changing_the_original_file(self):
        for data, mime in [(b'RIFF\x04\0\0\0WEBP', 'image/webp'), (b'\xff\xd8\xff\xe0example', 'image/jpeg'),
                           (b'\x89PNG\r\n\x1a\n', 'image/png')]:
            with self.subTest(mime=mime):
                filename = self.image(data)
                self.bridge.call('insert-image', {'path': '図.md', 'revision': 'r', 'file': filename,
                                                'x': -20, 'width': 320, 'parentId': 'shape:frame'}, 'image-1')
                args = self.factory.return_value.call.call_args.args
                self.assertEqual((args[0], args[2]), ('insert-image', 'image-1'))
                self.assertEqual(args[1]['src'], 'data:' + mime + ';base64,' + base64.b64encode(data).decode('ascii'))
                self.assertEqual(args[1]['name'], '写真.webp')
                self.assertNotIn('file', args[1])
                self.assertEqual(Path(filename).read_bytes(), data)

    def test_invalid_files_and_geometry_fail_before_connection(self):
        webp = self.image(b'RIFF\x04\0\0\0WEBP')
        base = {'path': 'a.md', 'revision': 'r', 'file': webp}
        invalid = [{'file': self.image(b'GIF89a', 'image.gif')}, {'file': str(self.root / 'missing.jpg')},
                   {'file': ''}, {'width': 0}, {'height': -1}, {'x': True}, {'y': float('nan')},
                   {'width': float('inf')}, {'shapeId': 'asset:bad'}, {'parentId': 'page:a'},
                   {'pageId': 'shape:a'}, {'revision': ''}, {'maxDimension': 0}, {'maxBytes': True},
                   {'format': 'jpeg'}, {'quality': .8}, {'format': 'webp', 'quality': 2}]
        for change in invalid:
            with self.subTest(change=change), self.assertRaises(BridgeError) as error:
                self.bridge.call('insert-image', {**base, **change})
            self.assertEqual((error.exception.code, error.exception.outcome), ('INVALID_INPUT', 'not_applied'))
        self.factory.assert_not_called()

    def test_cli_passes_file_layout_and_revision_to_shared_api(self):
        filename = self.image(b'\xff\xd8\xff\xe0example', '写真.jpeg')
        with patch('obsidian_tldraw_bridge.cli.Client') as client, contextlib.redirect_stdout(io.StringIO()):
            client.return_value.call.return_value = {'shapeId': 'shape:photo'}
            self.assertEqual(main(['--vault', 'Vault', '--request-id', 'photo', 'insert-image', 'a.md',
                                   '--revision', 'r', '--file', filename, '--x', '20', '--y', '30',
                                   '--width', '400', '--parent-id', 'shape:frame', '--page-id', 'page:a',
                                   '--shape-id', 'shape:photo', '--full']), 0)
            action, args, request_id = client.return_value.call.call_args.args
            self.assertEqual((action, request_id), ('insert-image', 'photo'))
            self.assertEqual((args['x'], args['y'], args['width']), (20, 30, 400))
            self.assertEqual((args['parentId'], args['pageId'], args['shapeId']), ('shape:frame', 'page:a', 'shape:photo'))
            self.assertTrue(args['full'])

    def test_argument_order_does_not_change_image_request_identity(self):
        args = {'path': 'a.md', 'revision': 'r', 'file': self.image(b'RIFF\x04\0\0\0WEBP'),
                'width': 320, 'shapeId': 'shape:image', 'pageId': 'page:a'}
        self.assertEqual(json.dumps(Bridge.prepare('insert-image', args)),
                         json.dumps(Bridge.prepare('insert-image', dict(reversed(list(args.items()))))))

    def test_image_info_needs_no_note_or_revision_and_keeps_processing_options(self):
        filename = self.image(b'\x89PNG\r\n\x1a\n', 'original.png')
        args = Bridge.prepare('image-info', {'file': filename, 'maxDimension': 1600, 'format': 'webp',
                                           'quality': .8, 'maxBytes': 500000})
        self.assertEqual((args['maxDimension'], args['format'], args['quality'], args['maxBytes']), (1600, 'webp', .8, 500000))
        self.assertTrue(args['src'].startswith('data:image/png;base64,'))
        self.assertEqual(Path(filename).read_bytes(), b'\x89PNG\r\n\x1a\n')
        with patch('obsidian_tldraw_bridge.cli.Client') as client, contextlib.redirect_stdout(io.StringIO()):
            client.return_value.call.return_value = {'transformed': True}
            self.assertEqual(main(['--vault', 'Vault', 'image-info', '--file', filename,
                                   '--max-dimension', '1600', '--format', 'webp', '--quality', '.8']), 0)
            self.assertEqual(client.return_value.call.call_args.args[:2], ('image-info', {k:v for k,v in args.items() if k!='maxBytes'}))
