# Diagramming guidance

Choose the diagram format that best answers the user's request and the reader's question. First consider established formats, including UML; use one when it fits well. Rely on familiar conventions without loading tutorials.

| Purpose | Starting point |
| --- | --- |
| Steps and conditional branches | Flowchart |
| Workflow, responsibilities, and handoffs | UML activity diagram, swimlane diagram, BPMN |
| Actors and system goals | UML use case diagram |
| Types, instances, and relationships | UML class or object diagram |
| Messages between participants | UML sequence or communication diagram |
| States, events, and time-dependent behavior | UML state machine or timing diagram |
| Coordination across interactions | UML interaction overview diagram |
| Modules, interfaces, and organization | UML component, package, or composite structure diagram |
| Runtime nodes and deployed artifacts | UML deployment diagram |
| System context, boundaries, and architecture levels | C4 diagram |
| Data entities and relationships | Entity–relationship diagram (ERD) |
| Data movement and transformation | Data flow diagram (DFD) |
| Hierarchy or radial topic organization | Tree diagram, mind map |
| Schedule, duration, and dependencies | Gantt chart, PERT diagram |

These are candidates, not an exhaustive catalog or mandatory notation. Preserve explicit creative choices and existing conventions. A local correction does not call for a full redesign. Verify the relevant standard when strict conformance is requested.

When none fits the intended meaning well, use an **Informal Diagram / Ad hoc Diagram**: choose or combine boxes and arrows, concept maps, rich pictures, sketchnotes, cluster diagrams, causal loop diagrams, and architecture sketches. Include flowchart or swimlane elements where useful. These building blocks can also be established formats in their own right; the informal composition need not conform to one notation. Make relationship meanings clear with labels or a small legend when needed.

## Common rules

- **Text serves the diagram:** Use layout, grouping, and connections to convey structure; avoid text-heavy diagrams that merely arrange prose in boxes. Prefer concise labels, but use full sentences without hesitation when they are needed for clarity or accuracy.
- **Explanations have a place:** Do not cram long passages into boxes. Use nearby annotations for supporting explanations, or propose a companion Markdown document for extended detail. Keep essential labels and qualifications in the diagram so it remains understandable.

### Quality check

After visual edits, inspect both the diagram's structure and its rendered appearance on each edited page. Check for unintended dangling or misconnected arrows, text overflow or clipping, lines crossing text, overlapping labels or shapes, and unreadable wrapping or sizing. Distinguish intentional open endpoints or overlaps from mistakes. Fix defects and inspect the updated rendering before completion.

## Project conventions

- **Named frames:** Normally put each coherent diagram in one descriptively named frame, including standalone diagrams. This is a user-defined project default. Leave boundaries open for exploration or when framing would obscure the intended relationship.
- **Connector alignment:** Connections between aligned peers should be exactly horizontal or vertical. Small accidental slopes distract without conveying meaning. Check actual attachment points after labels wrap or shapes grow. Deliberate diagonals remain appropriate where the layout benefits from them.

For Obsidian tldraw edits, read [implementation guidance](tldraw.md). For editing and persistence contracts, use [operations](../operations.md) and the Skill entrypoint.
