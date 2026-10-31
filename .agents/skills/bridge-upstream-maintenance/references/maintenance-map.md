# Upstream maintenance map

Paths below are relative to the repository root. These are entry points; confirm
current symbols, command options, and test behavior before relying on them.

## Official research sources

- Obsidian application releases: <https://obsidian.md/changelog/>.
- Obsidian CLI documentation: <https://help.obsidian.md/cli>. Compare it with the
  actual executable's help and behavior; Desktop, installer/runtime, and CLI
  availability may differ.
- Obsidian plugin API: <https://docs.obsidian.md/> and
  <https://github.com/obsidianmd/obsidian-api>. Public API documentation does not
  establish compatibility of the community plugin's private Store integration.
- Obsidian tldraw plugin: <https://github.com/tldraw/obsidian-plugin> and its
  releases/tags. Check the target manifest, dependency/lockfile entries, Editor
  initialization, Store management, serialization, and save notifications.
- tldraw SDK: <https://tldraw.dev/releases>, <https://tldraw.dev/>, and
  <https://github.com/tldraw/tldraw>. Check migration guidance and exact tagged
  implementation/types for the SDK version used by the plugin.

Follow official redirects or repository moves when necessary and identify the
resolved source. tldraw.com, tldraw offline, and the Obsidian plugin are different
hosts; features in one are not evidence of availability in another. An issue or
unmerged PR is not a shipped behavior. Cite the release/tag or commit and review
date for version-sensitive claims.

## Release source priority

For GitHub-hosted releases, prefer freshly retrieved official API metadata
(`/repos/{owner}/{repo}/releases/latest`) over cached HTML lists and search
snippets. Check the tag, publication date, and draft/prerelease flags against the
project's release channel; for Obsidian Desktop, distinguish public from
Catalyst in its official changelog. A latest-release endpoint is a starting
point, not evidence of compatibility or the embedded SDK version: inspect the
target tag's manifest, lockfile and relevant patches too. If sources disagree,
report the discrepancy and which fresher evidence determines the target. When
fresh confirmation fails, label the latest version unconfirmed and retain the
previous value with its original confirmation date.

## Connection diagnosis

CLI "unable to find Obsidian" can result from a stopped app or from sandbox/IPC
restrictions. Use permitted read-only process or connection checks to distinguish
them; when necessary, use the environment's approval mechanism for a read-only
probe outside the sandbox. Retry after evidence of a specific cause or access
change, not repeatedly with identical permissions. Report unresolved access as
an unverified runtime state. Do not launch/restart Obsidian or change CLI/plugin
settings merely to complete a release review.

## Implementation and verification entry points

| Boundary | Inspect | Relevant verification |
| --- | --- | --- |
| Desktop CLI, executable discovery, vault identity, eval framing, deadlines, Unicode | `src/obsidian_tldraw_bridge/obsidian.py`, `vaults.py`, `cli.py` | Python connection, vault, transport, payload, response and Unicode tests; `tests/live_transport.py` for real CLI behavior |
| Plugin hooks and dedicated Editor construction, GUI/shared Store synchronization, document records and saving | `src/obsidian_tldraw_bridge/runtime/bridge.cjs`: `pluginSupport`, `requirePlugin`, `requireEditor`, `requireEditing`, `saved`; inspect creation/session code too | `tests/runtime.test.cjs`; relevant `tests/live_create.py`, `live.py`, `live_sessions.py` |
| Runtime loading, Node module cache, pending updates and receipts | `src/obsidian_tldraw_bridge/runtime/loader.cjs`, loader dispatch in `obsidian.py` | `tests/loader.test.cjs`, Python reload tests; `tests/live_pending_update.py`, `live_reload.py` with their documented interruption/recovery rules |
| Shape records, rich text, arrow bindings, styles, export, freehand encoding and assets | Runtime edit/export helpers, `freehand.py`, `images.py`; canonical `references/diagramming/tldraw.md`, `arrows.md`, `references/freehand.md` | Runtime and Python feature tests; `tests/live_styles.py`, `live_apply_preview.py`, `live_freehand.py`, `live_images.py`; inspect previews |
| Markdown schema, document scope, migrations and multilingual fingerprints/checkpoints | Runtime parsing, revision/persistence and language helpers; `docs/multilingual.md` | `tests/multilingual.test.cjs`, runtime tests, `tests/live_languages.py`; saved/reopened records and previews for migrations |
| Public bridge contracts and knowledge | `src/obsidian_tldraw_bridge/api.py`, `cli.py`, `docs/api.md`, `docs/cli.md`, `docs/known-limitations.md`, `README.md`, canonical Skill | API/CLI tests and package tests; check examples against current help |

Canonical references in the table are under
`integrations/codex/skills/obsidian-tldraw/`. Python feature modules live alongside
`obsidian.py`. The bridge has no JavaScript dependency installation step: the
running Obsidian plugin supplies the SDK. Do not add or bump an unrelated npm
dependency to claim that the installed SDK has been upgraded.

## Check selection

Read `docs/testing.md` for current commands, prerequisites, side effects, cleanup,
and the distinction between tests using a disposable note and an existing
dedicated test note. Do not select a user's production diagram as a test fixture.
If a live request has an unknown outcome, inspect its receipt/evaluation evidence
before retries or cleanup; never rerun the edit or whole test as recovery.

For knowledge-only changes to the distributed Skill, rebuild and check the plugin
and run the package tests as documented in `docs/development.md`. For bridge
runtime/transport changes, run the automated Python/Node checks in
`docs/testing.md` and relevant live integration checks when the environment is
available. If live verification is unavailable, deliver the scoped repository
change with that limitation rather than claiming the new combination is tested.

This maintenance Skill is outside both builders' source trees. Changes only to
`.agents/skills/bridge-upstream-maintenance/` or its maintainer documentation do
not require regenerating the distributed drawing Skill. Validate this Skill's
frontmatter and local links, and check package consistency to confirm exclusion.
