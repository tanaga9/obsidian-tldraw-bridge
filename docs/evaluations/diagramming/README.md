# Diagramming guidance evaluation

This is a maintainer evaluation kit for the width, text-size, emphasis,
conflict-resolution, and drawing-workflow changes. It is outside the distributed
Skill. Preparing the kit and passing package tests do not establish better
drawing behavior. Keep reusable knowledge in [evaluation lessons](findings.md)
and individual executions in local run reports.

Ordinary diagramming ends with a checked, saved result delivered for the user's
purpose. It does not require this kit or automatically become an evaluation.
Use selected issues or test tasks to investigate guidance changes; retain useful
guidance when the evidence does not justify changing it.

## Choose the maintenance path

Start with the question, not a required number of comparisons.

| Question | Path | Evidence needed | Supported decision |
| --- | --- | --- | --- |
| Why does this label, connection, edit, or export fail? | Diagnose → reproduce → smallest correction → fresh targeted checks | Initial defect classification, controlled reproduction, final previews, preserved records, saved receipts | Keep a conditional workaround or narrow SDK/operation correction |
| Does a guide change improve drawing quality or effort? | Freeze versions and inputs → smoke → repeated comparison | The comparative protocol below, three separate verdicts, matched measurements | Keep, simplify, revise, or defer a guide change |

A local SDK repair does not require the 18-run guide comparison. A targeted
repair check cannot establish general guide superiority. A failed smoke check
can return to diagnosis; freeze a new candidate before resuming comparison.
Package/runtime integrity uses the ordinary [testing guide](../../testing.md),
not a drawing-quality score.

## Targeted improvement and recovery checks

For changes to the improvement/recovery decision procedure, check routing with
bounded cases before considering a drawing-quality comparison. These cases
exercise decisions, not exact response wording. Use current source facts and
disposable sketches if rendering is needed; keep user documents unchanged.

| Case input and observation | Expected decision | Failure to catch |
| --- | --- | --- |
| "Make this clearer" accompanies a diagram whose problem is a cramped label; the existing structure works. | Correct the label and its affected context while retaining the main structure. | Treating a generic improvement request as permission to rebuild. |
| "Improve this" accompanies a diagram whose main structure obscures required relationships; no redesign scope has been agreed. | Explain the concrete redesign and reader benefit, using a small separate sketch if needed; agree on its extent before replacing the diagram. | Applying a substantial redesign merely because diagnosis supports it. |
| The user explicitly requested a new representation or already agreed to a concrete redesign proposal. | Execute within that scope and verify the result. | Asking again for authorization already given. |
| A recovery sketch supports a new main structure, but the user authorized only ordinary improvements. | Preserve the usable diagram and present the supported redesign proposal for agreement. | Treating a successful recovery trial as redesign authorization. |
| A label remains clipped after two edits, but observation now establishes that its container is too narrow and widening fits within the requested scope. | Continue the supported local correction and inspect it. | Entering recovery solely because two revisions occurred. |
| Two layouts satisfy the same established reader task, facts, readability, and explicit constraints; no meaningful preference is missing. | Choose routinely and proceed. | Asking the user to resolve an inconsequential choice or drawing more variants. |
| An incident diagram lacks evidence for which event caused the failure. | Retrieve the source fact or ask for it; preserve causal uncertainty. | Inferring causality from time order or drawing speculative causes. |
| A reader cannot identify the first event; the agent cannot explain why another whole-diagram rearrangement would help. | Test one source-backed event path with a preselected start/next-event check. | Rewording or recoloring the full diagram without testing the uncertainty. |
| A sketch requires several export retries, followed by one successful inspection. | Count one visual trial; handle transport failures through operation recovery. | Exhausting the two-trial stopping rule on API calls or export failures. |
| Two inspected trials of the same uncertainty yield no discriminating observation; a new turn adds no evidence. | Stop variants and ask for the missing concrete choice/example, retaining the unresolved context. | Resetting the sequence on a new turn or calling an inconclusive result acceptance. |
| A trial refutes the proposed cause and identifies a different, source-supported next correction. | Use the informative rejection to choose the next step. | Treating every rejected hypothesis as no progress. |
| A trial or comparison draft clips a required label or omits a branch. | Repair it before judging the hypothesis or asking which structure is clearer; if it cannot be repaired, mark the trial inconclusive. | Rejecting an organizing principle because its sketch is broken. |

A source walkthrough of these cases checks logical coverage only. Package tests
check distribution integrity. Neither establishes reliable agent behavior or
reader benefit; report whether actual agent execution and preview review were
performed, and use the comparison protocol for claims of general improvement.

## Classify the initial state

Before timing a trial, save its initial state and preview. Classify every
initial shape/binding as editable or protected. Record known defects by ID,
affected records, scope, observation, and whether actually observed. Use the
[partial-edit scope example](partial-edit.scope.example.json) for that fixture;
replace every `verify` status after inspecting the installed SDK's output.
Do not assume a defect still exists on a different plugin version.

Editable records may still have immutable properties. Declare these in
`preserve_properties`, for example
`{"id":"shape:eval-worker","paths":[["props","richText"]]}`.
Each path is an array of object keys, not a dotted string or an array index.
The entire value at that path must equal the initial value, including rich-text
structure. Missing initial properties are rejected during setup; changed or
missing final properties fail preservation. The partial-edit example protects
Worker and arrow labels plus each editable binding's source, target, and
terminal while permitting geometry, font, and anchor adjustments.

An existing defect within the affected, editable connections is reviewed under
affected quality, separately from the requested repair. A protected defect is
recorded but must not be fixed or counted as an introduced regression. A broken
fixture that prevents the intended comparison must be adapted and frozen before
either arm starts. Apply identical classifications to both arms. Do not relax
scope or relabel a defect after seeing an arm's output.

## Record three verdicts

| Verdict | Question | How checked |
| --- | --- | --- |
| Task | Does the output satisfy the requested meaning and repair? | Source facts, requested acceptance criteria, and actual rendering |
| Affected quality | Are the edited content and incident connections readable, connected, and saved? | Previews, bindings, and saved receipts; include residual in-scope defects |
| Preservation | Are protected records and required properties unchanged, and additions/removals authorized? | Exact record/property comparison against frozen scope |

Record pass, fail, or unassessed with evidence for each. Task success does not
override affected-quality failure. Record whether a defect is introduced,
retained, or resolved; a retained defect is not automatically a regression.
Missing evidence is unassessed, not pass. All three must pass before treating a
trial as a clean successful result or using its speed as an improvement.

## Automatic recording

The repository-only [recorder](../../../scripts/diagramming_eval.py) uses the
Python standard library. It is not bundled with the Skill. Inspect and classify
the initial preview first, then run:

```sh
python3 scripts/diagramming_eval.py start --run-dir workspace/evaluations/<run-id>/trials/<trial-id> --mode diagnose --scope scope.json --initial-state initial-state.json --input prompt.md
python3 scripts/diagramming_eval.py call --run-dir workspace/evaluations/<run-id>/trials/<trial-id> --kind bridge -- python3 <assigned-skill>/scripts/bridge.py --vault <vault> state <note.md>
python3 scripts/diagramming_eval.py finish --run-dir workspace/evaluations/<run-id>/trials/<trial-id> --status complete
python3 scripts/diagramming_eval.py prepare-review --run-dir workspace/evaluations/<run-id>/trials/<trial-id> --final-state final-state.json --preview preview.webp --preview-receipt preview-receipt.json --saved saved.json
# Inspect the frozen artifacts and fill the returned review.json before checking.
python3 scripts/diagramming_eval.py check --run-dir workspace/evaluations/<run-id>/trials/<trial-id> --final-state final-state.json --review <review-target-directory>/review.json --review-target <review-target-directory>/target.json
```

Use `--mode compare` for comparative trials. `start` requires a new directory
and freezes scope, initial records, and optional input hashes. For creation
trials use an empty initial records array, empty scope ID lists, and
`allow_new_records: true`. Existing records must always be classified.

Route every assigned bridge invocation through `call`, including help, retries,
and failures. It runs an argv array without a shell, records start/end times,
exit status and bridge errors, retains stdout/stderr, and forwards the output.
Redirect a `state` call's stdout to `final-state.json` as usual. Calls made
outside the wrapper are not measured; disclose them. Exclude setup before
`start`. Finish on the same host/boot, after all calls return; interrupted calls
remain unresolved. Do not mark a timeout complete or blindly replay a mutation.

`metrics.json` distinguishes total child-process calls from bridge CLI calls
(including diagnostics/help). Neither is an agent tool-call count. Actual
tokens and human repair minutes remain null unless independently measured;
keep such measurements and their source separately. Do not mix counting units.
Timing is diagnostic metadata, not proof of quality or a performance gain.

Capture final state, a preview and its CLI export receipt, and a confirmed saved
receipt before `prepare-review`. The preview receipt must identify the final
state's revision, the supplied image path, and its image-byte `sha256`; the
recorder checks the hash before and after copying and again during evaluation.
Recapture exports whose receipts lack a hash; do not add one to historical evidence.
The saved receipt must confirm the
same note and revision. Recapture historical receipts without a revision; do not
add a revision to old evidence. The command copies these artifacts into a uniquely identified review
target and returns a template `review.json` bound to that target's SHA-256.
Keep the original JSON capture bytes unchanged when checking; even reformatting
the final-state file requires a new target. Changing the drawing requires new
captures and a fresh review. Review copies, rather than mutable source images.

Fill independently reviewed `task` and `affected_quality` statuses and evidence
in that generated template. `check` verifies target identity, trial/scope,
artifact hashes, and the final-state file hash before using those judgments.
Missing or stale bindings make the judgments unassessed, and replace any prior
`checks.json` pass with that unassessed result. They cannot produce a clean pass.
Keep completed review bundles; never stamp a new target hash onto an old verdict.

`checks.json` computes protected-record counts and property violations; it does
not infer readable rendering or correct meaning. Without a valid bound review,
those judgments stay unassessed. Lifecycle commands within one trial are
sequential; use separate run directories for concurrent trials. Older trials
without a trial ID cannot prepare bound reviews; retain them as historical
evidence and start a new trial for this workflow.

## Reports and retained knowledge

- **Per execution, outside Git:** copy the [report template](report-template.md)
  to `workspace/evaluations/<run-id>/report.md`. Keep run-specific results,
  measurements, hashes, environment details, and raw artifacts together there.
- **Reusable, in Git:** maintain this protocol, the task prompts and fixture,
  the report template, and concise decision-relevant lessons. Put applicable
  agent actions in the canonical Skill; do not add run logs to it.

When a run changes guidance, retain its reusable reproduction method, applicable
conditions, and limitations. A run report remains the evidence for that
execution; a reusable lesson is not a substitute for its measurements.

## Guide comparison: baseline and candidate

The guide baseline is `integrations/codex/skills/obsidian-tldraw/references/diagramming/index.md`
at commit `ebd8f0fd82b90ecbd46c98ccadde8a3f93b9fc95`. This pins the guide being
compared, not its historical runtime. Freeze the candidate index revision (or
archive its exact working-tree bytes) and record both guide hashes.

Prepare the two arms as follows before collecting results:

1. Build a current plugin package using `python3 scripts/build_plugin.py`. Freeze
   that package and `scripts/diagramming_eval.py` by revision and file hashes;
   archive exact bytes for any uncommitted sources. This is the common CLI,
   runtime, Skill entrypoint, and supporting references for both arms.
2. Copy the package's `skills/obsidian-tldraw/` directory to two isolated arm
   directories. In the baseline arm replace only `references/diagramming/index.md`
   with the pinned baseline file; in the candidate arm replace it with the frozen
   candidate index. Verify that every other file is identical between arms.
   Do not load the installed plugin's other copy of the guidance into either arm.
3. Before timing, use each arm's bundled CLI on disposable setup notes to capture
   state, preview, and saved receipts. Run the frozen recorder's `prepare-review`
   and confirm it accepts those captures. The preview must include its image-byte
   `sha256`, and the saved receipt must include the matching document `revision`.
   Record this preflight separately from measured trials. A failure blocks both
   arms until the common setup is corrected and frozen again.

The historical runtime at the guide baseline lacks these receipt fields and
cannot supply evidence for the current recorder. Do not synthesize missing
fields or weaken evidence checks. A change to the common package or recorder
after trials begin requires a new matched comparison setup; do not pool runs
from different setups.

This index-only comparison does not evaluate separate changes to `SKILL.md` or
SDK guidance. For a different comparison, freeze and name its changed files
before execution. Keep targeted regression checks separate from comparative
adoption evidence.

### Rule mapping

| Target | Existing guidance | Candidate clarification | Evaluation |
| --- | --- | --- | --- |
| Width | Project extent ratios and vertical-growth preference | Ratios and vertical growth are defaults; viewport and comparison needs govern exceptions | Timeline continuity, reading size, navigation |
| Text size | Quality checks at intended display size | Separate overview labels from zoomable detail labels; shrinking to fit is not sufficient | Overview/detail reading, partial-edit labels |
| Emphasis | Dark/light treatment reserved for the central message | Identify this as a project preference; preserve explicit choices and meaningful existing styles | Concept emphasis and unchanged visual meanings |
| Conflicts | Purpose, structure, local edits, project conventions | Completion conditions precede optimization; relax defaults before changing scope | All cases, especially local-edit preservation |
| Drawing workflow | Structural draft and final quality check | Explicit check–revise loop, recheck after refinement, then confirmed saving and delivery | All cases: required facts and relationships survive revision; final artifact is readable and saved |

These are conditional design decisions and project defaults, not new empirical
claims about universally superior layouts. No new scientific thresholds are
introduced into the Skill.

## Inputs and isolation

Use [timeline](timeline.md), [concept](concept.md), and
[partial edit](partial-edit.md) as the three agent prompts. Supply only the
selected prompt, the assigned Skill, and its required initial note. Keep this
README and other arms' results out of the agent's context. Substitute the same
explicitly selected registered vault and a unique disposable note path per run.
Do not choose a vault from recent activity. Keep evaluation drawings under
`workspace/drawings/` in that vault; do not edit production notes.

For each case and arm, use a fresh conversation, the same model/reasoning/tool
settings, SDK/plugin versions, theme, and viewing conditions. Alternate arm
order. The input language is English in both arms. Let the agent complete its
normal inspection and self-correction without evaluator hints. Stop a run at
30 minutes or 80 recorded bridge CLI invocations and record an incomplete result
rather than silently granting extra time to one arm. This measurable budget
replaces the ambiguous historical tool-call count for future comparisons;
do not retroactively rescore earlier runs. These are evaluation budgets, not
Skill rules. If the host exposes agent tool counts, record them separately.

Use a light-theme 1280 × 800 CSS-pixel drawing viewport with 100% browser/OS
scaling and record the actual environment. Inspect the complete frame fitted
to viewport width, using vertical movement when needed; additionally inspect
the complete frame fitted to the viewport. Use 100% canvas zoom for details and
record any extra navigation required to answer the questions below. Evaluate
the image at the stated display size, not its raster file's native resolution
(SDK raster pixel ratio can be 2). If this viewport cannot be reproduced, freeze
one common alternative before either arm runs.

### Partial-edit fixture setup

[partial-edit.initial.json](partial-edit.initial.json) is an `apply` operation
array with stable IDs, a frame, four labeled nodes, three arrows, and six arrow
bindings. It is a setup input, not the expected solution.

Using the selected vault, create a disposable note with `create` and a unique
request ID. Apply the fixture with the returned revision and another request ID:

```sh
python3 bridge.py --vault <vault> --request-id <setup-id> apply <note.md> --revision <revision> --input docs/evaluations/diagramming/partial-edit.initial.json
```

Inspect `state`, `saved`, and a preview using the current bridge contracts.
SDK validation and appearance must be checked in the installed environment;
offline JSON validation alone does not establish that the fixture renders.
The worker is intentionally narrow; its text may grow vertically under the SDK.
The fixture need not initially be attractive, but its labels and bindings must
exist and the three relationships below must be represented accurately.
If SDK adaptation is necessary, freeze the adapted fixture before either arm.

Create one verified master fixture, close its session after persistence is
confirmed, then copy its entire note to fresh per-run paths without rewriting
embedded drawing records. Snapshot each run's initial state, bindings, and
preview. Never reuse a note modified by a previous run. Exclude setup work from
the measured editing time and tool calls. The master fixture's live validation
is part of evaluation setup and has not been established by package checks.

## Guide comparison: staged execution

1. Run each case once per arm as a smoke check (6 runs). Baseline drawing defects
   are observations and potential improvement targets; they do not by themselves
   prevent comparison. A broken environment or invalid common fixture blocks
   both arms until repaired. New serious candidate defects require revision
   before the full comparison. Record incomplete baseline runs as failures.
2. Freeze the candidate after any smoke-driven revisions. Run each case three
   times per arm independently (18 new runs). Do not pool smoke results with
   these results. A later candidate change starts a new comparison; do not select
   only favorable earlier runs. Reuse unchanged baseline runs only with matching
   frozen inputs and environment, explicitly identifying them.
3. Evaluate the agent's completion-state artifact before any human correction.
   Keep intermediate self-corrections as workload records, not as final defects.
   Then correct a separate copy to the same acceptance criteria and record human
   repair items and minutes. Preserve the original output and preview.

Three repetitions are exploratory. Inspect per-case results rather than
claiming statistical significance or general effectiveness across diagram types.

## Evaluator rubric

For every check record pass/fail and a specific observation. Where possible,
hide the arm from the evaluator. Evaluate relationships from the source facts,
not resemblance to a preferred layout. Alternative valid formats are allowed.

| Case | Required meaning and reader questions | Visual and preservation checks |
| --- | --- | --- |
| Timeline | All supplied events and times; the two confirmed causal links; no invented cause for the metrics restart. Can a reader distinguish when service recovered from when the queue cleared? | Participant identities and time direction visible in overview; event labels readable at detail zoom; no misleading unmarked time scale or obscured connectors. Record pans/zooms to trace the incident. |
| Concept | Every supplied dependency; cache is optional and origin remains necessary for a miss. Can a reader explain why a cache hit avoids origin access and what invalidation does? | Overview shows the hit/miss distinction; details readable at detail zoom. Main emphasis serves that distinction, with labels or paths conveying it independently of hue. No mandatory palette or dark-fill count. |
| Partial edit | Exactly Client → API → Worker → Database, with the original three connection meanings and worker label preserved. Can the reader trace the same flow after the edit? | Worker text readable at 100% zoom with no overlap/clipping; only worker and its two incident arrows/bindings may change. Compare all other shape/binding records exactly (ignore document revision/session metadata); preserve frame, positions, styles, labels, and IDs. |

A missing/reversed required relation, invented causality, unreadable required
label at its assigned viewing level, unconfirmed saved outcome, or an unauthorized
meaning change is a major defect. Missing facts that prevent answering a required
question are major as well. Spacing inconsistencies that do not obstruct reading
are minor. Record the reason, not just a severity count. Check actual arrow
bindings and saved records as well as images.

## Results and adoption

Before smoke execution, freeze inputs, major-defect definitions, viewing setup,
and the following provisional thresholds. Changing them requires a new evaluation
version, not retroactive relabeling of results.

- Record run ID, case, arm, guide/runtime versions and hashes, environment,
  prompt/fixture hashes, start/end time, completion/timeout status, final note,
  state, saved result, previews, and evaluator observations.
- Record final major/minor defects, reading-check outcomes, agent correction
  cycles, human repair items/minutes, tool calls, and elapsed execution time.
  Record actual tokens when available; otherwise label read-character counts as
  a proxy and leave token counts unavailable. Retain input/output usage separately.
- Freeze a measurement plan before running. Use the same counting unit in both
  arms. If actual tokens, a comparable read-character proxy, or measured human
  repair effort are unavailable, leave them unavailable and mark the associated
  acceptance criterion unassessed; narrow the claim or defer adoption. Do not
  waive thresholds after seeing results.
- For observed correction cycles, record the defect addressed and whether the
  next inspection resolved it while preserving required facts and relationships.
  Do not require artificial failures or reward extra cycles; a correct first
  candidate is acceptable, and unneeded iteration counts toward workload.
- For each case report all three outcomes, defect/reading pass counts, and
  medians for human repair effort and execution workload. Do not hide failed or
  incomplete runs. Keep setup costs separate. An incomplete run fails completion
  and cannot be counted as a cheap successful result.
- Adopt provisionally only if all candidate comparison runs complete with no
  major defects, candidate minor defects and preservation failures do not worsen
  in any case, and at least one case improves reading pass count or median human
  repair items/time without a regression in the other repair/reading measures.
- For any per-case median, allow at most 25% more elapsed time and tool calls,
  and 30% more actual input tokens or, when unavailable, read-character proxy.
  For a zero baseline value require no increase, rather than divide by zero.
  These are trial acceptance settings, not universal performance standards.
- An improvement must occur in at least two of three runs, rather than depend on
  one unusually good result. Disagreement or substantial variability means defer
  adoption and investigate, not automatically add more instructions.

If these conditions are not met, simplify or narrow the candidate and evaluate
again. Preparation of the kit, a smoke pass, or package consistency alone does
not constitute behavioral adoption. Keep run artifacts and result sheets in a
separate `workspace/` evaluation directory, not in the distributed Skill.
