# obsidian-tldraw-bridge

Edit local Obsidian tldraw diagrams with an AI agent while continuing to edit the same diagrams in Obsidian. The bridge provides a CLI and a Codex plugin with a bundled Skill, without modifying the existing Obsidian tldraw plugin.

```text
Codex -> Skill -> Bridge CLI -> Official Obsidian CLI -> Dedicated Editor/Store
                                                               |
                                               Existing plugin synchronization
                                                               |
                                                Obsidian GUI and vault Markdown
```

Python 3.9.6+, a running Obsidian Desktop instance, a supported tldraw plugin, and the enabled official Obsidian CLI are prerequisites. Codex checks Python before running the bridge and notifies you if it is missing or too old.

## Compatibility policy

The bridge has no backward-compatibility guarantee. CLI commands and arguments, APIs, JSON input/output formats, and CI workflows may change without prior notice or a deprecation period. Use the documentation and help shipped with the current version when writing integrations. Contributors and agents may make breaking changes within their task's scope without separate compatibility approval; see the [development policy](docs/development.md#compatibility-policy).

## Setup

**Install the `obsidian-tldraw-bridge` plugin in Codex.**

That is the only user setup step. The plugin bundles its Skill and bridge code; no manual Skill copying, build, Python package installation, or CLI commands are required for normal use.

## Usage

Tell Codex which diagram to work on and what you want to do. For example:

> Create "Drawings/project-plan.md" in the Documents vault and draw a project schedule.

Codex runs the connectivity checks and diagram commands. The `create` command generates a new tldraw Markdown note through the existing plugin, opens it in a GUI tab and a bridge session, and returns its revision and persistence result. Existing files are rejected. If the vault cannot be identified from the conversation, Codex asks you to specify it.

## Current support

The bridge supports macOS and Obsidian tldraw plugin versions 1.31.0 and 1.32.0. Use it in a Codex environment with access to your local Obsidian app and shell.

The plugin and Skill packages are included in this repository. Installation through the Codex plugin UI and other outstanding work are recorded in [Known limitations](docs/known-limitations.md). These are accepted limitations for the current scope, not claims of completed validation.

For direct CLI use, see the [CLI reference](docs/cli.md). For builds and local marketplace registration, see [Development and distribution](docs/development.md).

## Diagramming knowledge

For a concise overview of tldraw apps, the SDK, file formats, comparisons with diagramming and slide tools, and AI agent editing, see [tldraw overview](docs/tldraw-overview.md).

The Skill includes concise [diagramming guidance](integrations/codex/skills/obsidian-tldraw/references/diagramming/index.md): a diagram selection table, project conventions, and Obsidian tldraw implementation notes. Both plugin and standalone builds include it. Familiar diagram types use established conventions rather than bundled tutorials. See [development guidance](docs/development.md) when extending these notes.

## Agent operation API

The CLI uses a shared Python operation layer with `capabilities`, compact `observe`,
named `apply` operations, and retained-request `status`. Errors distinguish edits
that were not applied, applied edits whose saving is unconfirmed, and unknown
outcomes. See the [API contract](docs/api.md) and [CLI reference](docs/cli.md).

## Advanced SDK operations

`script <path> --revision <revision> --input layout.js` runs synchronous JavaScript with access to `editor`, `app`, `plugin`, and `require`. For example:

```js
editor.alignShapes([...editor.getCurrentPageShapeIds()], 'left');
```

Edits return a compact summary containing the path, revision, selected page, net record change counts, and persistence result. Use `observe` for compact current-page context, `state` for full records, or add `--full` to `apply`, `batch`, or `script` to include them in the edit result. See the [operation reference](integrations/codex/skills/obsidian-tldraw/references/operations.md) for details. Scripts run with Obsidian's local privileges and are not sandboxed. Use code you write or review.

If synchronous code throws, the bridge restores Store records using the history mark and the pre-execution records. Asynchronous scripts and delayed edits through timers are unsupported. Rejecting a returned Promise does not cancel already scheduled work. Side effects outside the Store, such as filesystem changes, are not restored.

## Persistence and compatibility

A dedicated Editor handles bridge edits. The existing plugin's document store manager synchronizes them with the GUI and canonical Markdown. The bridge does not directly overwrite the Markdown's embedded JSON. Multiple document sessions are supported.

If the SDK has not been initialized, the bridge opens a diagram tab through the existing plugin and then returns to the previously active tab. The diagram tab remains open.

Before editing an existing document, the bridge checks a revision covering all SDK document-scope records, including document settings, pages, shapes, bindings, and assets. Stale revisions are rejected. Persistence checks compare the saved records with the Editor. Camera and selection state are excluded. Revision checks do not lock out human editing. PNG export checks the revision before and after rendering; a conflict leaves the output file unchanged.

The integration uses private APIs, so unverified plugin versions are rejected. Runtime source changes are detected on the next new request. The bridge checks persistence, closes its dedicated sessions, and reopens them with the updated runtime, restoring each selected page; Obsidian does not need to restart. A failed reopen is reported in `doctor.reloadErrors` and does not block other documents. Use `open` to retry that document or `close` to dismiss its recovery entry. Updates refuse to interrupt running work and preserve retained request IDs. Recreating sessions resets the bridge Editor’s Undo history. Reopen sessions after Obsidian restarts. Bridge and GUI Editors have separate Undo histories.

An operation or persistence timeout can occur after an edit has already been applied. For consequential changes, pass an explicit `--request-id`; the same ID and arguments retrieve the retained result without repeating the operation. Ordinary results are released after retrieval. Explicit request IDs remain in Obsidian's process without automatic expiration, up to a 128-receipt limit. New requests are rejected at capacity. Release unneeded results with `forget <request-id>`. Deduplication no longer applies after forgetting an ID or restarting Obsidian.

MCP is not implemented. The editing runtime is separate from the CLI client, leaving room for a future adapter. The repository includes a local marketplace package and a portable Skill build. Public publication and installation into user settings are separate actions.

## Testing

See the [testing guide](docs/testing.md) for automated checks, live test prerequisites, expected behavior, and cleanup. See [known limitations](docs/known-limitations.md) for outstanding work and runtime boundaries.
