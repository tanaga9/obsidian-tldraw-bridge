# obsidian-tldraw-bridge

Edit local Obsidian tldraw diagrams with an AI agent while continuing to edit them in Obsidian. The bridge provides a CLI and a Codex plugin with a bundled Skill, without modifying the existing Obsidian tldraw plugin.

```text
Codex → Skill → Bridge CLI → Official Obsidian CLI → Dedicated Editor
                                                         ↕
                                               Existing plugin sync
                                                         ↕
                                               Obsidian GUI / Markdown
```

## Setup and usage

Install the `obsidian-tldraw-bridge` plugin in Codex. It bundles the Skill and bridge code; no separate Python package installation or build is needed.

Prerequisites: macOS, Python 3.9.6+, running Obsidian Desktop with its official CLI enabled, and Obsidian tldraw plugin 1.31.0 or 1.32.0. Codex checks Python before running the bridge. Installation through the Codex plugin UI remains unverified; see [known limitations](docs/known-limitations.md).

Tell Codex the vault, diagram, and desired change. For example:

> Create "Drawings/project-plan.md" in the Documents vault and draw a project schedule.

The bridge synchronizes edits through the existing plugin and verifies persistence. Revision checks detect conflicts without locking human editing. Bridge and GUI Editors have separate Undo histories.

## Documentation

- [CLI reference](docs/cli.md): commands, note creation, connection settings, and sessions.
- [Python API](docs/api.md): shared interface for programmatic callers and future adapters.
- [Operations and recovery](integrations/codex/skills/obsidian-tldraw/references/operations.md): observation, named edits, SDK scripts, results, and retries.
- [Diagramming guidance](integrations/codex/skills/obsidian-tldraw/references/diagramming/index.md): diagram selection and drawing conventions.
- [tldraw overview](docs/tldraw-overview.md): apps, SDK, formats, tool comparisons, and AI editing.
- [Development and distribution](docs/development.md): builds, local marketplace registration, and standalone Skill packaging.
- [Testing](docs/testing.md) and [known limitations](docs/known-limitations.md): verification and runtime boundaries.

## Compatibility

CLI/API/JSON interfaces and CI may change without notice or a deprecation period. Contributors and agents may make breaking changes within the task's scope without separate compatibility approval. Use the documentation shipped with the current version; see the [compatibility policy](docs/development.md#compatibility-policy).
