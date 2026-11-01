# Upstream maintenance status

Last upstream research: **2026-11-01T02:13:24Z** (UTC); official plugin/SDK release APIs
reconfirmed 1.35.1 / 5.6.0.
Latest live editing verification after application restart: **2026-11-01T02:08:23Z** (UTC).
Scope: plugin 1.35.1 compatibility and package-known update advice.
Latest read-only diagnostic check: **2026-11-01T02:13:24Z** (UTC), checkout base
`b018cfac365d7c8c91115c70773e0d4aa511cf69` with the update-advice changes.

## Versions and evidence

| Component | Installed / tested observation | Latest stable | Evidence |
| --- | --- | --- | --- |
| Obsidian Desktop | **1.14.5**, installer **1.14.4** | Last confirmed **1.14.5** on 2026-10-31; changelog refresh on 2026-11-01 returned HTTP 403 | Official macOS CLI `version`; [public release](https://obsidian.md/changelog/2026-10-22-desktop-v1.14.5/) |
| Obsidian tldraw plugin | **1.35.1**, local and running manifests | **1.35.1**, fresh API confirmation 2026-11-01, non-draft and non-prerelease | [release API](https://api.github.com/repos/tldraw/obsidian-plugin/releases/latest), [release](https://github.com/tldraw/obsidian-plugin/releases/tag/1.35.1) |
| Embedded tldraw SDK | **5.6.0**, installed bundle registrations, running library registry and saved test-note metadata | **5.6.0**, fresh API confirmation 2026-11-01 | Target [lockfile](https://github.com/tldraw/obsidian-plugin/blob/1.35.1/package-lock.json), [SDK release API](https://api.github.com/repos/tldraw/tldraw/releases/latest), [SDK release](https://github.com/tldraw/tldraw/releases/tag/v5.6.0) |
| Electron / Node inside Obsidian | **43.7.7 / 24.21.0** | Previously reviewed Desktop release describes Electron **43.8.3**; target Node unknown | Read-only `process.versions`; Desktop release above |

The target's [release manifest](https://github.com/tldraw/obsidian-plugin/releases/download/1.35.1/manifest.json)
requires Obsidian **1.10.0**, satisfied locally. The source-tag manifest still
says 1.35.0; the release asset and installed manifest identify 1.35.1.
Latest live-tested checkout: `478c5ce8cb2c345ef27ec8effb1940a2bfcc9a41`.

## Completed verification

Explicit vault: `obsidian-tldraw-bridge`. Official CLI:
`/Applications/Obsidian.app/Contents/MacOS/obsidian-cli`.
All checks below ran on **2026-11-01 (UTC)** against the installed combination.

- After application restart, seven live scripts passed again: `live_create.py`,
  `live_styles.py`, `live_apply_preview.py`, `live_images.py`, `live.py`,
  `live_sessions.py`, and `live_reload.py --multi-page-copy`. Runtime versions
  were reconfirmed; the library registry contained only SDK **5.6.0**, with no
  5.4.0 registrations. PNG/WebP previews were visually inspected.
- Before restart, eleven live scripts passed: `live_create.py`, `live_styles.py`,
  `live_apply_preview.py`, `live_images.py`, `live_transport.py`,
  `live_languages.py`, `live_pending_update.py`, `live.py`, `live_sessions.py`,
  `live_freehand.py`, and `live_reload.py --multi-page-copy`.
  Scope includes creation, CRUD, saved records, conflicts with injected GUI
  changes, shared-Store rollback, Undo/Redo, retained replay, transport recovery,
  styles, inline images, PNG/WebP exports, multilingual metadata, independent
  documents, and deferred runtime replacement with explicit closure/reopening.
- Added and passed literal `$&`, `$'`, `$1` and Japanese text save/reopen coverage
  in `live_create.py`, releasing the test note's GUI Store before reopening.
- A disposable copy of `docs/diagrams/architecture.md` (plugin 1.32.0 / SDK 5.4.0)
  opened, saved with plugin 1.35.1 / SDK 5.6.0 metadata, and reopened with the
  same document revision. All **78 document records**, including shapes,
  bindings and inline assets, were preserved. The original note was unchanged.
  This is one real legacy fixture, not exhaustive migration coverage.
- Visually inspected the legacy frame WebP, bound-node export, inline-image
  export, rich-text PNG, and freehand context crop; text, icons, connections,
  fills and cropping rendered correctly. Previews remain outside tracked docs.
- Automated checks passed: **175 Python tests**, **135 Node tests**, runtime and
  loader syntax, generated package consistency, and `git diff --check`.
- Current checkout and rebuilt package `doctor` return
  `pluginUpdate: {latestKnownVersion: "1.35.1", available: false}` on the installed
  1.35.1. Checkout `capabilities` agrees. Older/equal/newer and unknown-version
  cases are covered by runtime tests; no plugin was downgraded for this check.
  The unsupported-plugin error path also retains update advice; a Python
  regression test reproduced its loss before the fix and passes with the fix.
- Final checkout-runtime `doctor`: plugin **1.35.1**, supported, version tested,
  no missing capabilities, no document sessions, and `pendingUpdate: null`.
  All temporary test notes were removed; unrelated sessions were not closed.

## Outcome and limits

### Focused rich-text check

Latest focused verification: **2026-11-01T02:53:11Z**, checkout
`178d3023f22e3b05fba18d621f188e8b76b35b13` with text-operation edits, vault
`obsidian-tldraw-bridge`, plugin **1.35.1** / SDK **5.6.0**.
`tests/live_rich_text.py` verifies exact mark/list results and removals, untouched
text, selected rich-text observation, saved/export revision agreement, and disk
reopening. Label separation preserves effective character size and bindings;
its position and width are explicit, without automatic placement or custom metadata.

Native wrapped/list arrow labels and auto-sized list text can clip in WebP output.
Separate editable text with ample explicit width rendered correctly in the
inspected preview; check wrapping and reposition it with the arrow.
Default SDK text configuration supports inline code but disables `codeBlock`.
GUI rendering and the native-export root cause remain unverified. No application
or plugin upgrade was performed. Drawing guidance and operation docs were updated;
the existing knowledge-map routes still apply, so its note/preview were preserved.
Release versions and application/Electron/Node observations above retain their
original research/verification dates; this was an installed-capability check.

### Previous upgrade review

No functional bridge regression was reproduced and no compatibility workaround
was needed. **1.35.1** remains live-tested. Diagnostics now compare the installed
stable plugin version with the package-known latest release. The rebuilt Skill
mentions an update as a short aside in a normal progress message, once per
vault/version pair when older, without blocking supported APIs or updating
automatically. Release knowledge is maintained
separately from live-tested versions. Existing Store reconciliation remains in place: the
[SDK 5.6 notification/rollback fixes](https://tldraw.dev/releases/v5.6.0) do not
by themselves establish that it is safe to remove the bridge's protections.

The latest seven-script live check ran after application restart with only SDK
5.6.0 registered. The legacy-fixture migration check, freehand, transport,
multilingual and deleted-note update-deferral checks were not repeated after
restart; their successful results above remain from the earlier check.
Manual GUI gestures and GUI/embed export paths were not separately tested.
Checkout and rebuilt package diagnostics were exercised directly; the package
was not installed into other Codex-cache contexts. The end-to-end conversational
notice on an older installed plugin was not live-tested.

The previously identified installer/Electron update remains separate scope and
was not an observed blocker. No application, plugin, personal configuration,
production diagram or drawing-design guidance was changed by this check.
