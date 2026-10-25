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
[multilingual review](docs/multilingual.md#commit-review). The review itself must
not modify diagrams or metadata. Inspect and report its findings; a finding alone
does not authorize translation or checkpoint advancement.

Reflect language changes only on explicit request or existing task authorization.
After an authorized multilingual update, a separate checkpoint operation may
record the review actually performed, once both source and target pages have
been inspected for meaning and rendering and their persistence verified. This
does not require additional approval solely because the read-only review reports
changes. Preserve and report uncertain independent edits or unreviewed differences;
do not translate or advance checkpoints merely to clear review findings.
