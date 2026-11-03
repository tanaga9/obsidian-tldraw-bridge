# Upstream maintenance status

This is a current snapshot. Replace superseded entries and use Git for history.

## Versions and evidence

| Component | Last observed locally (2026-11-03 UTC) | Last confirmed upstream stable |
| --- | --- | --- |
| Obsidian Desktop | **1.15.0**, installer **1.14.4** (official macOS CLI) | **1.14.5** on 2026-10-31 ([release](https://obsidian.md/changelog/2026-10-22-desktop-v1.14.5/)). Predates the local observation. |
| Obsidian tldraw plugin | **1.35.1** (running manifest) | **1.35.1** on 2026-11-01 ([release](https://github.com/tldraw/obsidian-plugin/releases/tag/1.35.1), [release API](https://api.github.com/repos/tldraw/obsidian-plugin/releases/latest)) |
| Embedded tldraw SDK | **5.6.0** (running library registry) | **5.6.0** on 2026-11-01 ([release](https://github.com/tldraw/tldraw/releases/tag/v5.6.0), [release API](https://api.github.com/repos/tldraw/tldraw/releases/latest), [plugin lockfile](https://github.com/tldraw/obsidian-plugin/blob/1.35.1/package-lock.json)) |
| Electron / Node | **43.7.7 / 24.21.0** (running process) | — |

Last successful plugin/SDK release check: **2026-11-01T02:13:24Z**.
The 2026-11-03 source review used plugin 1.35.1 / SDK 5.6.0 and covered
[Obsidian integration](https://github.com/tldraw/obsidian-plugin/blob/1.35.1/README.md)
and [SDK feature coverage](https://tldraw.dev/docs/editor). Latest-release
metadata could not be refreshed. No separate upgrade target is set.

## Live verification

| Scope | UTC date and bridge checkout | Verified |
| --- | --- | --- |
| Broad compatibility | 2026-11-01T02:08:23Z, `478c5ce`. Obsidian 1.14.5, plugin 1.35.1, SDK 5.6.0. | Seven scripts passed after restart, covering creation, editing, styles, images, exports, sessions, and multi-page reopening. A legacy fixture preserved all 78 records across migration and reopening. |
| Rich text | 2026-11-01T02:53:11Z, `178d302` with text-operation edits. Obsidian 1.14.5, plugin 1.35.1, SDK 5.6.0. | `tests/live_rich_text.py` verified marks, lists, label separation, saved/export revision agreement, and disk reopening. |
| GUI reveal | 2026-11-03, `3185db8` changes. Obsidian 1.15.0, plugin 1.35.1, SDK 5.6.0. | `tests/live_create.py` verified closed-tab opening, tab reuse, cross-page navigation, missing targets, camera lock, oversized and clipped shapes, and preservation of document revision and bridge page. |

Last broad bridge diagnostic: **2026-11-01T02:13:24Z**. Checkout and rebuilt
package reported plugin 1.35.1 supported and no known update available.

## Open limits

- Broad compatibility was exercised on Obsidian 1.14.5. The 1.15.0 check covered the reveal workflow.
- Wrapped or list-formatted arrow labels and auto-sized list text can clip in WebP. Separate editable text with explicit width rendered correctly. Native GUI rendering and the export root cause remain unverified.
