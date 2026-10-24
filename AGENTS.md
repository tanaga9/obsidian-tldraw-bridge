# Project guidance

Use English by default for file names, documentation, comments, and other saved
content, unless the user requests another language or the content requires it.

CLI/API/JSON interfaces and CI may break compatibility without notice or
additional approval within the task's scope; see the
[compatibility policy](docs/development.md#compatibility-policy).

For diagram work, use the [diagramming guidance](integrations/codex/skills/obsidian-tldraw/references/diagramming/index.md).

For tldraw diagrams used in this repository's documentation:

- Update the editable tldraw note and its referenced preview images together.
- Export previews as WebP and inspect readability at the intended display size.
- Keep intermediate previews in a temporary directory, outside tracked documentation.

Maintain canonical Skill sources under `integrations/codex/skills/obsidian-tldraw/`;
`plugins/obsidian-tldraw-bridge/` is generated. Follow the
[development guide](docs/development.md) when extending the guidance or rebuilding
packages, and the [testing guide](docs/testing.md) for appropriate checks.

Before committing changed tldraw Notes, use the read-only
[multilingual review](docs/multilingual.md#commit-review). Inspect and report
findings; do not translate or advance checkpoints merely to clear the review.
Reflect language changes only on explicit request or existing task authorization.
