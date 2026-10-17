# Agent operation API

The shared operation layer lives in `src/obsidian_tldraw_bridge/api.py`.
The CLI parses command-line input and delegates to it. The live JavaScript runtime
implements observation, SDK editing, revision checks, rollback, and persistence.
There is no MCP server or HTTP listener in this implementation.

## Using the shared Python interface

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

Use an existing shape's ID and type; the example assumes `shape:example` exists.
Choose a fresh request ID per intended edit, then reuse that ID only with identical
arguments to recover that attempt. `Bridge` validates paths, edit revisions,
observation/preview options, and compiles freehand inputs before connecting.
Runtime named-operation validation and SDK validation apply equally to all callers.

`call(action, args, request_id=None)` returns an operation's JSON-compatible result.
Actions include `capabilities`, `doctor`, `create`, `open`, `observe`, `state`,
`apply`, `batch`, `script`, `freehand`, `saved`, `preview`, and `close`.
`freehand` takes a `drawing` object and compiles it to a synchronous SDK script.
`status(id)` reads a receipt; `forget(id)` releases it and its deduplication protection.
The transport is created lazily after shared input validation.

## Runtime contract

`capabilities` reports `apiVersion`, plugin version/support, named operation fields,
registered shape types when a session is open, limits, and correctness boundaries.
The version identifies this contract; it does not promise backward compatibility.
Shape props follow the installed SDK rather than a new drawing language.

For named operation fields, observation filters/pagination, coordinate systems,
result fields, and failure recovery, use the canonical
[operations reference](../integrations/codex/skills/obsidian-tldraw/references/operations.md).
Compact shapes include parent-local `localPosition` for position updates as
well as page-space bounds for visual reasoning. Full records and advanced SDK
operations remain available for work that the compact interface does not describe.

`BridgeError.as_dict()` and CLI `error` objects contain:

```json
{
  "code": "SAVE_UNCONFIRMED",
  "message": "...",
  "outcome": "applied",
  "requestId": "unique-edit-id",
  "details": {"path": "Drawings/example.md", "revision": "..."}
}
```

`requestId` and `details` are present when available. `outcome` is `not_applied`,
`applied`, or `unknown`; `applied` does not mean saving succeeded. Read operations
can also fail without modifying content. A successful edit includes its new
revision and verified persistence result. Pending inbound changes are reconciled
before observation and revision checks. If another edit changes the document
during saving, `SAVE_CONFLICT` / `applied` reports the original and actual
revisions instead of returning a superseded success result. Script failures have
unknown overall outcome because Store rollback cannot restore external side effects.

The transport reports the request ID even if the initial dispatch times out.
Receipts are retained for explicit IDs and for uncertain/applied automatic failures.
A receipt is an account of one attempt, not a live indicator of current disk state.
Use `saved` to check later persistence. Restarting Obsidian discards receipts.

Future adapters should reuse this operation layer and runtime contract rather
than reimplementing revision, retry, or saving logic. An MCP adapter is a possible
addition, not a requirement for editing through the current CLI.
