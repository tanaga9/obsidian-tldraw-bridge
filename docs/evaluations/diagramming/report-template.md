# Evaluation run report template

Copy this template to `workspace/evaluations/<run-id>/report.md`. Fill it for
that execution; keep the report and raw artifacts out of Git. Promote only
reusable lessons to [findings.md](../../../docs/evaluations/diagramming/findings.md), and applicable runtime guidance
to the canonical Skill. Do not treat template defaults as measured results.

## Purpose and scope

- Question or observed problem:
- Maintenance path: diagnose and repair / compare guidance
- Execution type: reproduction / targeted regression / smoke / repeated comparison
- Planned runs and acceptance criteria:
- Actually completed, failed, incomplete, and unexecuted runs:
- Claim this execution can support:

## Frozen inputs and environment

- Baseline guide revision and index hash:
- Candidate guide revision and index hash; exact files changed:
- Common package and recorder revisions, file hashes, and archived working-tree
  sources; confirmation that only the assigned index differs between arms:
- Preflight for both arm CLIs: state, preview/hash, saved/revision, and accepted
  review-target captures; setup costs excluded from measured trials:
- Task and fixture hashes:
- Model/reasoning settings and fresh-context isolation:
- Vault, interpreter, plugin, and SDK versions:
- Viewing conditions and actual inspection scale:
- Deviations from the protocol, concurrency, and setup costs:
- Frozen scope file: editable/protected IDs, allowed additions, initial defects
  classified as observed/not observed, and initial preview evidence:
- Required unchanged properties inside editable records, such as label rich
  text and binding endpoints:
- Measurement plan: available metrics, units, unavailable metrics, and claims
  that cannot be evaluated without them:

## Results

| Run / case / arm | Task | Affected quality and saving | Preservation | Defects and evidence | Workload |
| --- | --- | --- | --- | --- | --- |
| Include every run, including failures | Unassessed | Unassessed | Unassessed | Not assessed | Not measured |

Keep the three verdicts separate. A task pass with an affected-quality failure
is not a clean result. Distinguish introduced, retained, and resolved defects;
record protected pre-existing defects without treating them as regressions.

Separate introduced defects from pre-existing defects, and permitted edits from
protected content. Keep intermediate correction cycles separate from final
defects. Record metric definitions: elapsed time, actual tool calls, CLI calls,
actual tokens or a named proxy, and human repair items/minutes. Leave unavailable
measurements unavailable; do not replace them with zero or mix unlike counts.
Use `scripts/diagramming_eval.py` for frozen scope, child-process timing/counts,
and preservation checks. Retain `trial.json`, `metrics.json`, `checks.json`, and
the generated review-target bundle with its bound `review.json`. Record target
identity and final-state hash; a stale review is unassessed, not pass. These
records do not replace visual/meaning review.

## Reproduction and proposed correction

- Original failing artifact and saved state:
- Minimal controlled change and comparison artifact:
- Guidance to keep, simplify, or revise, and why:
- New candidate identity and independent follow-up results:

Preserve originals. Do not pool smoke trials, later candidates, or targeted
checks into a repeated comparison.

## Decision and limits

- Decision and evidence supporting it:
- Acceptance criteria met and unmet:
- Unresolved issues and claims not supported:
- Reusable knowledge promoted; canonical files changed:

## Artifact index

Link the local manifest, assigned Skill snapshots, prompts, initial/final notes,
states, saved receipts, previews, reviews, and workload records. Keep links
relative to this report where practical. Record the execution date and timezone
in the manifest.
