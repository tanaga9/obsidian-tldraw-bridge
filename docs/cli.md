# CLI reference

The CLI adapts the shared [Python API](api.md). Agents use the bundled Skill;
no separate CLI installation is needed. Interfaces may change without notice;
use this version's `--help` and [compatibility policy](development.md#compatibility-policy).

## Example

Run from the repository root with the selected Python 3.9.6+ environment.
Examples target macOS and use `python3`; use the selected environment's absolute
interpreter path when needed. On Windows, substitute a verified Python 3.9.6+
command such as `python` or `py -3`; in PowerShell, invoke a quoted interpreter
path with `&`. Create a note, then observe its revision and page:

```sh
python3 bridge.py --vault Documents doctor
python3 bridge.py --vault Documents capabilities
python3 bridge.py --vault Documents --request-id create-example create 'Drawings/example.md'
python3 bridge.py --vault Documents observe 'Drawings/example.md'
python3 bridge.py --vault Documents style-spec 'Drawings/example.md' --shape-type geo
```

Substitute the observed revision and `currentPageId` below. Use the returned path
if creation chose a unique filename.

Save the operations as a UTF-8 file named `operations.json` (a UTF-8 BOM is also
accepted). Using a file avoids shell-specific multiline quoting:

```json
[{"op":"createShapes","shapes":[
  {"id":"shape:bridge-example","type":"geo","x":100,"y":100,
   "props":{"geo":"rectangle","w":240,"h":120,"color":"blue","fill":"solid"}}
]}]
```

```sh
python3 bridge.py --vault Documents --request-id edit-example apply 'Drawings/example.md' --revision '<revision-from-observe>' --page-id '<currentPageId>' --input operations.json
python3 bridge.py --vault Documents preview 'Drawings/example.md' --output example.webp
python3 bridge.py --vault Documents close 'Drawings/example.md'
```

Preview output paths are local filesystem paths, resolved against the process's
working directory; their parent directory must exist. They are separate from
vault-relative diagram paths.

Specify the vault for every command except `vaults`; diagram paths are vault-relative `.md` paths. `apply`,
`batch`, `freehand`, and `script` accept `--input -` for standard input. Results
are JSON; handled errors are JSON on standard error with exit code 1.

## Choosing a vault

List registered vaults and their on-disk tldraw installation status without
selecting or opening any vault:

```sh
python3 bridge.py vaults
```

The JSON `vaults` array preserves each registration's `name` and absolute `path`,
including duplicate names. Each entry adds a `tldraw` object:

```json
{"status":"installed","version":"1.32.0","enabled":true,"configDir":"/path/to/vault/.obsidian","source":"filesystem"}
```

`status` is `installed` (valid tldraw manifest and main.js present),
`not_installed` (no plugin folder in the inspected configuration), `incomplete`
(missing/invalid installation files), or `unknown` (unavailable paths/permissions).
`reason` explains incomplete/unknown results. `enabled` separately reads
`community-plugins.json`: true/false means listed/not listed; null plus
`enabledReason` means it could not be read or parsed. A missing activation file
means false. If the vault/config folder itself cannot be inspected, enabled is
null and `reason` explains why. This reports saved configuration, not whether a
plugin is loaded, trusted, or compatible; use `doctor` on a selected vault for that.

The default inspected configuration folder is `.obsidian`. Alternate configuration
folders are explicit: `python3 bridge.py vaults --config-dir .custom` inspects that
folder in each listed vault. The command does not discover which configuration
folder a running Obsidian window uses. It never loads plugin code or writes files.
`--obsidian`/`OBSIDIAN_CLI` and `--timeout` also work; `--vault` and `--request-id`
are rejected for this read-only global command. A failed official CLI enumeration
returns `VAULT_DISCOVERY_FAILED`, not an empty successful list. Individual vault
inspection failures remain in the list without hiding other vaults.

Enumeration uses the [official Obsidian CLI](https://obsidian.md/help/cli#vaults)
`vaults verbose` command. Use it directly for connection diagnostics if needed:

```sh
obsidian vaults verbose
```

Pass a registered name or ID to `--vault` for subsequent operations; filesystem
paths are rejected. Match a supplied path to its registered entry. This command
lists registered vaults rather than searching the filesystem for every vault.

When multiple vaults exist and the target is at all uncertain, agents must ask
before running vault-scoped commands. Offer candidates ordered by estimated
likelihood, with distinguishing paths; wait for the user's selection. An active
vault or a high-ranked candidate does not replace confirmation. Reuse an explicit
choice for the same task. If discovery fails, ask rather than guessing.

## Commands and contracts

[Operations and recovery](../integrations/codex/skills/obsidian-tldraw/references/operations.md)
is the canonical reference for input schemas, observation/pagination, coordinates,
SDK access, result fields, errors, persistence, and request-ID recovery.

| Purpose | CLI usage |
| --- | --- |
| Vaults and tldraw status | `vaults [--config-dir <folder-name>]`; no `--vault` |
| Installed style specification | `style-spec <path> --shape-type <type>`; the document must already be open |
| Compact observation | `observe <path> [--ids <id> ... \| --bounds X Y W H] [--limit N]`; continue with `--offset N --revision <revision> --page-id <currentPageId>` |
| Full records | `state <path>`; add `--full` to `apply`, `batch`, `script`, or `freehand` for full edit results |
| Freehand drawing | `freehand <path> --revision <revision> --input <file>`; see [drawing input](../integrations/codex/skills/obsidian-tldraw/references/freehand.md) |
| Inspect an image | `image-info --file <image> [--max-dimension N --format webp --quality Q]` |
| Insert PNG/WebP/JPEG | `insert-image <path> --revision <revision> --file <image> [--x X --y Y --width W --height H]` |
| PNG/WebP preview | `preview <path> --output <image> [--format png\|webp] [--quality <0–1>] [--part <part> \| --ids <id> ...] [--scale <number>]`; WebP and scale 1 are defaults, maximum scale 4 |
| Check persistence | `saved <path>` |
| Inspect/release a receipt | `status <request-id>` / `forget <request-id>` |

Use a fresh global `--request-id` for each consequential edit. After a timeout,
inspect its status or repeat the identical request with the same ID. Release
completed receipts with `forget`; explicit IDs occupy the 128-receipt capacity
until forgotten or Obsidian restarts.

`script` returns `scriptResult` in both normal and `--full` output, beside the
change summary and persistence result. `return {value:42}` yields
`{"hasValue":true,"value":{"value":42}}`. JSON data is validated and detached
inside the Store rollback transaction, with limits of 64 KiB UTF-8 and 32 nested
containers. Invalid/oversized results fail with Store restoration. See
[script results](../integrations/codex/skills/obsidian-tldraw/references/operations.md#script-results)
for type restrictions, retained results, and failure recovery.

## Note creation

`create <path.md>` uses the plugin's current frontmatter, tags, and serialization
settings, creates parent folders as needed, and opens a bridge session.
It reuses a live GUI Editor for initialization; a new GUI tab is needed only
when no live Editor is available.
No revision is required. The result includes `created`, `path`, `requestedPath`,
`currentPageId`, `revision`, records, and `persistence`; use its actual path and revision.

Existing files or folders are rejected. A concurrent name collision may make the
plugin choose a unique filename. Use `open <path>` for existing notes. If creation
succeeds but opening or persistence verification fails, the error identifies the
retained note: recover with `open` and `saved`. The bridge does not delete it.

## Image insertion

Inspect an image's size before inserting it (Obsidian must be running; no
diagram session or revision is needed):

```sh
python3 bridge.py --vault Documents image-info --file '/path/to/photo.png'
python3 bridge.py --vault Documents image-info --file '/path/to/photo.png' --max-dimension 1600 --format webp --quality 0.85
```

The report contains `source` and `output` MIME types, pixel dimensions and byte
counts, plus `output.dataUrlBytes`: the embedded data URL's exact byte count,
excluding surrounding Markdown/JSON. Processing is performed in memory without
editing a note or writing a converted file. Then open the diagram and insert
with its observed revision and the same processing options if desired:

```sh
python3 bridge.py --vault Documents --request-id insert-photo insert-image 'Drawings/example.md' --revision '<revision-from-observe>' --file '/path/to/photo.webp' --x 80 --y 120 --width 480
```

`--file` accepts local PNG, WebP and JPEG (`.jpg` / `.jpeg`); actual bytes determine
the format. Original bytes are preserved by default. These options are explicit:

- `--max-dimension N` shrinks pixels to fit within an N-pixel longest edge, without upscaling.
- `--format webp` re-encodes as WebP; `--quality Q` sets quality from 0 to 1 (default 0.85 when encoding WebP).
- `--max-bytes N` rejects output exceeding N image bytes **before** Base64 encoding. There is no default limit.

These options work with both commands. Reducing display `--width` or `--height`
alone does not reduce encoded pixels or file size. Resize without conversion
keeps the image format; re-encoding may discard image metadata. Animated images
can be embedded unchanged but cannot be resized or converted by this command.
Conversion does not guarantee smaller output; inspect the byte counts first.

The inserted data URL is stored in the note, so the original file can be moved
afterward. No attachment file is created and the source file is never modified.

Coordinates default to `(0, 0)` on the current page. `--parent-id <shape-id>`
places the image under a current-page shape (normally a frame); coordinates
then use that parent's local space. `--page-id` pins the current page.
Omitting both dimensions uses the decoded image's natural size; supplying one
preserves its aspect ratio. Supplying both sets the exact display dimensions.

The result includes `shapeId`, `assetId`, display `width`/`height`, `mimeType`, an
`image` report in the same format as `image-info`, and the
usual revision, change counts, and persistence result. `--shape-id` can assign
a new stable ID; an existing ID is rejected without replacing its shape.
`--full` includes document records. Use the same request ID and unchanged file
contents to recover an uncertain insertion without creating a duplicate.

The browser decodes the image before editing. Invalid images leave the document
unchanged, and revisions and page selection are checked again after decoding.

## Connection and sessions

Use `--obsidian <official-CLI-executable>` or `OBSIDIAN_CLI` to override
CLI discovery. The flag takes precedence; an invalid override fails without
silently selecting another installation. On macOS, discovery checks `obsidian`
and `obsidian-cli` on PATH, then
`/Applications/Obsidian.app/Contents/MacOS/obsidian-cli`. Legacy GUI registrations
select the CLI in the same app bundle.

On Windows, use `Obsidian.com`; an explicit `Obsidian.exe` is rejected. Discovery
uses PATH registrations and standard Windows installation locations.
See [CLI discovery and connection diagnostics](../integrations/codex/skills/obsidian-tldraw/references/operations.md#cli-discovery-and-connection-diagnostics)
for the exact search order, diagnostic codes and timeout contract.

Run `doctor` before the first edit. It reports checks for the CLI executable,
evaluation connection, vault identity, plugin and runtime. Failures identify the
stage in `error.details.stage`. A connection error can also reflect restricted
local IPC permissions; it does not by itself prove the app is stopped. For
OS-specific commands and live checks, see [live test setup](testing.md#live-test-setup).

`--timeout` is a shared client wait budget, not cancellation in Obsidian. A
retained request may still run after the CLI process times out. Recover using
`status` and the same request ID before repeating an uncertain edit.

Multiple document sessions are supported. SDK initialization reuses a live GUI
Editor or opens one diagram tab when necessary. It does not restore focus or
reopen a tab closed by the user. If the tab closes before its Editor can be
captured, initialization stops; any newly created note is retained for recovery.
After initialization, GUI tabs may be closed or switched without ending the
bridge session. Showing a result in Obsidian is separate from creating or editing it.
Bridge and GUI Editors have separate Undo histories. Reopen sessions after an
Obsidian restart.

Runtime source updates check persistence and recreate sessions, preserving selected
pages and retained request IDs, but resetting bridge Undo history. Running work
is not interrupted. Failed reopens appear in `doctor.reloadErrors`; retry with
`open <path>` or dismiss with `close <path>`. If the previous page was deleted,
dismiss before reopening. Other documents remain usable. Changes to `loader.cjs`
itself require restarting Obsidian.

Optional `python3 -m pip install .` exposes the `obsidian-tldraw` command.

## WebP preview

```sh
python3 bridge.py --vault Documents preview 'Drawings/example.md' --format webp --quality 0.9 --output example.webp
```

WebP is the default, at quality 0.9. Use `--format png` for lossless PNG output.
Format is not inferred from the filename. `--quality` accepts 0–1 for WebP
(including when `--format` is omitted) and is rejected with `--format png`.
Selection, bounds, scale, and revision checks work with both formats. The result
includes `format`; output remains unchanged on render or revision failures.
