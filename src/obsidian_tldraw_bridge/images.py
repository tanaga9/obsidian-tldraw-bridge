"""Load supported image bytes without an imaging-library dependency."""
import base64
from pathlib import Path


def load_image(filename):
    path = Path(filename).expanduser()
    data = path.read_bytes()
    if data[:3] == b'\xff\xd8\xff':
        mime = 'image/jpeg'
    elif data[:4] == b'RIFF' and data[8:12] == b'WEBP':
        mime = 'image/webp'
    elif data[:8] == b'\x89PNG\r\n\x1a\n':
        mime = 'image/png'
    else:
        raise ValueError('Supported image formats are PNG, WebP and JPEG')
    return {'name': path.name, 'src': 'data:' + mime + ';base64,' + base64.b64encode(data).decode('ascii')}
