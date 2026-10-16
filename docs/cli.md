# CLI reference

Direct CLI use is intended for development and debugging. It is not part of the plugin user's setup.

## Command examples

Run these commands from the repository root; package installation is not required.

```sh
python3 bridge.py --vault Documents doctor
python3 bridge.py --vault Documents --request-id create-example create 'Drawings/example.md'
python3 bridge.py --vault Documents state 'Drawings/example.md'
```

Use the `revision` returned by `state` when submitting edits:

```sh
python3 bridge.py --vault Documents batch 'Drawings/example.md' \
  --revision '<revision-from-state>' --input examples/create.json
python3 bridge.py --vault Documents preview 'Drawings/example.md' --output /tmp/example.png
python3 bridge.py --vault Documents close 'Drawings/example.md'
```

Use `--obsidian /path/to/executable` or the `OBSIDIAN_CLI` environment variable to override the Obsidian CLI location. Always specify the vault. Diagram paths are vault-relative `.md` paths. For `batch` and `script`, `--input -` reads from standard input. Results are JSON; handled errors are written as JSON to standard error with exit code 1.

Explicit `--obsidian` takes precedence over `OBSIDIAN_CLI`; an invalid override fails without switching installations. Automatic discovery checks `obsidian` on PATH, then `obsidian-cli` on PATH, then `/Applications/Obsidian.app/Contents/MacOS/obsidian-cli`. If an older PATH registration resolves to the app bundle's GUI executable, discovery selects its sibling `obsidian-cli` instead. Automatic discovery never falls back to launching that GUI executable; update the installer if the dedicated CLI is missing.

Optional Python package installation with `python3 -m pip install .` exposes the `obsidian-tldraw` command. Normal plugin use does not require this installation.

## Freehand drawing and detail previews

`freehand <path> --revision <revision> --input <json-file>` creates or redraws strokes from authored curves using stable IDs. See the bundled [freehand reference](../integrations/codex/skills/obsidian-tldraw/references/freehand.md) for the input format and iterative workflow. It uses the same edit result, persistence, and request-ID contracts as `script`.

`preview` accepts `--part <part>` or `--ids <shape-id> ...` to export a subset of the current page, and `--scale <number>` to enlarge it (greater than 0, at most 4). The default remains a whole-page preview at scale 1. An empty or invalid selection fails without changing the output file.

## Edit results

`batch` and `script` return a compact result by default:

```json
{
  "path": "Drawings/example.md",
  "revision": "<new revision>",
  "currentPageId": "page:example",
  "changes": {"added": 2, "updated": 1, "removed": 0},
  "persistence": {"saved": true, "path": "Drawings/example.md", "bytes": 1024}
}
```

`changes` counts the net differences in all persistent document records, including shapes, pages, bindings, assets, and document settings. Changes made and reversed within one edit count as zero; camera and selection changes are excluded. Counts describe the edit itself, rather than the number of requested operations.

Use `state <path.md>` to inspect full records, or append `--full` to `batch` or `script` to include records and editor diagnostics in that edit's result. `--full` is part of the request: keep it unchanged when replaying an explicit request ID. Previously retained requests still return their original results. `create`, `open`, and `state` continue to return full document state.

## Create a note

`create <path.md>` creates a new tldraw Markdown note through the plugin, opens a GUI tab and a bridge Editor session, and checks persistence. Parent folders are created by the plugin when needed. No revision is required for creation. The result includes `created: true`, the actual `path`, `requestedPath`, `currentPageId`, `revision`, records, and `persistence`. Use the returned revision for the first edit. Use `open <path.md>` for an existing note.

An existing file or folder at the requested path is rejected without overwriting it. If another client takes the name during creation, the plugin may choose a unique filename; use the returned `path` for subsequent commands. Creation uses the plugin's current frontmatter, tags, and serialization settings.

Pass an explicit `--request-id` to recover a timed-out creation without creating another note. If the note was created but opening or checking persistence failed, the error identifies the retained note's path. Recover it with `open` and `saved`; the bridge does not delete the note automatically.

## Release retained results

A request with an explicit `--request-id` can retrieve its result using the same ID and arguments. Release a completed result when it is no longer needed:

```sh
python3 bridge.py --vault Documents forget '<request-id>'
```

Forgetting an ID also removes its deduplication protection. Ordinary results are released automatically after retrieval; timed-out requests are retained. At the 128-receipt limit, new requests are rejected without executing them.

## Runtime reload diagnostics

`state` and successful edits include `currentPageId`. Source updates preserve the selected page when recreating each dedicated Editor. `doctor` includes a `reloadErrors` array with the path, previous page ID, and error for each failed reopen. A failed document does not block other documents. Use `open <path>` to retry recovery, or `close <path>` to dismiss its recovery entry. If the previous page was deleted, dismiss recovery before opening the document normally.
