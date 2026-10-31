# Upstream maintenance status

Last checked: **2026-10-31T08:22:07Z** (UTC).
Scope: stable-release research, tagged-source comparison and read-only diagnostics.
This record was shortened without rerunning checks; confirmation dates are unchanged.

## Versions and evidence

| Component | Local observation | Latest stable / review target | Evidence |
| --- | --- | --- | --- |
| Obsidian Desktop | App **1.14.5**, installer **1.14.4** | **1.14.5**, published 2026-10-22 | CLI `version`; [public release](https://obsidian.md/changelog/2026-10-22-desktop-v1.14.5/) |
| Obsidian tldraw plugin | **1.32.0**, enabled in the repository vault | **1.35.1**, published 2026-10-29T06:40:40Z | Local/runtime manifests and `doctor`; [release API](https://api.github.com/repos/tldraw/obsidian-plugin/releases/latest), [target release](https://github.com/tldraw/obsidian-plugin/releases/tag/1.35.1) |
| Embedded tldraw SDK | **5.4.0** | **5.6.0**, also latest SDK stable; published 2026-10-28T15:01:24Z | Installed bundle registrations; target [lockfile](https://github.com/tldraw/obsidian-plugin/blob/1.35.1/package-lock.json); [SDK release](https://github.com/tldraw/tldraw/releases/tag/v5.6.0), [release API](https://api.github.com/repos/tldraw/tldraw/releases/latest) |
| Electron / Node inside Obsidian | **43.7.7 / 24.21.0** | Public 1.14.5 release describes Electron **43.8.3**; target Node unverified | Read-only `process.versions`; official Desktop release above |

Target combination: latest stable Desktop/installer and plugin above, with its
embedded SDK. Obsidian 1.15.0 was Catalyst and excluded. The fetched GitHub
release-list page showed plugin 1.35.0; direct API metadata confirmed 1.35.1.
Installed plugin build provenance beyond manifest/SDK identifiers is unknown.

## Verification scope

- Bridge checkout: `afa78eaf8a953c053c5f2ea29ec49ee5aee62c8e`; target plugin
  source: `56955a499277186e93d4e7a7738377edd057e195` (tag 1.35.1).
- Read-only diagnostics: **2026-10-31 (UTC)**, vault
  `obsidian-tldraw-bridge`, official CLI `obsidian-cli` in the installed macOS app.
  `doctor` passed with no missing capabilities, no document sessions and
  `pendingUpdate: null` for the checkout runtime. Package consistency check passed.
- Checkout and installed Codex-cache loaders were present; their on-disk runtime
  files matched. Other loader contexts' pending state was not established.
- Last live editing/persistence verification: **date and complete combination
  unknown**. Existing declarations list plugins 1.31.0 and 1.32.0 as tested.
  No editing, save/reopen, migration or visual tests were run in this review;
  plugin 1.35.1 / SDK 5.6.0 compatibility remains unverified.

## Unresolved actions

No mandatory bridge code change was established by the
[tagged comparison](https://github.com/tldraw/obsidian-plugin/compare/1.32.0...1.35.1).
Principal plugin hooks remain present; API presence does not prove behavior.

- **High:** Plan a separately authorized installer update for the newer Electron,
  then repeat CLI/transport checks. No CLI regression was reproduced.
- **High:** Test synchronization, rollback, Undo, queued changes at teardown,
  saving and reopening on plugin 1.35.1 / SDK 5.6.0. The
  [SDK 5.6 Store fixes](https://tldraw.dev/releases/v5.6.0) affect these boundaries;
  retain existing reconciliation until tested.
- **Medium:** Add save/reopen coverage for literal `$&` and `$'` labels, following
  the plugin's [saving fix](https://github.com/tldraw/obsidian-plugin/blob/1.35.1/src/utils/strings.ts).
  Recheck assets, styles and exports after the [SDK 5.5 changes](https://tldraw.dev/releases/v5.5.0)
  and [1.35.1 patches](https://github.com/tldraw/obsidian-plugin/compare/1.35.0...1.35.1).

Use [testing procedures](../testing.md), especially `live_create.py`,
`live_styles.py`, `live_apply_preview.py`, `live_images.py` and dedicated-note
rollback/Undo/close checks. Update `testedPluginVersions` and compatibility
claims only after relevant target live tests. No application, installer, plugin
or runtime implementation was updated by this review.
