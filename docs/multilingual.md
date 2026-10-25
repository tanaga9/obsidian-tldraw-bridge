# Multilingual diagram workflow

Multilingual diagrams use the same live Editor and persistence protections as
other bridge edits. Translation remains an agent task, performed on explicit
request. The implementation supplies identity, freshness inspection, and reviewed
checkpoints; it does not call a translation model, schedule background work, or
prevent edits in Obsidian's GUI.

## Identity and operating policy

A Note may contain several related diagrams. Each diagram has a stable ID and
at most one page for each language. Register only needed combinations. Overview,
detail, current/proposed and unrelated workflows are distinct diagrams, not
translations of one another. Single-language Notes require no registration.

If both language hashes changed, or the origin, intent, or compatibility of edits
is uncertain, inspect and summarize both versions and ask the user for the merge
policy before applying changes. Offer choices grounded in the actual edits,
such as combining both, prioritizing a specified language, or sharing layout
improvements only. Preserve both pages and existing checkpoints while awaiting
the decision; do not silently overwrite, choose a source, or acknowledge the
differences. An existing explicit merge policy can be reused when it clearly
covers the observed changes. Merely requesting translation does not decide how
to resolve independent or ambiguous edits.

Each registered diagram has one editing source. Changing that source is a
workflow handoff, not proof that independent changes have been merged. Page names
can change without changing identity. Existing language pages are updated in
place; do not create a Note or revision page for each reflection.

For each diagram, use its base-language name as the shared leading portion of
tldraw page names, export filenames, and the names of frames used for export.
Keep most of each name identical from the start across languages; append a
language code and, if useful, a translated title. For example, pages and export
frames can be `Architecture overview (en)` and `Architecture overview (ja)`,
with files `architecture-overview.en.webp` and `architecture-overview.ja.webp`.
Give a different theme its own shared prefix, such as `Data flow` and
`data-flow`. This keeps the correspondence visible when one Note contains
multiple diagrams in multiple languages. A language code at the beginning or
wholly translated names would obscure that correspondence.
The naming base is independent of the current editing source: a source handoff
alone does not change it. Names support human recognition; stable diagram/page
IDs remain the operational identity. When renaming existing exports, update
their Markdown references together.

Reflect changes on explicit user request or within already authorized translation
work. During commit review, inspect the changed diagrams and report unresolved
items; do not automatically translate or acknowledge them. No periodic monitor or
Git hook is installed by default.

## Decisions that prevent translation churn

- Read both current pages before updating, even when the target matches its
  baseline. Existing valid translations are input to the task, not disposable
  generated text. Keep unchanged labels, tone, shape identities, and layout.
- Use the whole diagram as translation context, then apply only necessary edits.
  Initial creation can clone the diagram once; subsequent reflection should not
  recreate the target wholesale. Persistent string correspondence tables are
  optional, not required by this workflow.
- A hash difference means records changed. It does not prove an obsolete
  translation, conflicting intent, or permission to overwrite. Inspect geometry
  changes because position, size and grouping can express meaning.
- Layout improvements discovered in a translation can be applied to the source
  too. Check both languages' text lengths; share a structural fix where it helps,
  while retaining useful language-specific wrapping and widths. Preserve meaning
  and existing wording, and inspect/export every affected page.
- Bound meaningful arrows to their corresponding shapes. When cloning an initial
  language page, remap parent IDs and both binding endpoints, not just labels.
  Check rendered height (`growY`) and connector alignment after text changes.
- Metadata is current operational state, not an execution diary. Keep one
  checkpoint per target; use ordinary history for recovery. Do not store copies
  of all previous diagrams, translation strings, or dated operation reports.

The installed [Skill workflow](../integrations/codex/skills/obsidian-tldraw/references/multilingual.md)
contains the agent-facing procedures and checkpoint JSON example.

## Live inspection and checkpointing

Open the intended Note, then inspect every registered group or just one diagram:

```sh
python3 bridge.py --vault obsidian-tldraw-bridge open docs/diagrams/diagramming-guide-design-system.md
python3 bridge.py --vault obsidian-tldraw-bridge language-status docs/diagrams/diagramming-guide-design-system.md
```

`language-status` reads all language pages without switching the dedicated
Editor's current page, writing metadata, or translating. It returns `path`,
`revision`, `diagrams`, `errors`, `requiresReview`, and a semantic-limit reminder.
Each page result includes its `diagramId`, `language`, `pageId`, `status`, and
hashes. Statuses distinguish source/target content-signature changes, divergence,
presentation review, missing lineage, and reviewed/current states. No status
alone establishes semantic correctness.

After inspecting both pages and performing any authorized updates:

```sh
python3 bridge.py --vault obsidian-tldraw-bridge --request-id language-review-unique language-checkpoint note.md --revision CURRENT_REVISION --input checkpoint.json
```

The JSON requires `diagramId`, `editingSourcePageId`, `languages` (language to page
ID), `targetLanguage`, `kind`, `reason`, and `reviewed: true`.

| Kind | Use |
| --- | --- |
| `translation` | After applying and verifying an authorized translation update |
| `adopt` | Establish a baseline for existing pages whose equivalence was inspected |
| `layout` | Accept reviewed presentation changes with unchanged content signatures |

A layout checkpoint rejects content-signature changes or missing v2 baselines.
It is not a shortcut for dismissing independent edits. Initial legacy metadata
can be inspected without mutation; adopt it only after comparing both pages.
A changed editing source leaves targets with old lineage as review items.
A checkpoint registers existing pages and changes metadata only. It cannot
create/delete pages, remove a registered language, or replace its page ID.

Checkpoint edits require a fresh document revision, use the normal synchronous
rollback and persistence checks, return `scriptResult` with the checkpoint, and
support retained request IDs. Retry uncertain results only with identical input
and the same ID, following the [operation contracts](../integrations/codex/skills/obsidian-tldraw/references/operations.md#results-and-failure-recovery).

## Metadata and hashing

Page metadata stores `diagramId` and `language`. Document metadata stores
`multilingualDiagrams[diagramId]`, with `schemaVersion: 2`,
`editingSourcePageId`, `languages`, and `checkpoints[targetLanguage]`.
Each checkpoint records its source page, source and target fingerprints, review
kind/reason/time, and algorithm `page-content-v2`. Other document metadata is
preserved. No full historical record snapshot is stored.

The full fingerprint includes descendant shapes, their bindings, and referenced
assets. It excludes shape locks and shape/binding metadata. Page names, metadata,
selection and cameras are excluded. The content signature additionally excludes
known position, size, typography, stacking, opacity and arrow geometry fields.
Unknown properties, labels, parent relationships, binding endpoints, and visual
encodings such as color remain conservative content inputs. Thus a content-signature
change is an inspection candidate, not an automatic judgment of changed meaning.
Content equality plus a changed full hash gives `presentation-review`, not an
automatic assertion that a change is harmless. Assets participate in both hashes.
Current fingerprints sort record IDs by UTF-16 code-unit order and object keys
lexically, so identical data does not change hashes with the process locale or
Store iteration order. Fingerprints include `hasAssets` to identify pages whose
asset content needs a verifiable baseline.

Legacy `sha256-page-records-v1` translation baselines and matching `layoutReview`
records remain inspectable. Legacy mismatches return `needs-review` because a
coarse hash cannot reconstruct what changed. No migration resets them silently.
Legacy fingerprints retain their original collation only for reading existing
baselines. They omit asset data: if either page references an asset, even a
matching generation hash or legacy layout review returns `needs-review` with
`reviewReason: legacy-baseline-excludes-assets`. Inspect both pages and explicitly
adopt a current checkpoint when appropriate; do not assume the image is unchanged
or silently advance the baseline.

## Commit review

From the repository root, with Node.js available as a developer dependency:

```sh
node scripts/review_translations.cjs
node scripts/review_translations.cjs --staged
node scripts/review_translations.cjs --worktree --strict
```

By default, review changed Markdown in the Git index and working tree separately,
including untracked working-tree Notes. The staged version is read from the index,
not substituted with the current file. Unrelated diagrams within a changed Note
are skipped when their records and registration are unchanged. Explicit
repository-relative paths can limit the files examined.

The command uses the same review logic as the live API. It reads saved Git/file
records, not unsaved Obsidian state, and never writes diagrams, metadata, files,
or Git state. Before reviewing a commit, ensure human edits are saved; use live
inspection if file freshness is uncertain. Errors produce exit 1. Review findings
are advisory by default; `--strict` returns 2 when review is required. Malformed
Note data and invalid/missing/duplicate language identities are reported.
If a previously saved tldraw Note loses its start marker, the reviewer reports
the damaged Note or intentional format removal for inspection rather than
silently skipping it as ordinary Markdown. The index and working-tree versions
are checked independently, so repairing one cannot hide damage in the other.
If the current Note is valid but its previous Git version cannot be parsed, the
reviewer inspects all current diagram groups and reports `baselineWarning` rather
than treating the historical error as a failed repair. It does not advance any
translation checkpoint. Invalid current data remains an error.

For findings, state which diagram/language changed and what still requires
inspection. Translation reflection remains explicit. A user can choose to reflect
now, defer with a clear stale-state explanation, or retire an unused language.
No arbitrary deadline or background notification is needed for this workflow.

## Current boundaries

Language retirement/removal has no dedicated command. Inspect independent edits
first, then use the existing SDK to remove the intended page and update only its
diagram's language map and checkpoints. If the editing source is being removed,
choose the replacement source explicitly. Single-language diagrams do not need
translation checkpoints. Do not interpret the absence of a retirement command as
automatic garbage collection or delete languages just to pass review.

The live integration check exercises a two-language, single-diagram Note. Runtime
unit tests also exercise a three-language source handoff, preservation of another
diagram's pages and checkpoints, and a layout checkpoint that acknowledges only
its intended language pair. They do not replace real SDK verification of every
multi-diagram or three-or-more-language editing sequence. Inspect the affected
pages and lineage when using those combinations; uncertain merges still require
a user decision.

The design-system example retains its reviewed legacy generation/layout metadata.
It is readable by the current inspector and need not be migrated just to commit
the example. Adopt a current checkpoint only after inspecting both language
pages; migration must not hide new edits or imply a new translation.
