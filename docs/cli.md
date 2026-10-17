# CLI reference

The CLI adapts the shared [Python API](api.md). Agents use the bundled Skill;
no separate CLI installation is needed. Interfaces may change without notice;
use this version's `--help` and [compatibility policy](development.md#compatibility-policy).

## Example

Run from the repository root. Create a note, then observe its revision and page:

```sh
python3 bridge.py --vault Documents doctor
python3 bridge.py --vault Documents capabilities
python3 bridge.py --vault Documents --request-id create-example create 'Drawings/example.md'
python3 bridge.py --vault Documents observe 'Drawings/example.md'
```

Substitute the observed revision and `currentPageId` below. Use the returned path
if creation chose a unique filename.

```sh
python3 bridge.py --vault Documents --request-id edit-example apply 'Drawings/example.md' \
  --revision '<revision-from-observe>' --page-id '<currentPageId>' --input - <<'JSON'
[{"op":"createShapes","shapes":[
  {"id":"shape:bridge-example","type":"geo","x":100,"y":100,
   "props":{"geo":"rectangle","w":240,"h":120,"color":"blue","fill":"solid"}}
]}]
JSON
python3 bridge.py --vault Documents preview 'Drawings/example.md' --output /tmp/example.png
python3 bridge.py --vault Documents close 'Drawings/example.md'
```

Always specify the vault; diagram paths are vault-relative `.md` paths. `apply`,
`batch`, `freehand`, and `script` accept `--input -` for standard input. Results
are JSON; handled errors are JSON on standard error with exit code 1.

## Commands and contracts

[Operations and recovery](../integrations/codex/skills/obsidian-tldraw/references/operations.md)
is the canonical reference for input schemas, observation/pagination, coordinates,
SDK access, result fields, errors, persistence, and request-ID recovery.

| Purpose | CLI usage |
| --- | --- |
| Compact observation | `observe <path> [--ids <id> ... \| --bounds X Y W H] [--limit N]`; continue with `--offset N --revision <revision> --page-id <currentPageId>` |
| Full records | `state <path>`; add `--full` to `apply`, `batch`, `script`, or `freehand` for full edit results |
| Freehand drawing | `freehand <path> --revision <revision> --input <file>`; see [drawing input](../integrations/codex/skills/obsidian-tldraw/references/freehand.md) |
| PNG preview | `preview <path> --output <png> [--part <part> \| --ids <id> ...] [--scale <number>]`; scale defaults to 1, maximum 4 |
| Check persistence | `saved <path>` |
| Inspect/release a receipt | `status <request-id>` / `forget <request-id>` |

Use a fresh global `--request-id` for each consequential edit. After a timeout,
inspect its status or repeat the identical request with the same ID. Release
completed receipts with `forget`; explicit IDs occupy the 128-receipt capacity
until forgotten or Obsidian restarts.

## Note creation

`create <path.md>` uses the plugin's current frontmatter, tags, and serialization
settings, creates parent folders as needed, and opens a GUI tab and bridge session.
No revision is required. The result includes `created`, `path`, `requestedPath`,
`currentPageId`, `revision`, records, and `persistence`; use its actual path and revision.

Existing files or folders are rejected. A concurrent name collision may make the
plugin choose a unique filename. Use `open <path>` for existing notes. If creation
succeeds but opening or persistence verification fails, the error identifies the
retained note: recover with `open` and `saved`. The bridge does not delete it.

## Connection and sessions

Use `--obsidian /path/to/executable` or `OBSIDIAN_CLI` to override CLI discovery;
the flag takes precedence and an invalid override fails. Automatic discovery
checks `obsidian` on PATH, `obsidian-cli` on PATH, then
`/Applications/Obsidian.app/Contents/MacOS/obsidian-cli`. Old GUI executable
registrations resolve to the sibling `obsidian-cli`; the GUI executable is never
launched as a fallback. Update the installer if the dedicated CLI is missing.

Multiple document sessions are supported. SDK initialization may open a diagram
tab and return focus to the previously active tab; the diagram tab stays open.
Bridge and GUI Editors have separate Undo histories. Reopen sessions after an
Obsidian restart.

Runtime source updates check persistence and recreate sessions, preserving selected
pages and retained request IDs, but resetting bridge Undo history. Running work
is not interrupted. Failed reopens appear in `doctor.reloadErrors`; retry with
`open <path>` or dismiss with `close <path>`. If the previous page was deleted,
dismiss before reopening. Other documents remain usable. Changes to `loader.cjs`
itself require restarting Obsidian.

Optional `python3 -m pip install .` exposes the `obsidian-tldraw` command.
