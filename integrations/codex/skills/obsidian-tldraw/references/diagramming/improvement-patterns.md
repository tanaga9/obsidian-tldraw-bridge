# Diagram improvement conversations

Use for requested improvements, dissatisfaction, or a task-relevant issue found
by the agent. Keep normal quality checks within the requested work.

## When to propose

Suggest proactively when an observed issue affects the established reader task
and a concrete change would help. Name the affected content and consequence,
such as unreadable required labels at sharing width or an unclear next step.
Explain the change, expected benefit, and significant rework. Prefer a natural
review point unless the issue blocks the work.

Respect user constraints and declined proposals. Do not search unrelated diagrams
for improvements or propose preference-only changes. A proposal does not expand
editing scope: perform known in-scope corrections normally, and keep broader
changes as suggestions unless already authorized.

## Ordinary improvement and structural redesign

For an existing diagram, default to ordinary improvement: resolve the requested
problem while retaining its main structure, representation, and useful content.
Local regrouping, spacing, label, and connection corrections remain routine
when they preserve that overall organization.

Structural redesign substantially replaces the diagram's main organization or
representation, or splits/combines its overview and detail views. Proceed when
the user explicitly requests that extent or has agreed to a concrete proposal
covering it. Reuse that authorization; do not ask again for routine decisions
within the agreed scope. A generic request such as "improve this" or "make it
clearer" alone does not authorize structural redesign.

When redesign appears necessary but is not yet authorized, explain the observed
reader problem, why retaining the structure would not resolve it, what would
change, and what useful content would remain. Prepare the smallest useful
comparison sketch in a separate draft when needed to make the proposal
reviewable, preserving the current usable diagram. Agree on the proposed extent
before applying the redesign to the delivered diagram. Continue known in-scope
corrections without waiting when they remain useful independently.

Design recovery gathers evidence for a next decision. Entering recovery or
finding a promising trial does not authorize structural redesign or expand the
agreed editing scope.

## Diagnose and ask

Assume the user recognizes difficulty without knowing its cause. Inspect the
diagram against its purpose, facts, relationships, and viewing conditions; the
agent owns diagnosis. Proceed when evidence supports a direction. If the next
structural choice remains unclear, use [design recovery](design-recovery.md).

Ask only when the answer could change the direction. Offer two or three short,
intuitive choices about the reading experience, not notation or design causes:

> Which feels closest: "I don't know where to start," "I can read each part but
> can't see the overall point," or "There is too much to take in"?

Reuse established goals. Accept free-form answers, combinations, or "not sure."
If choices do not help, show a small comparison or revisit the hypothesis rather
than repeating questions. An answer is a clue, not proof of a cause: "too much"
may call for hierarchy or overview/detail separation rather than deletion.

## Choose a concrete measure

Connect an observed symptom to a change and an expected reader benefit. These
are candidates, not automatic diagnoses; combine them where useful and check
the intended effect after editing.

| Observed symptom | Measure | Expected benefit | Limits |
| --- | --- | --- | --- |
| Chronology and causality are mixed. | Put sequence on a directed time axis and show causality with separately labeled connections. | Distinguish what happened next from what caused it. | Do not infer cause from order; mark time spacing when it could mislead. |
| Required text becomes unreadable when the whole diagram fits the viewport. | Separate a compact overview from clearly linked detail views. | Grasp the whole, then follow the relevant detail. | Keep essential context visible and information needing simultaneous comparison together. Detail labels need not all be readable in a zoomed-out overview. |
| Boxes contain paragraphs but their relationships remain unclear. | Use short entity/action names, grouping, and explicit connections; move supporting prose to annotations or notes. | Read structure instead of reconstructing it from paragraphs. | Preserve essential qualifications and relationship meanings. Prefer prose if a diagram adds little. |
| Text and simple symbols do not evoke the entities or roles. | Add small, recognizable icon images at a few useful points, paired with labels and consistent scale/style. | Picture and recognize the entities while following relationships. | Keep icons selective and recognizable at display size; omit decorative or ambiguous images that crowd labels or connections. |
| Many elements compete; the main point or entry is hard to find. | Concentrate emphasis on the task's central elements using placement and restrained size, outline, or color differences. | Recognize where to start and what matters first. | Preserve equally critical branches, warnings, meaningful category cues, and adequate contrast. Essential meaning must survive without color. |

Choose an editing extent within the agreed scope that realizes the measure.
Recommend structural redesign directly when evidence shows the current structure
obstructs the purpose; do not exhaust cosmetic edits first. Apply it only under
the authorization conditions above. The extent of change does not substitute
for explaining the reader benefit. Carry forward required facts and useful
existing strengths.

Usually recommend one direction. For example: "The explanations become too small
at sharing width. Keep the main relationships in an overview and move supporting
explanations into linked detail views so readers can grasp the structure first."
Check that result through the normal [quality check](index.md#quality-check),
not by additional polish alone.

## Compare rough diagrams when useful

When structures are hard to judge verbally, draw two or three small alternatives
with meaningfully different approaches. Choose the reader task and question
first. Use the same essential facts, viewing size, and comparable polish; disclose
intentional information differences. Fix clipping or missing branches before
asking the user to compare structures. Inspect actual rendered diagrams, not
just descriptions of proposed alternatives.

> Which makes the flow easiest to follow: A, B, or C? You can combine features or
> say that none works yet.

Use the answer to choose or combine useful features. If none works, revisit the
purpose or hypothesis through recovery rather than generating endless variants.
Follow normal operation and persistence contracts; keep repository documentation's
intermediate previews in a temporary directory outside tracked documentation.

## Complete and retire drafts

Once a direction is supported and editing is in scope, return to normal
check–revise, refinement, verification, and saved delivery. Keep the previous
usable diagram during exploration. After adopting a replacement, remove unused
old pages/previews and update references when cleanup is in scope. Retain needed
language variants, comparison views, and useful independent edits.
