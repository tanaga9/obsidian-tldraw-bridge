# Upstream maintenance status

This is a current snapshot. Replace superseded entries and use Git for history.

## Versions and evidence

| Component | Last observed locally (2026-11-28 UTC) | Last confirmed upstream stable (2026-11-28 UTC) |
| --- | --- | --- |
| Obsidian Desktop | **1.15.1**, installer **1.15.1** (official macOS CLI) | **1.15.1** ([public release](https://obsidian.md/changelog/2026-11-12-desktop-v1.15.1/)) |
| Obsidian tldraw plugin | **1.35.1** (running manifest) | **1.35.1** ([release](https://github.com/tldraw/obsidian-plugin/releases/tag/1.35.1), [release API](https://api.github.com/repos/tldraw/obsidian-plugin/releases/latest)) |
| tldraw SDK | **5.6.0** (running library registry) | **5.6.2** standalone ([release](https://github.com/tldraw/tldraw/releases/tag/v5.6.2), [release API](https://api.github.com/repos/tldraw/tldraw/releases/latest)). Plugin 1.35.1 embeds **5.6.0** ([lockfile](https://github.com/tldraw/obsidian-plugin/blob/1.35.1/package-lock.json)). |
| Electron / Node | **43.8.9 / 24.22.1** (running process) | — |

Last upstream review: **2026-11-28T15:23:02Z**, bridge checkout `b5fe358`.
[Obsidian Connectors](https://obsidian.md/help/connectors) distributes general
vault Skills through [obsidian-skills 1.2.3](https://github.com/obsidianmd/obsidian-skills/releases/tag/1.2.3).
No Connector-specific runtime change or upgrade target was identified. The
relevant follow-up is co-installation guidance for explicit vault/path selection
and delegating tldraw Markdown mutations to bridge operations.

## Live verification

| Scope | UTC date and bridge checkout | Verified |
| --- | --- | --- |
| Broad compatibility | 2026-11-01T02:08:23Z, `478c5ce`. Obsidian 1.14.5, plugin 1.35.1, SDK 5.6.0. | Seven scripts passed after restart, covering creation, editing, styles, images, exports, sessions, and multi-page reopening. A legacy fixture preserved all 78 records across migration and reopening. |
| Rich text | 2026-11-01T02:53:11Z, `178d302` with text-operation edits. Obsidian 1.14.5, plugin 1.35.1, SDK 5.6.0. | `tests/live_rich_text.py` verified marks, lists, label separation, saved/export revision agreement, and disk reopening. |
| GUI reveal | 2026-11-03, `3185db8` changes. Obsidian 1.15.0, plugin 1.35.1, SDK 5.6.0. | `tests/live_create.py` verified closed-tab opening, tab reuse, cross-page navigation, missing targets, camera lock, oversized and clipped shapes, and preservation of document revision and bridge page. |

Focused CLI diagnostic on **2026-11-28 UTC**, checkout `b5fe358`: macOS
Obsidian/installer 1.15.1, plugin 1.35.1, SDK 5.6.0. The official CLI and bridge
listed vaults, explicit-vault `doctor` passed, and a read-only `eval` accepted
top-level `await`.
Connector co-installation and edit/save behavior were outside this diagnostic.

## Open limits

- Broad compatibility was exercised on Obsidian 1.14.5. The 1.15.0 check covered the reveal workflow.
- Wrapped or list-formatted arrow labels and auto-sized list text can clip in WebP. Separate editable text with explicit width rendered correctly. Native GUI rendering and the export root cause remain unverified.
