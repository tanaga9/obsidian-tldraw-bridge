# Agent operation API

The shared Python interface in `src/obsidian_tldraw_bridge/api.py` powers the CLI.
Reuse it for other adapters so validation, revisions, retries, and persistence
follow the same contract. No MCP server or HTTP listener is provided.

## Python usage

```python
from obsidian_tldraw_bridge.api import Bridge
from obsidian_tldraw_bridge.obsidian import BridgeError

bridge = Bridge("Documents")
bridge.call("open", {"path": "Drawings/example.md"})
view = bridge.call("observe", {"path": "Drawings/example.md", "limit": 100})
result = bridge.call("apply", {
    "path": view["path"],
    "revision": view["revision"],
    "pageId": view["currentPageId"],
    "operations": [{"op": "updateShapes", "shapes": [
        {"id": "shape:example", "type": "geo", "props": {"color": "blue"}}
    ]}],
}, request_id="unique-edit-id")
receipt = bridge.status("unique-edit-id")
bridge.forget("unique-edit-id")
```

The example assumes `shape:example` exists; use an observed shape's ID and type.
Choose a fresh request ID per intended edit and reuse it only with identical arguments.

## Interface

- `Bridge(vault)` selects the vault; transport initialization is lazy.
- `call(action, args, request_id=None)` returns a JSON-compatible result. Actions
  include `capabilities`, `doctor`, `create`, `open`, `observe`, `state`, `apply`,
  `batch`, `script`, `freehand`, `image-info`, `insert-image`, `saved`, `preview`, and `close`.
- `freehand` takes a `drawing` object, compiled to a synchronous SDK script.
- `insert-image` takes `path`, `revision`, and a local image `file`, plus optional
  `x`, `y`, `width`, `height`, `parentId`, `pageId`, `shapeId`, and `full`.
  PNG, WebP and JPEG bytes are preserved by default. Optional `maxDimension`,
  `format` (`original`/`webp`), `quality`, and `maxBytes` control processing.
- `image-info` takes `file` and the same processing options, without a diagram
  path or revision. It reports source/output dimensions and byte counts without
  editing documents. Insertion adds this report as `image` in its result. See
  [image insertion](cli.md#image-insertion) for sizing, storage, and result fields.
- `status(id)` reads a retained receipt; `forget(id)` releases it and its deduplication protection.
- Failures raise `BridgeError`; `as_dict()` exposes the same fields as CLI `error` objects.

Paths, revisions, image file types/layout, observation/preview options, and freehand input are validated
before connecting. Runtime operation and SDK validation apply to every caller.

The canonical [operations reference](../integrations/codex/skills/obsidian-tldraw/references/operations.md)
defines discovery, operation fields, coordinates, results, errors, and recovery.
Use [the freehand reference](../integrations/codex/skills/obsidian-tldraw/references/freehand.md)
for drawing input. These interfaces follow the [compatibility policy](development.md#compatibility-policy).
