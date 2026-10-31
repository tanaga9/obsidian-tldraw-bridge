---
name: bridge-upstream-maintenance
description: Investigate tldraw SDK, Obsidian tldraw plugin, and Obsidian Desktop or CLI upgrades for this obsidian-tldraw-bridge repository; propose or implement evidence-based updates to bridge code, tests, documentation, and distributed drawing guidance. Use for upstream release reviews, compatibility regressions, or maintenance of version-sensitive knowledge, not ordinary diagram editing.
---

# Bridge upstream maintenance

This is a repository maintenance Skill, outside the distributed plugin and
standalone drawing Skill. Resolve the repository root from this file
(`../../..`), then read `AGENTS.md`, `docs/development.md`, and the relevant
sections of `docs/testing.md`. Keep this Skill under `.agents/skills/`;
the canonical **distributed** Skill lives under
`integrations/codex/skills/obsidian-tldraw/`.

## Choose the outcome

- For research, review, or proposal requests, inspect sources and perform
  non-mutating diagnostics; report recommended changes without implementing
  them. Always update the maintenance snapshot described below, including for
  proposal-only checks, unless the user explicitly requests no file changes.
  Write any additional report file only when requested or useful.
- For implementation or knowledge-update requests, make the scoped changes and
  validate them. Existing authorization carries forward; do not insert a second
  approval step before ordinary repository edits.
- If asked generally to handle an upgrade without a target version, determine
  the relevant stable release from official sources. Distinguish an installed
  version repair from migration to a release not installed locally.

Creating this Skill does not itself authorize upgrading applications or plugins.
Repository maintenance does not imply installing releases, changing a personal
vault's configuration, restarting Obsidian, or closing unrelated live sessions.
Use an isolated test environment when a different installed version is needed;
otherwise report the validation gap and the specific action needed.

## Establish the actual version boundary

Record the repository revision and relevant working-tree edits. Establish the
current and target combination separately for:

- Obsidian Desktop application and installer/runtime, including the actual CLI
  executable, platform, CLI enablement, and observed command behavior.
- The Obsidian community plugin with ID `tldraw`: manifest version and, when
  available, source tag/commit and bundled build.
- The tldraw SDK embedded in that plugin, including record schemas and migrations.
  Plugin release numbers are not SDK release numbers; inspect that release's
  dependency declarations/lockfile or build evidence. Report an unknown SDK
  version as unknown.
- The bridge source and runtime actually loaded in Obsidian, which can differ
  from this checkout when a packaged copy or pending runtime update is in use.

Use current CLI help and this checkout's bridge help before constructing probes.
For Obsidian, prefer CLI `version` for app/installer versions, then read
`process.versions` for the running Electron/Node versions. Use OS bundle metadata
only as a fallback; it may describe the installer rather than the running app.
Keep unavailable values unknown. For connection failures, follow the diagnostic
routing in the maintenance map before concluding that Obsidian is stopped.
Use explicit vault selection. Read-only `doctor`, `capabilities`, `observe`, and
`style-spec` can establish observed capabilities, but API presence alone does not
prove behavior or persistence. Do not require a running Obsidian instance just
to review upstream releases.

## Research and map changes

Read [the maintenance map](references/maintenance-map.md) for source entry
points, upstream source selection, connection diagnosis, and test selection.
Confirm the latest stable release from fresh official metadata using the map's
source priority; do not rely solely on search snippets or cached release lists.
Browse official release notes, tagged source and migration guides for the
current-to-target interval. Include
intermediate breaking changes and distinguish stable releases from prereleases.
Prefer release-pinned source over a moving default branch when discussing the
target. If network access or release artifacts are unavailable, state what could
not be checked; do not substitute remembered versions for current evidence.

Separate upstream facts, locally reproduced behavior, and hypotheses. For each
relevant change connect the evidence to an actual bridge dependency or knowledge
claim: affected file/API, resulting behavior, proposed action, and verification.
Review opportunities as well as breakage: an upstream API may replace a private
hook or remove a workaround. A new upstream feature does not need bridge support
unless useful within the requested scope. Avoid unrelated rewrites and copying
upstream manuals into the drawing Skill.

## Apply scoped updates

Follow the compatibility policy in `docs/development.md`. Update affected callers
and contracts together; compatibility shims are not required solely for old
callers. Preserve document/revision checks, synchronous Store rollback, request
identity/replay, persistence verification, and GUI/shared-Store synchronization.
Do not weaken these guarantees merely to make a newer version pass.

Keep capability-based checks for untested plugin versions. Update
`testedPluginVersions` only for plugin versions actually exercised with relevant
live tests, and report the tested Obsidian/plugin/SDK combination and test scope.
Do not treat mock tests, upstream declarations, or a successful `doctor` as live
compatibility evidence.

Maintain knowledge at the right layer:

- Product/format knowledge: `docs/tldraw-overview.md`, with dated, linked evidence
  for the claims actually reviewed.
- Guarantees, limitations, and developer procedures: existing maintainer docs.
- Agent-facing operation contracts and drawing decisions: canonical distributed
  Skill references. Update decision-changing guidance where it already belongs;
  keep extended research and version comparisons outside the distributed Skill.
- Generated package: rebuild after changes to bridge source or the canonical
  distributed Skill; never patch generated files directly.

Remove or narrow obsolete workarounds only after checking their callers and the
behavior they protected. Do not edit saved drawing JSON as a substitute for a
schema migration. Use SDK/plugin migration paths on disposable copies and verify
reopening, assets, rendering, and saved records if formats change. Follow the
repository's diagram and multilingual rules for any documentation Notes touched.

## Verify and report

Select checks using `docs/testing.md` and the maintenance map. Reproduce a
regression with a targeted test before or alongside fixing it. Mock tests verify
bridge logic; live tests verify installed integration behavior; inspect previews
to verify rendering. State skipped checks and why. For runtime updates, account
for session-based update deferral and the loader's restart requirement rather
than testing stale code or forcing sessions closed.

For a proposal, give the version scope, linked upstream findings, affected paths,
recommended changes with priority, and the test plan. For implementation, report
what changed, checks and their environment, and remaining uncertainties. Include
a concise mapping of evidence → impact → action → validation when there are
multiple findings. Explicitly say when no relevant repository change was found.
Keep compatibility claims limited to the combination and behavior verified;
do not append cumulative activity logs to maintainer documentation.

At the end of every upstream check, create or update
`docs/maintenance/upstream-status.md` with a compact current snapshot, even when
no implementation change is needed. Read the previous snapshot first. Record the
check timestamp in UTC (ISO 8601 with `Z`), latest stable and installed Obsidian/plugin/SDK
versions, any distinct target version, relevant Electron/Node versions, bridge
commit, official release/tag links, and the check's outcome and limitations.
Use UTC for recorded dates and timestamps. Keep upstream research and live
verification separate, each with its actual date and scope. Preserve the last genuinely live-tested combination and date unless
new live tests were performed. Mark unknown or failed checks explicitly; retain
previously confirmed values with their original dates rather than presenting
them as newly checked. Maintain one current snapshot and use Git for history.
Keep it brief: a version/evidence table, diagnostic and live-test dates/scopes,
and unresolved actions. Put extended analysis in the response or a separately
requested report. Omit full command output, hashes, and staging history unless
they explain an unresolved issue. Editing the guidance or reformatting this
record alone must not advance check dates.
If the user requests no file changes or saving is blocked, include the snapshot
in the response and state that the saved record was not updated.
