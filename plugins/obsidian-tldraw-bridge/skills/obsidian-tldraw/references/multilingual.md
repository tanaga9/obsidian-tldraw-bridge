# Multilingual diagrams and page review

## Scope and identity

Multilingual support is optional. Keep related diagrams in one Note. Use a stable
`diagramId` for each logical diagram and one page per `(diagramId, language)`;
page names are reader-facing labels, not identifiers. Overview/detail,
current/proposed, and different workflows are different diagrams. Translate only
the requested diagram/language; do not create the full diagram × language matrix.
Single-language diagrams need no translation metadata. Do not register arbitrary
manual duplicates as translations without inspecting their purpose.

Use each diagram's base-language name as the shared leading portion of its
tldraw page names, export filenames, and export-source frame names. Keep most
of the name identical from the start across languages; put language codes and
optional translated titles at the end, not the beginning. For example, use
`Architecture overview (en)` / `Architecture overview (ja)` for pages and frames,
and `architecture-overview.en.webp` / `architecture-overview.ja.webp` for exports.
Use a distinct shared prefix for each theme so multiple diagrams and languages
in one Note remain visibly paired. Do not translate the entire name or rely on
language-only page/frame names. Keep this naming base when the editing source
changes; it does not replace stable IDs. Update Markdown references when
renaming existing exports.

Within each diagram, name one editing source page. It may change between work
sessions; different diagrams in one Note may have different source languages.
Do not select the newest language by modification time. Never resolve independent
content edits by overwriting one page or merely changing the source pointer.

## Ask about uncertain merges

When both language pages' hashes have changed, or there is doubt about the
origin, intent, correspondence, or compatibility of edits, inspect both pages
and ask the user for the merge policy before reflecting changes. Summarize the
observed changes and uncertainty, then offer concrete choices such as preserving
both sets of edits, prioritizing a specified language, or sharing only layout
improvements. A hash difference alone does not prove a conflict, but it must not
be used to choose a winner. Do not silently resolve uncertainty by classifying
edits as layout-only.

While awaiting the answer, retain both versions and their checkpoints. Read-only
inspection and previews may continue; do not overwrite, merge, switch the editing
source, delete a language page, or advance a checkpoint to dismiss the issue.
Reuse an explicit user merge policy only when it clearly covers the observed
changes; a generic request to translate does not settle conflicting edits.

## When to check and apply

- Apply translations or shared layout changes when the user explicitly requests
  them, or when already authorized as part of the current task.
- During a commit review, inspect changed diagrams and report untranslated content,
  independent edits, and presentation changes. A request to review or commit is
  not itself a request to translate. Do not translate or advance checkpoints just
  to make the review pass. Report a deferred update explicitly.
- Do not translate on every edit, install timers, or add periodic notifications
  by default. Reuse an existing version when no relevant changes need reflection.

For a live open Note, run:

```sh
python3 bridge.py --vault <vault> language-status <note.md>
python3 bridge.py --vault <vault> language-status <note.md> --diagram-id <diagram-id>
```

These read all registered language pages without selecting a different page or
editing the Note. A registered page missing from the Note, duplicate identities,
and missing checkpoints require review. Ordinary unregistered single-language
pages are left alone. Reading reports does not require explicit translation
approval; reuse the user's selected vault.

Status interpretation:

| Status | Action |
| --- | --- |
| `editing-source` | Current workflow source; not proof of exclusive edits |
| `current` | Matches the recorded reviewed pair; reuse, subject to task context |
| `source-content-changed` | Inspect source change and existing target before reflecting |
| `target-content-changed` | Inspect independent target edits; preserve/resolve their intent |
| `diverged` | Both content signatures changed; ask the user for the merge policy before reflection |
| `presentation-review` | Geometry/format changed without a content-signature change; inspect meaning |
| `source-changed` | Editing source differs from the checkpoint lineage; compare pages |
| `untracked`, `needs-review` | No usable baseline or only a coarse legacy baseline; inspect both pages |
| `reviewed-layout` | Matches a recorded legacy layout review; does not imply a new translation |

Hashes are change detectors, not semantic judgments. Content signatures exclude
known layout fields but cannot know whether movement changes sequence, scope,
containment, or emphasis. Unknown properties and changed text are conservatively
retained in the content signature. Never label a translation wrong or disposable
from a status alone. Hashes do not reconstruct historical content; use available
history or compare current pages, and report uncertainty when intent is unclear.
Legacy baselines omit asset data. When either language page references an asset,
an old generation/layout hash cannot establish freshness: inspect both pages and
use an explicit reviewed `adopt` checkpoint if their equivalence is established.
Do not dismiss `legacy-baseline-excludes-assets` by updating hashes blindly.

## Reflect without translation churn

1. Observe/read the source **and the existing target**, even if the target hash
   matches its baseline. Inspect corresponding structure, labels, and bindings.
2. For a new language, clone the diagram once, remap all shape/parent/binding IDs,
   and translate in context. Reuse assets and preserve the source. Keep empty
   rich-text paragraphs as `content: []`, never empty text nodes.
3. For an existing language, use the whole diagram as context but apply only
   necessary changes. Retain valid existing wording, tone, shape identities,
   and user-adjusted layout where the meaning did not change. Do not recreate
   the entire page or independently retranslate unchanged labels.
4. A layout problem discovered in translation may justify adjusting the source
   too. Prefer a shared structural fix when it helps both languages; retain
   language-specific wrapping/widths where useful. Do not copy coordinates blindly
   if they cause overflow in the other language. A layout fix alone does not
   switch the editing source or authorize unrelated text rewrites.
5. Check both before/after meaning and unintended rewording/movement. Preview
   **every affected language page**, including a source page whose layout changed.
   Select the dedicated Editor's page explicitly before preview. Verify bindings,
   rendered `growY`, text fit and frame bounds; refresh corresponding previews.
6. Resolve any merge-policy question with the user before applying uncertain
   changes. After the result is inspected and saved, record a checkpoint. Do not acknowledge
   unseen independent edits or reset a hash to hide an unresolved change.

## Checkpoints, not version copies

`language-checkpoint` changes only page/document metadata. It does not translate,
create/delete pages, change text, or resolve conflicts. Run it only after the
above inspection with a fresh revision, an explicit request ID, and a JSON file:

```json
{
  "diagramId": "overview",
  "editingSourcePageId": "page:en",
  "languages": {"en": "page:en", "ja": "page:ja"},
  "targetLanguage": "ja",
  "kind": "translation",
  "reason": "Reviewed both pages and preserved unchanged target labels and layout",
  "reviewed": true
}
```

```sh
python3 bridge.py --vault <vault> --request-id <unique-id> language-checkpoint <note.md> --revision <revision> --input checkpoint.json
```

Use `translation` after a reviewed translation update, `adopt` to establish a
baseline for inspected existing equivalents, or `layout` after a presentation
review. `layout` requires an existing v2 checkpoint with unchanged content
signatures on both pages; it cannot acknowledge content edits. `adopt` is an
explicit semantic judgment, not a workaround for unresolved differences.
The supplied source page becomes this diagram's editing source; other target
checkpoints with a different source remain review items. Registration cannot
silently replace/remove existing language pages. Remove or retire languages only
through a separate reviewed SDK edit, preserving independent edits and cleaning
associated metadata. Retain one current checkpoint per target, not a history of
page copies or translation strings. Revisions, persistence, and receipt recovery
follow the normal [operation contracts](operations.md#results-and-failure-recovery).
