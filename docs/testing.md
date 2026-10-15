# Testing

This guide describes how to verify the current implementation. Keep test procedures and expected behavior here; use Git history for past changes and [Known limitations](known-limitations.md) for outstanding work. Do not append dated execution logs or cumulative pass counts.

Run commands from the repository root.

## Automated checks

Use Python 3.10+ and Node.js 22, matching the CI configuration. Node.js is a developer test dependency, not a requirement for normal plugin use.

```sh
python3 -m unittest discover -s tests -p 'test_*.py'
node --test tests/*.test.cjs
node --check src/obsidian_tldraw_bridge/runtime/bridge.cjs
node --check src/obsidian_tldraw_bridge/runtime/loader.cjs
python3 scripts/build_plugin.py --check
```

These checks do not require a running Obsidian instance. They cover:

| Area | Expected behavior |
| --- | --- |
| CLI transport | Code is passed as an argument rather than through a shell. Missing initial output can be recovered by polling. |
| Result handling | Automatic receipts are released; explicit request IDs retain their results. Cleanup failures do not hide successful operations. |
| Note creation | Plugin-generated Markdown, existing-path and traversal rejection, saved editable session, retained creation after initialization failure, and request replay without duplicate creation. |
| Revisions and persistence | All SDK document-scope records participate in revision and persistence checks. Session records do not affect the revision. Pending source/shared notifications are processed without waiting for animation frames. |
| Synchronous rollback | Failed edits restore records, including history-ignored changes, without leaving forward changes queued for other Editors. |
| Exceptions | Arbitrary thrown values become failed jobs with readable errors; subsequent requests remain usable. |
| Preview | Changes during image generation reject the export without replacing an existing output file. |
| Receipt capacity | The limit rejects new work while preserving retained results and their deduplication protection. |
| Runtime updates | Changed source replaces the cached runtime after persistence checks and reopens sessions with their selected pages restored. Failed reopens are isolated and reported by doctor; retry and dismissal remain available. Retained request IDs remain deduplicated. Busy runtimes, save failures and invalid updates do not interrupt editing. |
| Packaging | The bundled CLI runs outside the source checkout, references resolve, and generated plugin files match canonical sources. |

If the plugin package is stale, regenerate it with `python3 scripts/build_plugin.py` and run the checks again. CI runs the automated checks; it does not run Obsidian integration tests.

## Note creation integration check

```sh
python3 tests/live_create.py --vault Documents
```

This check creates a uniquely named folder and Markdown note through `create`, verifies an empty editable document, request replay, duplicate rejection, and a saved shape edit, then closes the session and removes its temporary note and folder. It uses fresh runtime and loader copies so cached code does not affect the check.

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

## Live test prerequisites

Use macOS with Python 3.10+, running Obsidian Desktop, the enabled official CLI, and a supported tldraw plugin version. Create a dedicated tldraw Markdown test diagram using the existing plugin. Do not use a production diagram.

Specify the vault and its relative diagram path explicitly. The examples below assume a vault named `Documents` and an existing file named `Bridge test diagram.md`.

## Single-document integration test

```sh
python3 tests/live.py --vault Documents --path 'Bridge test diagram.md' \
  --output /tmp/obsidian-tldraw-test.png
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

After live tests, confirm that temporary shapes and documents are gone, the original grid size is restored, and dedicated sessions are closed. Compare persistent diagram records with the pre-test baseline when validating cleanup. A failed test can also fail during cleanup; inspect its output and the diagram before rerunning it.

Automated checks and SDK integration tests do not establish that plugin UI installation or mouse-driven GUI editing works end to end. Validate those workflows separately. Private API compatibility also requires a live run against each plugin version being evaluated. See [Known limitations](known-limitations.md) for current boundaries, including asynchronous scripts, external side effects, file lifecycle changes, and runtime updates.
