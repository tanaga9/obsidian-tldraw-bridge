# Agent operation API

The shared Python interface in `src/obsidian_tldraw_bridge/api.py` powers the CLI.
Reuse it for other adapters so validation, revisions, retries, and persistence
follow the same contract. No MCP server or HTTP listener is provided.

## Python usage

```python
from obsidian_tldraw_bridge.api import Bridge, list_vaults
from obsidian_tldraw_bridge.obsidian import BridgeError

vaults = list_vaults()  # No vault selection, Editor, or plugin execution.
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

- `list_vaults(executable=None, timeout=30, config_dir=".obsidian")` lists registered
  vault names/paths and filesystem tldraw status without selecting a vault.
  `tldraw.status` distinguishes installed, not_installed, incomplete and unknown;
  `version`, `enabled`, `configDir` and diagnostic reasons describe the inspected
  configuration. `enabled` describes saved activation settings, not runtime load.
  Alternative config folder names are explicit. See [vault discovery](cli.md#choosing-a-vault).
  This is a module function, separate from vault-scoped `Bridge.call` actions.
- `Bridge(vault)` selects the vault; transport initialization is lazy.
- `call(action, args, request_id=None)` returns a JSON-compatible result. Actions
  include `capabilities`, `style-spec`, `doctor`, `create`, `open`, `observe`, `state`, `apply`,
  `batch`, `script`, `language-status`, `language-checkpoint`, `freehand`, `image-info`, `insert-image`, `saved`, `preview`, and `close`.
- `style-spec` takes `path` and `shapeType` for an already-open document. It
  reports installed style enums, separate SDK/shape defaults and current creation
  styles with per-field availability/source; it does not edit or save the note.
- `script` returns `scriptResult` beside changes and persistence in compact/full
  output. JSON results are detached and validated inside the rollback transaction
  (64 KiB UTF-8, container depth 32). No return is `{"hasValue":false}`; null is
  `{"hasValue":true,"value":null}`. Invalid results restore Store changes.
  See [script results](../integrations/codex/skills/obsidian-tldraw/references/operations.md#script-results)
  for allowed types, errors, and persistence-failure recovery.
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
- `preview` accepts `format` (`webp` by default, or explicit `png`) and optional WebP
  `quality` (0–1, default 0.9), alongside its selection, scale, revision and output
  options. Format is explicit, not inferred from the output filename. The result
  includes `format`, `path`, logical `width`/`height`, and the captured `revision`.
- Failures raise `BridgeError`; `as_dict()` exposes the same fields as CLI `error` objects.

Paths, revisions, image file types/layout, observation/preview options, and freehand input are validated
before connecting. Runtime operation and SDK validation apply to every caller.

The canonical [operations reference](../integrations/codex/skills/obsidian-tldraw/references/operations.md)
defines discovery, operation fields, coordinates, results, errors, and recovery.
Use [the freehand reference](../integrations/codex/skills/obsidian-tldraw/references/freehand.md)
for drawing input. These interfaces follow the [compatibility policy](development.md#compatibility-policy).

## Language-page actions

`language-status` takes `path` and optional `diagramId`; it returns a read-only
review of all relevant language pages and the observed document revision.
`language-checkpoint` takes `path`, `revision`, `checkpoint`, and optional `full`.
The checkpoint object requires `diagramId`, `editingSourcePageId`, `languages`,
`targetLanguage`, `kind` (`translation`, `adopt`, `layout`), `reason`, and
`reviewed: true`. It registers existing pages and updates only metadata through
revision checks, rollback, saved-state verification, and retained receipts.
The result includes `scriptResult`. Neither action performs translation.
See [multilingual workflow](multilingual.md) for interpretation and limitations.
