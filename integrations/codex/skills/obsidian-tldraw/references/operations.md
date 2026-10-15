# Operations

Input is a JSON array, or an object with an `operations` array:

```json
[
  {"method":"createShapes","args":[[
    {"id":"shape:example","type":"geo","x":80,"y":80,
     "props":{"geo":"rectangle","w":220,"h":120,"color":"blue"}}
  ]]}
]
```

Supported methods: createShapes, updateShapes, deleteShapes, createBindings,
deleteBindings, groupShapes, ungroupShapes, alignShapes, distributeShapes,
rotateShapesBy, resizeShape, reparentShapes, createPage, updatePage, deletePage,
setCurrentPage, undo, redo. Arguments follow the installed tldraw SDK Editor API.
Inspect existing records for shape props, binding endpoints, rich text and asset records.
IDs must have the tldraw prefix, such as `shape:example` or `binding:example`.

Undo/redo each require a separate single-operation batch. Other operations in a
batch have one history boundary and restore synchronous Store record changes on exceptions, including changes excluded from Undo history.
State and revision cover the SDK document scope, including document settings, pages, shapes, bindings, assets and any other persistent record types.
Preview renders current-page shapes; switch pages before exporting another page.

Example synchronous SDK script:

```js
const ids = [...editor.getCurrentPageShapeIds()];
editor.alignShapes(ids, 'left');
```

Do not mutate records after the script returns. Timers and promises would bypass
revision checks, rollback, and save completion. Automatic conflict resolution is
not provided. A revision check detects changes before the edit; it does not lock
out human edits while a long export is running.

Preview checks the document revision before and after asynchronous rendering and blob conversion. A conflict leaves an existing output file unchanged. An unsupported async script can still run already scheduled callbacks after it returns an error; this bridge does not provide a JavaScript sandbox or cancellation of arbitrary code.

## Results

`batch` and `script` return compact summaries with `path`, `revision`, `currentPageId`, `changes` (`added`, `updated`, `removed`), and `persistence`. Change counts measure net differences in document-scope records. Session records are excluded. Use `state` for full records, or add `--full` to an edit for full state plus change counts. A replayed request ID must use the same arguments, including the full-output option.
