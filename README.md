# Obsidian Tldraw Bridge

Edit local Obsidian tldraw diagrams with an AI agent while continuing to edit them in Obsidian. The bridge provides a CLI and a Codex plugin with a bundled Skill, without modifying the existing Obsidian tldraw plugin.

```text
Codex → Skill → Bridge CLI → Official Obsidian CLI → Dedicated Editor
                                                         ↕
                                               Existing plugin sync
                                                         ↕
                                               Obsidian GUI / Markdown
```

## Setup and usage

In the Codex desktop app, open the plugin browser and install **Obsidian Tldraw Bridge** from the **Obsidian Tldraw Bridge** marketplace. The plugin bundles the Skill and bridge code; no manual clone, build, or Python package installation is needed.

For first-time access, register the GitHub marketplace once, then return to the app to install:

```sh
codex plugin marketplace add tanaga9/obsidian-tldraw-bridge
```

See the [official marketplace guide](https://developers.openai.com/plugins/build/plugins#add-a-marketplace-from-the-cli).

macOS is the primary target; Windows support is also available.

Prerequisites:

- Obsidian Desktop is installed and running with the target vault open.
- The Obsidian **tldraw** plugin is installed and enabled in that vault.
- Obsidian's official CLI is enabled and available on the same computer.
- Python 3.9.6+ is available. Codex checks it before running the bridge.

Tested with tldraw 1.31.0 and 1.32.0. Other versions are allowed; the bridge checks required APIs at runtime and reports any missing functionality.

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
