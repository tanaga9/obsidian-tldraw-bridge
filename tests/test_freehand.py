import base64
import json
import math
from pathlib import Path
import struct
import subprocess
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from obsidian_tldraw_bridge.freehand import compile_script, encode_points, sample_path


def decode(path):
    data = base64.b64decode(path)
    point = list(struct.unpack_from('<fff', data))
    result = [point[:]]
    for offset in range(12, len(data), 6):
        point = [a + b for a, b in zip(point, struct.unpack_from('<eee', data, offset))]
        result.append(point)
    return result


class CurveTest(unittest.TestCase):
    def test_quadratic_and_cubic_pass_through_expected_midpoints(self):
        quadratic, closed = sample_path('M 0 0 Q 10 20 20 0', 1)
        self.assertFalse(closed)
        self.assertEqual(quadratic[-1], (20, 0))
        self.assertLess(min(math.dist(p, (10, 10)) for p in quadratic), .5)
        cubic, _ = sample_path('M0,0 C0,20 20,20 20,0', 1)
        self.assertLess(min(math.dist(p, (10, 15)) for p in cubic), .5)
        self.assertEqual(cubic[-1], (20, 0))

    def test_close_samples_return_to_origin(self):
        points, closed = sample_path('M-5 2 L15 2 L15 20 Z', 2)
        self.assertTrue(closed)
        self.assertEqual(points[0], points[-1])
        self.assertTrue(all(math.dist(a, b) <= 2.01 for a, b in zip(points, points[1:])))

    def test_bad_geometry_is_rejected(self):
        for path in ['M0 0', 'L0 0', 'M0 0 M1 1', 'M0 0 Q1 2', 'M0 0 l1 2',
                     'M0 0 L1e999 1', 'M0 0 L1 1 Z L2 2', 'M0 0 L0 0']:
            with self.subTest(path=path), self.assertRaises(ValueError):
                sample_path(path, 2)

    def test_quantization_does_not_accumulate_drift(self):
        points = [(i * .1234567, math.sin(i / 50), .5) for i in range(10000)]
        actual = decode(encode_points(points))
        self.assertEqual(len(actual), len(points))
        for expected, found in zip(points, actual):
            self.assertLess(max(abs(a - b) for a, b in zip(expected, found)), .001)

    def test_invalid_definitions_are_rejected_before_dispatch(self):
        valid = {'id': 'shape:line', 'path': 'M0 0 L10 10'}
        for data in [None, {}, {'strokes': []}, {'strokes': [valid, valid]},
                     {'strokes': [dict(valid, pressure=True)]},
                     {'strokes': [dict(valid, scale=0)]},
                     {'strokes': [dict(valid, parentId='elsewhere')]},
                     {'strokes': [dict(valid, part='')]},
                     {'strokes': [dict(valid, pressure=10 ** 400)]},
                     {'strokes': [dict(valid, fill='fill')]},
                     {'strokes': [dict(valid, fill='unknown')]},
                     {'strokes': [dict(valid, opacity=-.1)]},
                     {'strokes': [dict(valid, opacity=1.1)]},
                     {'strokes': [dict(valid, opacity=True)]},
                     {'strokes': [dict(valid, opacity=float('nan'))]},
                     {'spacing': float('nan'), 'strokes': [valid]}]:
            with self.subTest(data=data), self.assertRaises(ValueError):
                compile_script(data)


class StrokeEditTest(unittest.TestCase):
    def run_edit(self, data, existing=None):
        # Execute the actual generated code, testing observable edits rather
        # than matching strings in the script template. Node is a test dependency.
        harness = '''
const input=JSON.parse(require('fs').readFileSync(0,'utf8'));
const records=new Map(input.existing.map(s=>[s.id,s]));
const editor={
 getCurrentPageId:()=> 'page:a', getShape:id=>records.get(id),
 createShapes:shapes=>{for(const s of shapes)records.set(s.id,s)},
 updateShapes:shapes=>{for(const s of shapes){const old=records.get(s.id);records.set(s.id,{...old,...s,props:{...old.props,...s.props}})}}
};
try {new Function('editor',input.code)(editor);console.log(JSON.stringify({records:[...records.values()]}))}
catch(e){console.log(JSON.stringify({error:e.message,records:[...records.values()]}))}
'''
        proc = subprocess.run(['node', '-e', harness], input=json.dumps({
            'code': compile_script(data), 'existing': existing or [],
        }), capture_output=True, text=True, check=True)
        return json.loads(proc.stdout)

    def test_filled_translucent_region_is_created_in_one_edit_and_redraw_resets_style(self):
        data = {'strokes': [{'id': 'shape:paint', 'path': 'M0 0 L30 0 L15 20 Z',
                             'color': 'red', 'fill': 'fill', 'opacity': .35}]}
        result = self.run_edit(data)
        self.assertNotIn('error', result)
        region = result['records'][0]
        self.assertEqual(region['props']['fill'], 'fill')
        self.assertEqual(region['props']['color'], 'red')
        self.assertEqual(region['opacity'], .35)
        self.assertTrue(region['props']['isClosed'])
        result = self.run_edit({'strokes': [{'id': 'shape:paint', 'path': 'M0 0 L40 10'}]},
                               [dict(region, meta={'note': 'keep'})])
        region = result['records'][0]
        self.assertEqual(region['props']['fill'], 'none')
        self.assertEqual(region['opacity'], 1)
        self.assertEqual(region['meta'], {'note': 'keep'})

    def test_redraw_preserves_id_parent_and_other_metadata(self):
        existing = [
            {'id': 'shape:frame', 'type': 'frame', 'parentId': 'page:a'},
            {'id': 'shape:curve', 'type': 'draw', 'parentId': 'shape:frame',
             'meta': {'note': 'retain', 'bridgeFreehand': {'part': 'detail'}}, 'props': {'scale': 1}},
        ]
        result = self.run_edit({'strokes': [{'id': 'shape:curve', 'path': 'M0 0 Q10 20 20 0',
                                             'part': 'refined-detail', 'scale': .5}]}, existing)
        self.assertNotIn('error', result)
        self.assertEqual(len(result['records']), 2)
        curve = next(s for s in result['records'] if s['id'] == 'shape:curve')
        self.assertEqual(curve['parentId'], 'shape:frame')
        self.assertEqual(curve['meta'], {'note': 'retain', 'bridgeFreehand': {'part': 'refined-detail'}})
        self.assertEqual(curve['props']['scale'], .5)
        points = decode(curve['props']['segments'][0]['path'])
        self.assertAlmostEqual(points[-1][0], 20, places=3)
        self.assertTrue(curve['props']['isComplete'])

    def test_invalid_target_prevents_any_edits(self):
        for target in [
            {'id': 'shape:target', 'type': 'geo', 'parentId': 'page:a'},
            {'id': 'shape:target', 'type': 'draw', 'parentId': 'page:other'},
        ]:
            result = self.run_edit({'strokes': [
                {'id': 'shape:new', 'path': 'M0 0 L20 0'},
                {'id': 'shape:target', 'path': 'M0 0 L20 0'},
            ]}, [target])
            self.assertIn('error', result)
            self.assertEqual(result['records'], [target])

    def test_new_stroke_uses_frame_and_native_draw_records(self):
        frame = {'id': 'shape:f', 'type': 'frame', 'parentId': 'page:a'}
        result = self.run_edit({'strokes': [{'id': 'shape:outline', 'parentId': frame['id'],
                                            'part': 'outline', 'path': 'M-10 5 L20 30'}]}, [frame])
        self.assertNotIn('error', result)
        stroke = result['records'][1]
        self.assertEqual((stroke['x'], stroke['y']), (-10, 5))
        self.assertEqual(stroke['type'], 'draw')
        self.assertEqual(stroke['parentId'], frame['id'])
        self.assertEqual(stroke['meta']['bridgeFreehand']['part'], 'outline')
