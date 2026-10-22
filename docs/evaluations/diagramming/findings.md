# Reusable evaluation lessons

Keep decision-relevant lessons here. Individual run results, timings, hashes,
environment manifests, and artifact links belong in each local run's `report.md`,
using the [report template](report-template.md). This page is maintainer
documentation and is not included in the distributed Skill.

## Inspect affected connections, not only the requested node

A node edit can leave an existing incident-arrow label unreadable even when
the node itself improves. Assess the requested edit and the final readability
of affected connections separately. Preserve protected records; an unrelated,
pre-existing defect outside the permitted scope is not an introduced regression.
Do not count a faster edit as an improvement when an in-scope readability
defect remains.

## Reproduce export defects with a minimal change

Native `sans` arrow-label clipping has been reproduced in Obsidian tldraw 1.32.0
/ SDK 5.4.0 raster exports. A font-only change to `mono` resolved the reproduced
case. Runtime actions and scope constraints are maintained in the canonical
[SDK guidance](../../../integrations/codex/skills/obsidian-tldraw/references/diagramming/tldraw.md#connections-and-rendered-dimensions).

To investigate this class of issue again:

1. Use a disposable copy of the [partial-edit fixture](partial-edit.initial.json)
   or an affected saved note. Inspect the initial state and actual preview.
2. Preserve the failing artifact. On a separate copy, change one relevant
   property and re-export at the same viewing scale.
3. Verify label text, bindings, persistence, and protected records as well as
   appearance. Confirm the workaround in fresh editing trials before retaining
   a conditional SDK note.

Recheck this behavior after SDK or plugin changes. The workaround is not a
mandatory font convention or a guarantee for other versions. Targeted repair
checks do not establish that a whole guide is better; use the separate
[comparison protocol](README.md#results-and-adoption) for that claim.
