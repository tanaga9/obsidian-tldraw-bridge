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
python3 bridge.py --vault Documents preview 'Drawings/example.md' --output example.png
python3 bridge.py --vault Documents close 'Drawings/example.md'
```

Preview output paths are local filesystem paths, resolved against the process's
working directory; their parent directory must exist. They are separate from
vault-relative diagram paths.

Always specify the vault; diagram paths are vault-relative `.md` paths. `apply`,
`batch`, `freehand`, and `script` accept `--input -` for standard input. Results
are JSON; handled errors are JSON on standard error with exit code 1.

## Choosing a vault

The [official Obsidian CLI](https://obsidian.md/help/cli#vaults) lists known vaults
without selecting a target:

```sh
obsidian vaults verbose
```

`vaults` lists names; `verbose` includes paths. Pass a registered name or ID to
`--vault`; filesystem paths are rejected. If the user identifies a vault by path,
match it to the registered entry before calling the bridge. Use the executable resolved by
[connection discovery](#connection-and-sessions) if `obsidian` is not registered
on PATH. This is an official CLI command, not a bridge subcommand; it lists known
vaults rather than searching the filesystem for every vault.

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
settings, creates parent folders as needed, and opens a bridge session.
It reuses a live GUI Editor for initialization; a new GUI tab is needed only
when no live Editor is available.
No revision is required. The result includes `created`, `path`, `requestedPath`,
`currentPageId`, `revision`, records, and `persistence`; use its actual path and revision.

Existing files or folders are rejected. A concurrent name collision may make the
plugin choose a unique filename. Use `open <path>` for existing notes. If creation
succeeds but opening or persistence verification fails, the error identifies the
retained note: recover with `open` and `saved`. The bridge does not delete it.

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
