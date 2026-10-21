# Diagramming guidance

## Production workflow

For new diagrams or substantial structural revisions:

1. **Clarify the purpose:** State in one sentence what the reader should understand or be able to decide, using the request and existing context. Identify the relationships needed—chronology, causality, or other structure—and choose the [format and layout](#format-selection) accordingly.
2. **Check a structural draft:** Before adding explanatory prose or visual polish, draw short element names and meaningful connections. Verify that placement, containment, and connections communicate the main relationships; this is a condition for proceeding to refinement. If they do not, revise the structure and check again. Necessary labels and concise qualifications remain appropriate. Distinguish different connection meanings, such as chronology and causality, with labels, line styles, or a small legend when direction alone is ambiguous.
3. **Refine and verify:** Add only the explanation and visual detail that serve the purpose. Perform the [quality check](#quality-check), correcting problems and inspecting the revision before considering the diagram complete. Move long explanations that obscure relationships into supporting notes.

Ask only when an unresolved choice would materially change the diagram's purpose or structure; reuse what the conversation already establishes. Prefer one concise question at a time with two or three outcome-oriented choices and room for a free-form answer. Show a structural draft early to refine direction, and ask follow-ups only for important ambiguities it reveals. Handle routine drawing decisions without questioning the user at every step.

Local corrections reuse the existing purpose and structure rather than restarting the workflow.

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

## Common rules

- **Show structure:** Use layout, grouping, and connections rather than turning headings and paragraphs into boxes. Avoid diagrams where most elements are explanatory prose, including short passages or annotations. Prefer concise labels, but use sentences when needed for clarity or accuracy. Put supporting explanation in annotations or supporting Markdown for extended detail. Markdown may live outside the drawing data block in the same note; it is not visible in the drawing view, so keep essential reader-facing information in the diagram or response. Follow [Markdown body edits](../operations.md#markdown-body-edits) when updating it.
- **Preserve meaning:** Make node identities and connection meanings clear. Enclosures and headings supply context: when their name, scope, or nesting changes, recheck the interpretation of their contents and retain essential context in labels.
- **Balance the layout:** Keep spacing and alignment coherent across comparable elements, with visual emphasis matching the diagram's purpose.
- **Refine without losing strengths:** Compare with the prior diagram before finalizing. Preserve useful information and effective visual choices, or convey their meaning another way.

### Quality check

After visual edits, inspect structure and rendered appearance on each edited page, including at the intended display size:

- **Meaning:** Independently of visual neatness, verify that the diagram enables the intended understanding or decision. Names, scope, relationship meanings, and arrow directions must remain clear, including inside changed enclosures. If a bullet list would convey almost the same information, reconsider what the layout and connections contribute; move extended explanation to prose.
- **Connections:** Check for unintended dangling or misconnected arrows. Distinguish intentional open endpoints and overlaps from mistakes.
- **Readability and balance:** Check text overflow or clipping, lines obscuring text, overlapping labels or shapes, and unreadable sizing or unnecessary wrapping. Compare padding and gaps across peers. What draws the eye first should match the diagram's purpose; enclosures and fills should not overpower the contents.

Fix defects and inspect the updated rendering before completion. If the structure fails the meaning or connection checks, revise the structure and verify it again; changes to prose volume or appearance alone do not establish completion.

## Freeform Diagram techniques

- **Time as an axis:** For events, consider arranging time horizontally or vertically in a clearly indicated direction. A long arrow spanning the event region along an unobtrusive edge of the diagram can make the overall time direction clear; label it as time and keep it separate from event connectors. This is especially useful for digital-system incidents, where physical spatial layout often provides little guidance: use the other axis for participants, components, or locations when helpful. Space events according to their density and readability; an event-order diagram need not use a uniform time scale. Mark it as not to scale, or show timestamps, elapsed-time labels, or axis breaks where spacing could mislead. When comparing durations or rates, use a consistent time scale or clearly marked scale changes. Sequence along the axis establishes chronology, not causation by itself.
- **Node composition:** Prefer wider-than-tall nodes and other text-containing shapes for horizontal writing, avoiding unnecessary wrapping without imposing a fixed aspect ratio. Allow other proportions when notation, content, or layout warrants them. Place names, optional icons, and short role labels consistently across peers; keep each icon with its node and distinguish names from supporting explanations.
- **Icons and illustrations:** Add small icons or spot illustrations when they help readers recognize an entity or imagine its role. Choose simple imagery that remains recognizable at the intended display size, pair it with clear labels, and keep its scale and style consistent with the diagram. Use images as supporting cues without competing with the relationships being shown.
- **Spacing:** Treat available space as valuable: keep the layout comfortably readable without wasting area. Use margins and padding deliberately where they improve legibility, grouping, or separation; avoid generous empty bands or oversized containers by default. Choose a small set of intervals for padding within nodes and enclosures and gaps between peers. Larger gaps may express hierarchy or separation. Balance visible clearances on all sides, including headings, icons, and connectors; make optical adjustments rather than forcing identical distances everywhere. When substantial supplementary material at the bottom is concentrated on the left and extends too far vertically, consider two columns to use the available width while preserving readable text and a clear reading order.
- **Enclosures and strokes:** A thicker outline can distinguish a grouping level. Pair thicker outlines, lines, or arrows with lower opacity where useful, keeping enclosures subordinate to their contents, often with a neutral color. Boundaries, paths, arrowheads, and labels must remain discernible.
- **Lightness and contrast:** Establish legibility and distinguish important boundaries primarily through lightness contrast; hue and saturation differences are supplementary. Use dark text on light backgrounds and light text on dark backgrounds, checking the rendered result including transparency. Preserve sufficient contrast without automatically maximizing it: if pure black against pure white feels harsh, use a softer near-black or off-white while keeping text and boundaries clear.
- **Labels over lines:** When deliberately placing text over a line or arrow, give the label a slightly translucent background color that contrasts with the text and softens the line beneath it. Keep the text itself opaque and the connection's path and direction clear.
- **Exceptional emphasis:** Reserve dark fills with light text for elements that are truly the central message of the material, such as an error or failure point in a troubleshooting diagram. Do not use this treatment merely to accent an ordinary component, even if only one node receives it. Use gentler color, outline, or placement differences for routine emphasis. When exceptional emphasis is warranted, prefer bold light text where supported; see the [tldraw text limitation](tldraw.md#styles) for this workflow.
- **Color as visual support:** Use hue and saturation as secondary cues for accents, gentle fills, and visual grouping, supported by adequate lightness contrast. Colored outlines and matching headings can provide distinction while preserving white space; not every node needs a fill. Keep the palette coherent, use color where helpful, and avoid assigning too many category meanings to it. Viewing conditions and color perception vary, so convey essential meaning through labels, placement, shape, or line style as well.

## Project conventions

- **Diagram extent:** Start with a landscape layout, roughly width:height = 1:0.75, as a flexible default. Fit the intended viewing width at a readable scale; when more space is needed, prefer growing vertically over horizontal sprawl because vertical scrolling is generally easier on a work PC. Let the relationships and content justify other proportions rather than forcing this ratio or shrinking text to fit. This concerns the whole diagram, while individual nodes may remain wider than tall.
- **Node outlines:** The default line style for node outlines is hand-drawn (`draw`).
- **Named frames:** Use one descriptively named frame per diagram as the project default. Use ordinary enclosure shapes for node groups, subsystem boundaries, and other containment within a diagram. Nested frames are rare: use them only when a diagram itself contains another diagram that warrants its own frame. Leave boundaries open for exploration or when framing would obscure the intended relationship.
- **Connector alignment:** Connections between aligned peers should be exactly horizontal or vertical. Small accidental slopes distract without conveying meaning. Check actual attachment points after labels wrap or shapes grow. Deliberate diagonals remain appropriate where the layout benefits from them.

For Obsidian tldraw edits, read [implementation guidance](tldraw.md). For editing and persistence contracts, use [operations](../operations.md) and the Skill entrypoint.
