# Upstream maintenance status

Last upstream check and completed live verification: **2026-11-01T02:02:38Z** (UTC).
Scope: verify the user's installed plugin update from 1.32.0 to 1.35.1,
exercise bridge integration, and update tested-version declarations.

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
Checkout base: `001219193ccb6ea9319aaf08ce6b3d59d188ea43`, with the scoped
changes described below.

## Completed verification

Explicit vault: `obsidian-tldraw-bridge`. Official CLI:
`/Applications/Obsidian.app/Contents/MacOS/obsidian-cli`.
All checks below ran on **2026-11-01 (UTC)** against the installed combination.

- Eleven live scripts passed: `live_create.py`, `live_styles.py`,
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
- Automated checks passed: **175 Python tests**, **134 Node tests**, runtime and
  loader syntax, generated package consistency, and `git diff --check`.
- Final checkout-runtime `doctor`: plugin **1.35.1**, supported, version tested,
  no missing capabilities, no document sessions, and `pendingUpdate: null`.
  All temporary test notes were removed; unrelated sessions were not closed.

## Outcome and limits

No functional bridge regression was reproduced and no compatibility workaround
was needed. Added **1.35.1** to `testedPluginVersions`, updated compatibility
statements, added the literal-text persistence regression, and rebuilt the
plugin package. Existing Store reconciliation remains in place: the
[SDK 5.6 notification/rollback fixes](https://tldraw.dev/releases/v5.6.0) do not
by themselves establish that it is safe to remove the bridge's protections.

Tests ran after the user's plugin update in the existing Obsidian process.
Its global library registry retains both 5.4.0 and 5.6.0 registrations; the
installed bundle, saved metadata and newer non-finite camera validation confirm
5.6.0 availability/behavior. A clean application restart was not performed.
Manual GUI gestures and GUI/embed export paths were not separately tested.
Only the checkout runtime was confirmed current; the rebuilt package was not
installed into other Codex-cache contexts.

The previously identified installer/Electron update remains separate scope and
was not an observed blocker. No application, plugin, personal configuration,
production diagram or distributed drawing guidance was changed by this check.
