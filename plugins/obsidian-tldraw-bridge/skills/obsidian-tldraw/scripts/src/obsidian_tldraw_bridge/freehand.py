"""Compile authored curves to revision-checked native draw edits; no image tracing."""
import base64
import json
import math
import re
import struct

class FreehandCapacityError(ValueError):
    """A valid edit exceeds a per-request transport or drawing limit."""


_TOKEN = re.compile(r"[MLQCZ]|[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:[eE][-+]?\d+)?")


def number(value, name, minimum=None, maximum=None):
    try:
        finite = not isinstance(value, bool) and isinstance(value, (int, float)) and math.isfinite(value)
    except OverflowError:
        finite = False
    if not finite:
        raise ValueError(name + " must be finite")
    if (minimum is not None and value < minimum) or (maximum is not None and value > maximum):
        raise ValueError(name + " is out of range")
    return value


def sample_path(path, spacing):
    if not isinstance(path, str) or not path.strip():
        raise ValueError("Each stroke needs a nonempty path")
    tokens = []
    end = 0
    for match in _TOKEN.finditer(path):
        if path[end:match.start()].strip(" ,\t\r\n"):
            raise ValueError("Paths support absolute M, L, Q, C, and Z commands only")
        tokens.append(match.group())
        end = match.end()
    if path[end:].strip(" ,\t\r\n"):
        raise ValueError("Invalid path token")
    points = []
    i = 0
    closed = False
    while i < len(tokens):
        command = tokens[i]
        i += 1
        if closed or command not in ("M", "L", "Q", "C", "Z"):
            raise ValueError("Use an explicit command for each path segment; Z must be last")
        if (command == "M" and points) or (command != "M" and not points):
            raise ValueError("Use one initial M per stroke; use separate strokes for pen lifts")
        count = {"M": 2, "L": 2, "Q": 4, "C": 6, "Z": 0}[command]
        try:
            values = [number(float(t), "Coordinate", -1000000, 1000000) for t in tokens[i:i + count]]
        except ValueError as exc:
            raise ValueError("Invalid path coordinates") from exc
        if len(values) != count:
            raise ValueError("Incomplete path command")
        i += count
        coords = list(zip(values[::2], values[1::2]))
        if command == "M":
            points.append(coords[0])
            continue
        if command == "Z":
            coords = [points[0]]
            closed = True
        controls = [points[-1]] + coords
        length = sum(math.dist(a, b) for a, b in zip(controls, controls[1:]))
        steps = max(1, math.ceil(length / spacing))
        if len(points) + steps > 100000:
            raise ValueError("Stroke exceeds 100000 sampled points")
        for step in range(1, steps + 1):
            t = step / steps
            curve = controls
            while len(curve) > 1:
                curve = [tuple((1 - t) * x + t * y for x, y in zip(a, b))
                         for a, b in zip(curve, curve[1:])]
            if curve[0] != points[-1]:
                points.append(curve[0])
    if len(points) < 2:
        raise ValueError("A stroke must contain at least two distinct points")
    return points, closed


def encode_points(points):
    """SDK delta format: Float32 first point, little-endian Float16 deltas."""
    data = bytearray(struct.pack("<fff", *points[0]))
    # Accumulate quantized deltas to prevent drift across long curves.
    previous = list(struct.unpack("<fff", data))
    for point in points[1:]:
        delta = [a - b for a, b in zip(point, previous)]
        if any(abs(d) > 65504 for d in delta):
            raise ValueError("Stroke point delta exceeds Float16 range")
        packed = struct.pack("<eee", *delta)
        data.extend(packed)
        previous = [a + b for a, b in zip(previous, struct.unpack("<eee", packed))]
    return base64.b64encode(data).decode("ascii")


def _compile_strokes(data):
    if not isinstance(data, dict) or not isinstance(data.get("strokes"), list) or not data["strokes"]:
        raise ValueError("Expected an object with a nonempty strokes array")
    if len(data["strokes"]) > 1000:
        raise FreehandCapacityError("Use at most 1000 strokes per edit")
    spacing = number(data.get("spacing", 2), "spacing", .25, 20)
    strokes = []
    ids = set()
    total = 0
    for stroke in data["strokes"]:
        if not isinstance(stroke, dict):
            raise ValueError("Each stroke must be an object")
        identity = stroke.get("id")
        if not isinstance(identity, str) or not identity.startswith("shape:") or len(identity) <= 6 or identity in ids:
            raise ValueError("Each stroke needs a unique shape: ID")
        ids.add(identity)
        points, closed = sample_path(stroke.get("path"), spacing)
        total += len(points)
        if total > 100000:
            raise FreehandCapacityError("Edit exceeds 100000 sampled points")
        pressure = number(stroke.get("pressure", .5), "pressure", 0, 1)
        taper = number(stroke.get("taper", .15), "taper", 0, 1)
        scale = number(stroke.get("scale", 1), "scale", .01, 100)
        size = stroke.get("size", "s")
        if size not in ("s", "m", "l", "xl"):
            raise ValueError("size must be s, m, l, or xl")
        color = stroke.get("color", "black")
        if not isinstance(color, str):
            raise ValueError("color must be a tldraw color name")
        fill = stroke.get("fill", "none")
        if fill not in ("none", "semi", "solid", "pattern", "fill", "lined-fill"):
            raise ValueError("fill must be none, semi, solid, pattern, fill, or lined-fill")
        if fill != "none" and not closed:
            raise ValueError("Filled strokes must close their path with Z")
        opacity = number(stroke.get("opacity", 1), "opacity", 0, 1)
        part = stroke.get("part")
        if part is not None and (not isinstance(part, str) or not part.strip()):
            raise ValueError("part must be a nonempty string")
        parent = stroke.get("parentId")
        if parent is not None and (not isinstance(parent, str) or not parent.startswith(("shape:", "page:"))):
            raise ValueError("parentId must be a shape: or page: ID")
        origin = [min(p[d] for p in points) for d in (0, 1)]
        local = [[p[0] - origin[0], p[1] - origin[1],
                  pressure * (1 - taper * (1 - math.sin(math.pi * i / (len(points) - 1))))]
                 for i, p in enumerate(points)]
        result = {
            "id": identity, "opacity": opacity, "x": origin[0] + number(stroke.get("x", 0), "x"),
            "y": origin[1] + number(stroke.get("y", 0), "y"),
            "props": {"segments": [{"type": "free", "path": encode_points(local)}],
                      "color": color, "size": size, "scale": scale, "fill": fill,
                      "dash": "draw", "isPen": True, "isComplete": True, "isClosed": closed},
        }
        if parent is not None:
            result["parentId"] = parent
        if part is not None:
            result["part"] = part
        strokes.append(result)
    return strokes, total


def _render_script(strokes):
    script = _SCRIPT.replace("__STROKES__", json.dumps(strokes, separators=(",", ":")))
    if len(script.encode("utf-8")) > 96000:
        raise FreehandCapacityError("Freehand edit is too large; split it into smaller passes")
    return script


def compile_script(data):
    strokes, _ = _compile_strokes(data)
    return _render_script(strokes)


def plan_passes(data):
    """Validate the entire drawing and partition it into ordered, valid edits.

    This is a planning operation only: each pass remains a separate edit with
    its own revision and request ID, so no atomicity is implied.
    """
    if not isinstance(data, dict) or not isinstance(data.get("strokes"), list) or not data["strokes"]:
        raise ValueError("Expected an object with a nonempty strokes array")
    strokes = data["strokes"]
    options = {key: value for key, value in data.items() if key != "strokes"}
    ids = set()
    prepared = []
    # Compile exactly once per stroke. No edit is returned unless all input is valid.
    for stroke in strokes:
        compiled, points = _compile_strokes({**options, "strokes": [stroke]})
        _render_script(compiled)  # A single stroke must fit by itself.
        identity = stroke["id"]
        if identity in ids:
            raise ValueError("Each stroke needs a unique shape: ID across all passes")
        ids.add(identity)
        encoded = json.dumps(compiled[0], separators=(",", ":")).encode("utf-8")
        prepared.append((stroke, points, len(encoded)))
    # JSON emits ASCII escapes by default, as in _render_script. Count commas
    # and the fixed script wrapper exactly, without repeatedly sampling curves.
    base_bytes = len(_render_script([]).encode("utf-8"))
    result, current = [], []
    count_points = payload_bytes = 0
    for stroke, points, size in prepared:
        next_bytes = payload_bytes + size + (1 if current else 0)
        if current and (len(current) == 1000 or count_points + points > 100000 or base_bytes + next_bytes > 96000):
            result.append({**options, "strokes": current})
            current, count_points, payload_bytes = [], 0, 0
            next_bytes = size
        current.append(stroke)
        count_points += points
        payload_bytes = next_bytes
    if current:
        result.append({**options, "strokes": current})
    return result


_SCRIPT = r'''
const strokes = __STROKES__;
const create = [], update = [];
const page = editor.getCurrentPageId();
function checkParent(id) {
  const seen = new Set();
  while (id !== page) {
    if (seen.has(id)) throw new Error('Cyclic stroke parent');
    seen.add(id);
    const shape = editor.getShape(id);
    if (!shape) throw new Error('Stroke parent is not on the current page');
    if (shape.type !== 'frame' && shape.type !== 'group') throw new Error('Stroke parents must be frames or groups');
    id = shape.parentId;
  }
}
for (const stroke of strokes) {
  const existing = editor.getShape(stroke.id);
  if (existing && existing.type !== 'draw') throw new Error('Stroke ID belongs to a non-draw shape: ' + stroke.id);
  if (existing) checkParent(existing.parentId);
  const parentId = stroke.parentId ?? existing?.parentId ?? page;
  checkParent(parentId);
  const { part, ...shape } = stroke;
  shape.type = 'draw';
  shape.parentId = parentId;
  if (part !== undefined) shape.meta = { ...existing?.meta, bridgeFreehand: { ...existing?.meta?.bridgeFreehand, part } };
  (existing ? update : create).push(shape);
}
if (create.length) editor.createShapes(create);
if (update.length) editor.updateShapes(update);
'''
