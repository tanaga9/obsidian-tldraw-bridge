# Testing

This guide describes how to verify the current implementation. Keep test procedures and expected behavior here; use Git history for past changes and [Known limitations](known-limitations.md) for implementation boundaries. Do not append dated execution logs or cumulative pass counts.

Run commands from the repository root, using the selected Python environment.
macOS is the primary target; examples use `python3` or the selected environment's
absolute interpreter path. On Windows, substitute a verified Python 3.9.6+ command
such as `python` or `py -3` in PowerShell.

## Automated checks

Use Python 3.9.6+ and Node.js 22. CI tests Python 3.9, 3.10, and 3.13 on Linux, macOS, and Windows; 3.9 jobs use the latest available patch release for each runner. The macOS 3.9 job uses `macos-15-intel` because the [official Python distribution manifest](https://github.com/actions/python-versions/blob/main/versions-manifest.json) has no CPython 3.9 build for macOS arm64; newer Python jobs use `macos-latest`. To verify the minimum supported version on a Mac where `/usr/bin/python3 --version` reports 3.9.6, run the Python checks below with `/usr/bin/python3` instead of `python3`. Node.js is a developer test dependency, not a requirement for normal plugin use.

```sh
python3 -m unittest discover -s tests -p 'test_*.py'
node --test
node --check src/obsidian_tldraw_bridge/runtime/bridge.cjs
node --check src/obsidian_tldraw_bridge/runtime/loader.cjs
python3 scripts/build_plugin.py --check
```

Node discovers `*.test.cjs` files without shell wildcard expansion, so the same
command works in POSIX shells and PowerShell. Tests use platform temporary
directories; preview test outputs do not require `/tmp` or elevated privileges.

These checks do not require a running Obsidian instance. They cover:

| Area | Expected behavior |
| --- | --- |
| Multilingual pages | Read-only per-diagram freshness, content-signature versus presentation changes, asset changes, missing/duplicate identities, source handoff, legacy asset-baseline uncertainty, locale-independent current fingerprints, missing tldraw start markers in index/worktree versions, reviewed checkpoint validation/rollback/persistence/replay, and independent staged/working-tree review. No translation or shape changes from inspection/checkpointing. |
| Agent operation API | Shared validation before connecting; named edit schemas; scoped, bounded observations and revision-pinned pagination; structured failures and non-executing receipt queries. |
| Freehand drawing | Authored curves preserve geometry and pressure through point encoding; closed strokes accept fill and opacity in the same edit. Redraws reset omitted styles and preserve unrelated shapes. Invalid styles, open fills, and targets fail before edits. |
| Image insertion | PNG/WebP/JPEG bytes are preserved by default. Read-only size reports, opt-in pixel resizing/WebP conversion, optional byte limits and animation protection are checked. Invalid data, ID collisions, and stale revisions/pages do not add records. Asset/shape creation shares a rollback boundary; request replay does not duplicate an insertion. |
| CLI transport | CLI output is captured in temporary regular files with independent reader/writer positions; concurrent inherited writes preserve the response; completion and timeout do not wait for inherited descendant output handles. A short, shell-free argv bootstrap reads a closed UTF-8 evaluation file; code size and content do not expand argv. Receiver cleanup failure does not block evaluation; pre-launch failures discard unsent files and final timeout diagnostics list all tracked remaining files. Acknowledged returns also trigger sender cleanup, while uncertain delivery retains unread files. Missing initial output can be recovered by polling. UTF-8 process responses, input files/stdin (with or without a UTF-8 BOM), and JSON stdout/stderr preserve Unicode independently of the locale. Invalid response encoding retains unknown outcome and request identity. |
| Vault enumeration | Official CLI names/paths retain duplicate names and Unicode; plugin installation is separate from activation. Missing/incomplete/unreadable files, alternate config folders, invalid output, CLI failure, global argument validation and stdout failure preserve read-only outcomes. |
| Connection setup | Mocked macOS/Windows discovery without symlink privileges, explicit override precedence, Windows console selection, name/ID validation, wrong-vault rejection before runtime evaluation, staged doctor errors, disabled CLI detection, and a remaining-budget deadline shared by dispatch, polls and cleanup. Untested plugin versions are allowed; missing plugin, Editor, and operation APIs are reported by name, with edits rejected before execution where possible. |
| Style discovery | Document-specific installed StyleProps, enum extensions, separate defaults and next-shape styles; unavailable/unsupported/empty distinctions; no edits, history marks or file writes. |
| Script results | Detached JSON data in compact/full results; UTF-8 byte/depth limits; invalid-result rollback without getter/toJSON execution; persistence failure details, explicit-ID replay and CLI output recovery. |
| Result handling | Edits default to compact net change counts over document records; full output is available explicitly, and state remains inspectable. Automatic receipts are released; explicit request IDs retain their results. Cleanup failures do not hide successful operations. |
| Note creation | Plugin-generated Markdown, existing-path and traversal rejection, saved editable session, retained creation after initialization failure, and request replay without duplicate creation. A live Editor avoids opening GUI tabs. Initialization does not override a user tab switch or reopen a closed tab; captured SDK construction data remains usable after the seed tab closes. |
| Revisions and persistence | All SDK document-scope records participate in revision and persistence checks. Session records do not affect the revision. Pending GUI/source/shared notifications are reconciled before reads and revision checks without waiting for animation frames. Edits superseded during persistence return SAVE_CONFLICT; previews reject queued GUI changes during export. |
| Synchronous rollback | Failed edits restore records, including history-ignored changes, without leaving forward changes queued for other Editors. |
| Exceptions | Arbitrary thrown values become failed jobs with readable errors; subsequent requests remain usable. |
| Preview | WebP defaults, explicit PNG export, format/quality validation, and encoder fallback checks. Part and ID selections export only current-page shapes at the requested scale. Bounds crop the whole page with surrounding shapes. Invalid selections, bounds, and revision conflicts leave output files unchanged. |
| Receipt capacity | The limit rejects new work while preserving retained results and their deduplication protection. |
| Runtime updates | Changed source replaces the cached runtime after persistence checks and reopens sessions with their selected pages restored. Failed reopens are isolated and reported by doctor; retry and dismissal remain available. Retained request IDs remain deduplicated. Busy runtimes, save failures and invalid updates do not interrupt editing. Missing or non-function runtime exports are rejected before closing sessions; corrected code can load without restarting. |
| Packaging | The bundled CLI runs outside the source checkout, references resolve, and generated plugin files match canonical sources. Builders preserve UTF-8 source bytes, generate the manifest with LF line endings, and exclude `.DS_Store` recursively; metadata differences are ignored during consistency checks while real source changes are still detected. |

CLI response tests cover LF and CRLF framing while preserving U+0085, U+2028,
and U+2029 inside JSON strings, including dispatch, result polling, and retained
request status.

Output-failure tests cover full disks, broken pipes, write/flush failures, and
encoding errors after successful execution. Completed results and explicit request
IDs remain available in diagnostics; read-only commands and status queries do not
claim that the underlying edit was applied. Input-file errors remain unapplied.

If the plugin package is stale, regenerate it with `python3 scripts/build_plugin.py` and run the checks again. CI runs the automated checks; it does not run Obsidian integration tests.

## Live test setup

Use macOS with Python 3.9.6+, running Obsidian Desktop, its enabled official CLI,
and the tldraw plugin enabled. Versions 1.31.0 and 1.32.0 have been tested;
other versions are allowed when the required APIs are available. Windows can also run these checks; its command
substitutions are shown below. If CLI discovery fails, update the Obsidian
installer or select the actual official CLI path; do not point at the GUI.

Choose the registered vault explicitly. `--vault` accepts its name or ID, not a
filesystem path. The examples use a vault named `Documents`; substitute the
user's chosen registered vault. `doctor` uses automatic CLI discovery:

macOS, using a suitable `python3` environment:

```sh
python3 --version
python3 bridge.py --vault 'Documents' doctor
python3 tests/live_transport.py --vault 'Documents'
```

To list registered vaults when PATH registration is absent on macOS:

```sh
'/Applications/Obsidian.app/Contents/MacOS/obsidian-cli' vaults verbose
```

For Windows, use PowerShell and the console executable `Obsidian.com`. From the
selected Python environment, the equivalent commands are:

```powershell
$bridgePython = 'python' # Or the absolute path to the selected python.exe.
& $bridgePython --version
& $bridgePython bridge.py --vault 'Documents' doctor
& $bridgePython tests/live_transport.py --vault 'Documents'
```

Both sequences end with the self-contained transport check described below.
For a standard per-user Windows installation without PATH registration:

```powershell
& "$env:LOCALAPPDATA\Programs\Obsidian\Obsidian.com" vaults verbose
```

For a custom installation, pass `--obsidian` to the bridge or set `OBSIDIAN_CLI`
in the current shell. The environment variable also works for live scripts that
have no `--obsidian` option. See [connection diagnostics](../integrations/codex/skills/obsidian-tldraw/references/operations.md#cli-discovery-and-connection-diagnostics).

Before tests that take `--path`, create a dedicated tldraw Markdown test diagram
using the existing plugin. Their examples assume `Bridge test diagram.md`.
These tests edit that diagram or temporary copies; do not use a production note.
Scripts that create their own notes are identified below. PNG-producing scripts
default to the OS temporary directory; an explicit `--output` must have an
existing parent. Preview files remain available for visual inspection.

## Evaluation transport integration check

```sh
python3 tests/live_transport.py --vault Documents
```

Pass `--obsidian <official-CLI-executable>` when explicit CLI selection is needed.
Creates its own temporary note and verifies a large Unicode `apply` payload and
script containing quotes, newlines and backslashes, saved records, recovery after
lost dispatch output, retained-ID replay, changed-request rejection, and short CLI
bootstrap arguments. Removes its temporary note, session and consumed evaluation
files. This opt-in check requires a running Obsidian instance and supported tldraw;
it is separate from the automated Node-based transport checks.

## Style discovery and script result integration check

```sh
python3 tests/live_styles.py --vault obsidian-tldraw-bridge
```

Choose the intended registered vault explicitly. Creates its own unique temporary
note in `workspace/drawings/` and uses isolated runtime/loader copies. Checks real
SDK fill/dash enums, default versus next-shape style, unchanged records/revision
and Markdown during discovery, compact/full script results, retained replay/status,
invalid-result rollback in shared records and persistence, and saved edits with
results. It removes its note and closes its session. No production diagram is
edited. The CLI/API adapter contract is also covered by the automated tests.

## Freehand integration check

```sh
python3 tests/live_freehand.py --vault Documents --path 'Bridge test diagram.md'
```

Uses an existing dedicated test note. Creates a uniquely named frame and two strokes (including a translucent filled region), verifies redraw isolation, persistence, replay, stale revisions, invalid targets, a detail PNG, and a context crop with exact dimensions and unchanged document revision, then removes its frame and strokes and closes its session. Inspect the images separately for visual quality.

## Image insertion integration check

```sh
python3 tests/live_images.py --vault Documents
```

Creates real PNG/WebP/JPEG fixtures with the installed browser's canvas encoders,
then inserts them through the CLI and shared Python API. Verifies persistence,
cross-adapter request replay, read-only inspection, opt-in resizing/conversion,
source preservation, byte-limit/corrupt-input rejection, reopening, explicit PNG
preview, default API WebP export, and CLI WebP with a quality override. Real WebP previews are decoded with the
browser to verify output dimensions; previews must leave the document unchanged. The generated fixture note and session are removed. The preview remains
in the OS temporary directory (or the supplied `--output` path) for visual QA.
No third-party Python imaging library is needed.

## Note creation integration check

```sh
python3 tests/live_create.py --vault Documents
```

This check creates a uniquely named folder and Markdown note through `create`, verifies an empty editable document, request replay, duplicate rejection, and a named saved shape edit, compact observation, capabilities, retained status, structured stale-revision rejection, full-state inspection, position edits from compact observations, five deferred-GUI conflict rejections, and a GUI change injected during saving, then closes the session and removes its temporary note and folder. It uses fresh runtime and loader copies so cached code does not affect the check.

## Runtime reload integration check

Against an existing dedicated test diagram, run:

```sh
python3 tests/live_reload.py --vault Documents --path 'Bridge test diagram.md'
```

The check loads a temporary runtime, changes its source at the same path, and verifies automatic session recreation, unchanged document records and revision, initialized text options, and replay of a retained request ID. It does not add or remove shapes in this mode. The loader is also copied to a fresh path so the check always exercises the code on disk.

To verify that an edit after reload targets the previously selected second page, use:

```sh
python3 tests/live_reload.py --vault Documents --path 'Bridge test diagram.md' --multi-page-copy
```

This mode creates a temporary diagram copy, selects a new second page, reloads the runtime, and checks the parent page of a newly created shape. The copy is deleted after the check; the source diagram is not edited.

## Single-document integration test

```sh
python3 tests/live.py --vault Documents --path 'Bridge test diagram.md'
```

The test loads a fresh runtime copy to avoid stale Obsidian require cache entries. It verifies:

- Shape creation, update, deletion, and Markdown persistence.
- Rich-text labels rendered with the GUI Editor's inherited text options.
- Idempotent retry and stale-revision rejection.
- Undo and Redo.
- Successful synchronous SDK scripts and document-settings edits.
- Restoration after failed shape/settings edits and arbitrary exception values.
- Shared main Store records and Markdown persistence immediately after each failure, before a successful edit could conceal an incorrect rollback.
- PNG output with a valid file signature. Inspect the image separately to check its appearance.

A passing test exits with code 0 and prints the completed checks and preview path. It removes its UUID-named shape, restores the original grid size, and closes its dedicated session during cleanup.

## Multiple-document integration test

```sh
python3 tests/live_sessions.py --vault Documents --path 'Bridge test diagram.md'
```

This test creates a temporary copy of the diagram, opens both documents, and verifies that an edit to the copy is saved without changing the original session's revision. It then closes both sessions and removes the temporary Markdown file.

This script uses the normal runtime path, where runtime source updates are detected automatically. Restart Obsidian when testing changes to the loader itself, since Node caches that module.

## Cleanup and manual validation

Inspect exported PNGs for text, curves, fill and cropping. To check GUI
synchronization, edit the dedicated test note in the GUI and confirm the change
through the bridge, then confirm a saved bridge edit appears in the GUI and
Markdown.

After live tests, confirm that temporary shapes and documents are gone, the original grid size is restored, and dedicated sessions are closed. Compare persistent diagram records with the pre-test baseline when validating cleanup. A failed test can also fail during cleanup; inspect its output and the diagram before rerunning it.

See [Known limitations](known-limitations.md) for implementation boundaries,
including asynchronous scripts, external side effects, file lifecycle changes,
and runtime updates.

## Diagramming guidance evaluation

For changes to drawing decisions rather than runtime behavior, use the
[diagramming evaluation kit](evaluations/diagramming/README.md). It provides
three fixed prompts, a partial-edit setup fixture, a pinned guide baseline,
viewing conditions, and a staged comparison rubric. Both arms use the same frozen
current package and recorder; preflight their evidence captures before timing.
Package checks establish distribution
integrity; this separate evaluation is needed to establish drawing-quality gains.

Inspect whether required facts and useful existing content survive the
check–revise loop, and whether refinement is followed by another inspection and
confirmed saving. A successful first candidate need not demonstrate a forced
retry. This is a maintainer comparison procedure, not an extra completion step
for ordinary drawing requests.

The [maintenance paths](evaluations/diagramming/README.md#choose-the-maintenance-path)
separate local diagnosis from comparative guide evaluation. The repository-only
`scripts/diagramming_eval.py` records trial timing and CLI calls and checks exact
shape/binding preservation against frozen scope. Its automated tests are
`tests/test_diagramming_eval.py`; they do not establish visual or semantic quality.
Read those judgments from independent preview review, keeping task, affected
quality, and preservation verdicts separate.

Recorder regression checks also cover stale/cross-trial review rejection,
frozen-artifact integrity, export-image SHA-256 matching (including missing hashes
and image replacement before or during review preparation), matching final/preview/saved revisions (including rejection
of missing or stale saved revisions in otherwise valid bundles), and required
property preservation inside otherwise editable records. A valid review bound
to a changed label or reconnected binding cannot override a property violation.

## Multilingual integration check

```sh
python3 tests/live_languages.py --vault obsidian-tldraw-bridge
```

Creates its own temporary Note with English and Japanese pages using an isolated
runtime. Verifies metadata-only adoption, read-only status and unchanged selected
page, retained replay, presentation review, layout checkpointing, content-change
rejection for layout acknowledgement, and persistence. It removes its temporary
Note and closes its session. No production diagram or preview is edited.

This live check covers two languages of one logical diagram. Runtime unit tests
exercise three-language checkpoint handoff, a third language retaining an old
source lineage, pair-specific layout acknowledgement, and preservation of a
separate diagram's records and checkpoints. They also cover dictionary-like IDs
such as `toString` without treating inherited properties as saved registration.
These tests do not establish real SDK behavior for every multi-diagram or
three-language editing/retirement sequence; keep this scope explicit.

The Git-review regression also checks repair of a malformed historical Note:
valid current data receives full diagram inspection with a baseline warning,
while malformed current data still fails in either index or working-tree mode.
