# Diagramming guidance

## Production workflow

Use this workflow for new diagrams or authorized substantial structural revisions.

For an existing diagram, first establish that a substantial structural revision
is within the agreed scope using the [improvement and redesign conditions](improvement-patterns.md#ordinary-improvement-and-structural-redesign).
A general improvement request defaults to preserving the main structure;
choosing this production workflow does not itself authorize a redesign.

1. **Establish the task:** Use the user's purpose, source facts, audience, and viewing conditions to state what the reader should understand or decide. Identify the required facts and relationships, including useful content to preserve in an existing diagram, and choose the [format and layout](#format-selection).
2. **Draw a structural candidate:** For a new diagram, use the [initial sketch and collaborative expansion](#starting-a-new-diagram) approach below. If confidence in the design direction is insufficient, gather the missing information before committing to a structure, using the clarification guidance below. Once the direction is sufficiently supported, draw short element names and meaningful connections before visual polish or extended explanation. Use placement and containment to communicate the relationships. Keep necessary qualifications visible; distinguish different connection meanings, such as chronology and causality, with labels, line styles, or a small legend when direction alone is ambiguous.
3. **Check and revise:** Inspect the candidate against the task and the [completion conditions](#resolving-design-conflicts). If meaning, required content, or structure fails, revise the structure and check again. For readability problems, adjust layout, grouping, or detail level; relax obstructive project defaults before sacrificing meaning. Resolve incorrect connections or edits as well. Proceed when the candidate communicates the required relationships and can be read at its intended viewing level; supporting notes must not hide essential meaning.
4. **Refine and verify:** Improve navigation, consistency, appearance, and effort within those conditions. Add only explanation and detail that serve the purpose; move extended explanation into supporting notes. Perform the [quality check](#quality-check). If refinement breaks a completion condition, return to the affected structure or layout and recheck it.
5. **Save and deliver:** Confirm persistence using the [operation contracts](../operations.md), then provide the editable note and a useful preview or link for the user's task. Report any unresolved limitation instead of calling an unchecked or unsaved result complete.

Reuse what the conversation and available source material already establish. When uncertainty about the purpose, facts, audience, or representation could materially change the structure, gather evidence from those sources and ask the user focused questions where needed. Continue until the answers or evidence give reasonable confidence in the design direction; do not commit to a consequential assumption merely to produce a candidate quickly. Prefer one concise question at a time with two or three outcome-oriented choices and room for a free-form answer. When the available information sufficiently supports the direction, proceed with the next agreed increment without requiring confirmation for routine drawing decisions. For new diagrams, use the early feedback points below to agree on the main concept and how to expand the diagram.

Local corrections reuse the existing purpose and structure. Apply the check–revise loop to the affected content and connections, preserve unrelated content, and verify and deliver the saved result without restarting the whole design. Stop revising when the completion conditions are met; do not keep polishing without a task-relevant reason.

When improvement suggestions are requested, including feedback such as "this is
hard to understand," or an observed issue warrants a proactive suggestion, use
[improvement guidance](improvement-patterns.md). If the initial structure cannot
be chosen or revisions stop yielding useful findings, use
[design recovery](design-recovery.md). These are conditional aids, not extra
steps for known corrections or routine choices between acceptable layouts.

### Starting a new diagram

Begin with a simple, readable initial sketch of the main concept and its essential
relationships. Inspect and save it, then show it to the user to check whether it
matches their intended concept before building the full diagram. Treat this as an
initial draft, not completion of the full request. Reuse any direction already
established by the user; an explicit request for a complete first pass takes
precedence.

Offer a few concrete extensions to the initial sketch, explaining what each would add
or clarify. Incorporate the user's feedback and chosen extensions, inspect and
save the updated diagram, then repeat at meaningful increments while the diagram
is taking shape. Do not silently apply all proposed extensions before receiving
feedback. Extend the same page by default; use another page when a distinct topic
or detail view benefits from separation, keeping information that needs simultaneous
comparison together and making the relationship between pages clear.

If early feedback reveals a mismatch in the main concept, stop expanding and
identify its cause with the user. Revisit the purpose, assumptions, or representation;
consider restarting the initial draft when patching it would preserve the mismatch.
Use [design recovery](design-recovery.md) when the next direction remains unclear.
Once the main concept and scope are established, continue the production workflow to
complete the agreed diagram.

### Local revision loop

For successive corrections to an existing diagram:

1. Reuse the established purpose, representation, viewing conditions, and useful
   design choices. Reuse known IDs as lookup hints, not proof of current state.
   Observe the current targets and affected context before planning the edit;
   use exact records only where compact observation is insufficient.
2. Choose the review scope using the [scope decisions](#scope-decisions) below.
   Include incident connections and their labels, connected endpoints, affected
   containers, and nearby content as relevant. A subset's bindings may refer to
   shapes outside that subset; fetch their relevant context as well.
3. Batch related, understood edits in one `apply`. When the review region is
   known, include `--preview-output` and appropriate preview options to verify
   saving and export the resulting revision in the same request. Bounds crops
   retain surrounding content; ID-only exports omit unselected neighbors and
   connections. Choose enough context to detect affected defects.
4. Inspect the resulting image at the established viewing size and check affected
   meaning, connections, readability, and preservation of useful existing content.
   If a crop cannot establish the broader effect, inspect a wider export too.
   Reuse matching edit persistence evidence; re-observe and recheck saving after
   intervening changes. Correct remaining in-scope defects and inspect again;
   stop once the requested change and completion conditions are satisfied.

This combines execution and reuses context, not quality verdicts. Reconsider
structure when the request or observed effects require it. Follow the full
production workflow for substantial structural revisions; handle uncertain
outcomes through the operation recovery contract.

#### Scope decisions

Use the smallest scope that can establish the completion conditions from current
evidence. Choose autonomously for routine edits; the operation name alone does
not establish risk. A color change can alter meaning, and a short text change
can resize a box. Use these conditions rather than a mandatory score or report:

| Observed or expected effect | Review scope |
| --- | --- |
| Meaning, geometry, connections, and viewing scale remain stable; for example, a nonsemantic style adjustment | Inspect the changed content with enough surrounding context to judge contrast and consistency. A fresh local render is sufficient when effects stay contained. |
| Text wrapping, movement, resizing, alignment, rebinding, or grouping can affect neighbors | Inspect the changed elements, incident arrows and labels, endpoints, parent boundaries, and nearby peers. Prefer a context crop over isolated IDs; check actual rendered bounds and relevant bindings. |
| Meaning, membership, reading order, shared styles, frame extent, or export scale changes across a diagram; or local effects cannot be bounded confidently | Inspect the affected diagram at overview size and relevant details at intended reading size. Recheck its relationships and useful existing content. Use the production workflow when the structure needs revision. |

After the edit, widen the review if it reveals new wrapping or growth, clipped
text, overlaps, changed arrow geometry, boundary crossings, or an unexpected
change summary. Inspect exact records when needed to explain unexpected changes
or establish preservation; do not infer correctness from an image alone. If
effects reach a crop's edge or evidence does not establish their extent, inspect
the containing group or diagram. Re-observe after intervening edits or revision
conflicts; earlier review findings do not establish the quality of changed state.

Broader inspection does not authorize broader edits. Preserve protected content;
report an unrelated pre-existing defect instead of silently expanding the task.
Make routine in-scope quality decisions without asking permission. Ask only when
resolving an issue requires a consequential choice the task does not establish.

If successive fixes move the same defect elsewhere or undo earlier improvements,
diagnose its cause and reconsider the affected layout instead of continuing
cosmetic adjustments. Use [design recovery](design-recovery.md) when the next
structural step is unclear. Stop when the requested change, affected quality, and
preservation are supported by the inspected saved result. Reuse still-valid
context and matching receipts; do not add full-page exports, repeated discovery,
alternative designs, or written checklists without an identified reason. Briefly
explain consequential tradeoffs or unresolved limitations in delivery.

## Resolving design conflicts

Preserve accurate relationships, the requested purpose and scope, required readability and accessibility, and editing/persistence correctness. Treat these as completion conditions; visual polish or faster execution cannot compensate for failing them. Project conventions below are defaults, not universal perceptual constraints.

When requirements compete, first consider layout changes, grouping, or overview/detail separation while keeping essential meaning visible. Relax a project default when it obstructs meaning or readability; preserve explicit user choices and meaningful existing conventions. Use the clarification guidance in the production workflow when a tradeoff leaves consequential uncertainty about the purpose, information scope, or structure. Briefly explain consequential exceptions rather than documenting every routine adjustment.

Among acceptable designs, balance navigation, consistency, density, appearance, and execution effort according to the purpose and viewing environment. Do not require multiple rendered alternatives for routine decisions. Check the affected meaning, connections, and rendering after a change; use the existing operation contracts for persistence.

## Format selection

Briefly compare suitable representations and state the selection reason in one sentence. First consider established formats, including UML, and use one when it fits well. Rely on familiar conventions without loading tutorials.

| Purpose | Starting point |
| --- | --- |
| Processes and responsibilities | Flowchart, swimlane, BPMN, UML activity diagram |
| Goals, interactions, and lifecycles | UML use case, sequence, state diagrams |
| Software structure and architecture | UML structural diagrams, C4 |
| Data relationships and movement | ERD, DFD |
| Hierarchies and topics | Tree diagram, mind map |
| Schedules and dependencies | Gantt chart, PERT diagram |

These are candidates, not an exhaustive catalog or mandatory notation. Preserve explicit creative choices and existing conventions. Local corrections do not require repeating format selection or redesigning the diagram. Verify the relevant standard when strict conformance is requested.

When an established format such as UML is the best fit, suggest a dedicated tool such as Mermaid or PlantUML, choosing according to the notation needed. If those tools may not adequately express the required relationships, layout, annotations, or combination of forms, continue with the Obsidian tldraw workflow and briefly explain why. Respect explicit user choices of tool or format.

When none fits the intended meaning well, use a **Freeform Diagram** (also called an Informal Diagram or Ad hoc Diagram): choose or combine boxes and arrows, concept maps, rich pictures, sketchnotes, cluster diagrams, causal loop diagrams, and architecture sketches to express the intended relationships and structure. Include flowchart or swimlane elements where useful. These building blocks can also be established formats in their own right; the composition need not conform to one notation. Make relationship meanings clear with labels or a small legend when needed. The common rules below still apply.

For language variants and shared layout adjustments across languages, use the
[multilingual workflow](../multilingual.md).

## Common rules

- **Show structure:** Use layout, grouping, and connections rather than turning headings and paragraphs into boxes. Avoid diagrams where most elements are explanatory prose, including short passages or annotations. Prefer concise labels, but use sentences when needed for clarity or accuracy. Put supporting explanation in annotations or supporting Markdown for extended detail. Markdown may live outside the drawing data block in the same note; it is not visible in the drawing view, so keep essential reader-facing information in the diagram or response. Follow [Markdown body edits](../operations.md#markdown-body-edits) when updating it.
- **Preserve meaning:** Make node identities and connection meanings clear. Enclosures and headings supply context: when their name, scope, or nesting changes, recheck the interpretation of their contents and retain essential context in labels.
- **Flow direction:** Choose horizontal or vertical flow to suit the content, notation, diagram proportions, and available space; wide diagrams often benefit from horizontal flow. Within the chosen axis, prefer top-to-bottom for vertical flow and, more weakly, left-to-right for horizontal flow. The meaning being conveyed and the rules of the chosen notation take precedence over these directional preferences. Keep similar forward flows consistent, and use reverse directions for semantically opposite flows. Keep the layout compact and the flow easy to follow. Do not alternate the forward direction between rows or columns merely to fit the available space.
- **Balance the layout:** Keep spacing and alignment coherent across comparable elements, with visual emphasis matching the diagram's purpose.
- **Group stable compositions:** When multiple shapes form one object whose internal arrangement should stay intact, put them in an actual editor group so they can be selected and moved together. For example, group the head, body, arms, and legs of a UML-style actor assembled from basic shapes. Use groups sparingly: leave elements independently movable when that is useful, and avoid grouping merely because elements share a topic or enclosure.
- **Refine without losing strengths:** Compare with the prior diagram before finalizing. Preserve useful information and effective visual choices, or convey their meaning another way.

### Quality check

After visual edits, inspect structure and rendered appearance on each edited page, including at the intended display size:

- **Meaning:** Independently of visual neatness, verify that the diagram enables the intended understanding or decision. Names, scope, relationship meanings, and arrow directions must remain clear, including inside changed enclosures. If a bullet list would convey almost the same information, reconsider what the layout and connections contribute; move extended explanation to prose.
- **Connections:** Check for unintended dangling or misconnected arrows. Distinguish intentional open endpoints and overlaps from mistakes. Check that similar forward flows follow a consistent direction and that reversals convey a meaningful return, feedback, or other opposite relationship.
- **Readability and balance:** Check text overflow or clipping, lines obscuring text, overlapping labels or shapes, and unreadable sizing or unnecessary wrapping. Compare padding and gaps across peers. What draws the eye first should match the diagram's purpose; enclosures and fills should not overpower the contents.

Judge text at its intended displayed size, not by canvas font size alone: fitting a large diagram into a small viewport can make large canvas text unreadable. In a zoomable detail diagram, overview labels must identify the main structure at overview size; detail labels may require the intended detail zoom. Do not require every detail label to be readable in the overview. Reuse viewing conditions from the request or existing diagram; otherwise make a practical assumption and ask only if the choice materially affects the result.

Fix defects and inspect the updated rendering before completion. If the structure fails the meaning or connection checks, revise the structure and verify it again; changes to prose volume or appearance alone do not establish completion.

## Freeform Diagram techniques

- **Time as an axis:** For events, consider arranging time horizontally or vertically in a clearly indicated direction. A long arrow spanning the event region along an unobtrusive edge of the diagram can make the overall time direction clear; label it as time and keep it separate from event connectors. This is especially useful for digital-system incidents, where physical spatial layout often provides little guidance: use the other axis for participants, components, or locations when helpful. Space events according to their density and readability; an event-order diagram need not use a uniform time scale. Mark it as not to scale, or show timestamps, elapsed-time labels, or axis breaks where spacing could mislead. When comparing durations or rates, use a consistent time scale or clearly marked scale changes. Sequence along the axis establishes chronology, not causation by itself.
- **Node composition:** Prefer wider-than-tall nodes and other text-containing shapes for horizontal writing, avoiding unnecessary wrapping without imposing a fixed aspect ratio. Allow other proportions when notation, content, or layout warrants them. Place names, optional icons, and short role labels consistently across peers; keep each icon with its node and distinguish names from supporting explanations.
- **Icons and illustrations:** Add small icons or spot illustrations when they help readers recognize an entity or imagine its role. Choose simple imagery that remains recognizable at the intended display size, pair it with clear labels, and keep its scale and style consistent with the diagram. Place them selectively at useful points rather than on every node; omit images that add no recognition value. Use images as supporting cues without competing with the relationships being shown.
- **Spacing:** Treat available space as valuable: keep the layout comfortably readable without wasting area. Use margins and padding deliberately where they improve legibility, grouping, or separation; avoid generous empty bands or oversized containers by default. Choose a small set of intervals for padding within nodes and enclosures and gaps between peers. Larger gaps may express hierarchy or separation. Balance visible clearances on all sides, including headings, icons, and connectors; make optical adjustments rather than forcing identical distances everywhere. When substantial supplementary material at the bottom is concentrated on the left and extends too far vertically, consider two columns to use the available width while preserving readable text and a clear reading order.
- **Enclosures and strokes:** A thicker outline can distinguish a grouping level. Pair thicker outlines, lines, or arrows with lower opacity where useful, keeping enclosures subordinate to their contents, often with a neutral color. Boundaries, paths, arrowheads, and labels must remain discernible.
- **Lightness and contrast:** Establish legibility and distinguish important boundaries primarily through lightness contrast; hue and saturation differences are supplementary. Use dark text on light backgrounds and light text on dark backgrounds, checking the rendered result including transparency. Preserve sufficient contrast without automatically maximizing it: if pure black against pure white feels harsh, use a softer near-black or off-white while keeping text and boundaries clear.
- **Labels over lines:** When deliberately placing text over a line or arrow, give the label a slightly translucent background color that contrasts with the text and softens the line beneath it. Keep the text itself opaque and the connection's path and direction clear.
- **Exceptional emphasis:** As a project preference, reserve dark fills with light text for elements that are truly the central message of the material, such as an error or failure point in a troubleshooting diagram. For routine emphasis, prefer gentler color, outline, or placement differences. Preserve an explicit user choice or an existing meaningful visual convention when it calls for another treatment. In either case, check that the strongest emphasis serves the reader's task, with labels or other cues carrying essential meaning as well as color. When exceptional emphasis is warranted, prefer bold light text where supported; see the [tldraw text limitation](tldraw.md#styles) for this workflow.
- **Color as visual support:** Use hue and saturation as secondary cues for accents, gentle fills, and visual grouping, supported by adequate lightness contrast. Colored outlines and matching headings can provide distinction while preserving white space; not every node needs a fill. Keep the palette coherent, use color where helpful, and avoid assigning too many category meanings to it. Viewing conditions and color perception vary, so convey essential meaning through labels, placement, shape, or line style as well.

## Project conventions

- **Diagram extent:** Adjust the overall width:height continuously as 1:n, with n determined by the content. Use three preferred reference proportions: 1:0.6 for an initial landscape layout, 1:0.7 when more vertical room is needed, and 1:1.4 for a taller layout. These are guides, not mandatory steps or exact targets; intermediate values and further vertical growth are equally valid. Fit the intended viewing width at a readable scale; growing vertically is the project's work-PC default, not a claim that horizontal navigation is always harder. Available viewport space and the need to compare related elements constrain the choice. Consider regrouping or overview/detail separation before shrinking text; allow extra width when a timeline, lanes, or dependencies benefit from horizontal continuity. Check the actual pan/zoom burden and readability rather than aspect-ratio compliance. Do not add empty space to match a guide value. This concerns the whole diagram, while individual nodes may remain wider than tall.
- **Raster export width:** For routine sharing, choose an actual image width between 1000 and 2000 pixels, balancing readability, file size, and ease of viewing. Adjust export scale rather than changing the drawing solely to reach that width, and inspect the result at its intended display size. This is a project default; explicit output requirements or detail needs may justify another width.
- **Text size:** Start with M. Use S for secondary annotations and L selectively for headings when they improve hierarchy or readability. Reserve XL for exceptional cases, only at the single highest heading level; do not use it for lower-level headings, node labels, or routine emphasis. Keep size differences restrained and comparable elements consistent, checking readability at the intended display size.
- **Node outlines:** The default line style for node outlines is hand-drawn (`draw`).
- **Text area within shapes:** When the largest inscribed rectangle available for text occupies little of a shape's area, as with diamonds, favor a compact shape with an outside label. Favor space-efficient text containers, while choosing shapes and label placement to suit notation, meaning, and layout.
- **Text alignment:** Use left-aligned text by default. Center alignment can suit labels over lines, arrows, or grouping enclosure boundaries. Choose center alignment (or, rarely, right alignment) when it improves readability or clarifies the relationship between the text and nearby elements.
- **Named frames:** Use one descriptively named frame per diagram as the project default. Use ordinary enclosure shapes for node groups, subsystem boundaries, and other containment within a diagram. Nested frames are rare: use them only when a diagram itself contains another diagram that warrants its own frame. Leave boundaries open for exploration or when framing would obscure the intended relationship.
- **Frame export names:** When exporting a frame as an image, keep its name equal to the output filename without the extension (for example, frame `system-overview` and file `system-overview.webp`), so manual exports use the same name. Usually choose the output filename first and rename the frame to match before exporting. Use judgment when an existing frame name or explicit naming requirement is more appropriate: choose the filename to match the frame instead, or retain a necessary difference when the task requires it.
- **Connector alignment:** Connections between aligned peers should be exactly horizontal or vertical. Small accidental slopes distract without conveying meaning. Check actual attachment points after labels wrap or shapes grow. Deliberate diagonals remain appropriate where the layout benefits from them.

For Obsidian tldraw edits, read [implementation guidance](tldraw.md). For editing and persistence contracts, use [operations](../operations.md) and the Skill entrypoint.
