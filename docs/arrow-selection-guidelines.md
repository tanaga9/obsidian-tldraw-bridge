# Arrow selection guidelines

The routing, visual connection direction, terminal symbol, and relationship
direction guidelines below are established project conventions. Binding patterns
are provisional and remain subject to continued evaluation, as marked in their
section. These are project guidelines, not official tldraw rules. They have not
been incorporated into the distributed Skill.

Choose arrows so readers can naturally understand relationships and flows from
their appearance. Use consistent representations for relationships with the
same meaning.

This document covers routing, visual connection direction, terminal symbols,
relationship direction, and provisional binding patterns. General appearance
properties such as color and size are outside its scope.

## Routing: `kind`

| Choice | Selection guideline |
| --- | --- |
| `arc` | Use for ordinary connections that express direct relationships or natural flows between nodes. Start with a straight line; introduce a curve when it avoids overlapping lines or makes a relationship easier to read. |
| `elbow` | Use when right-angle routing makes an exceptional path, loop return, or retry easier to distinguish from the main flow. Also use when the diagram's structure or layout makes this routing easier to read. |

Do not rely on routing shape alone to communicate meaning. Support it with
placement, arrow direction, and labels.

## Visual connection direction

For a relationship between whole nodes, prefer a direction that connects their
centers or visual centers of gravity. The line should appear to lead naturally
into each node as a whole.

For example, when connecting two horizontally elongated rectangles placed
diagonally relative to each other, start with a straight line between their
centers. The visible line ends at their outlines, while its extension points
toward both centers.

Connecting the midpoints of the left or right edges can look less natural in
this arrangement: although the attachment points are regular, the diagonal
line's extension misses the nodes' centers of gravity. Do not choose these
points solely for their geometric regularity.

Prefer a particular side or attachment position when that position has meaning,
such as an input, output, port, or a specific location inside a node.

## Terminal symbols: `arrowheadStart` / `arrowheadEnd`

| Choice | Selection guideline |
| --- | --- |
| `arrow` | Use as the standard symbol for direction. |
| `triangle` | Can substitute for `arrow` intuitively. Choose it when the terminal or direction should stand out more clearly. |
| `none` | Use without a terminal symbol, such as at the start of a one-way arrow or for an undirected relationship. |
| `square`, `dot`, `pipe`, `diamond`, `inverted`, `bar` | Use when a notation or legend defines their meaning. Do not use them as direct substitutes for `arrow`. |

As a rule, use either `arrow` or `triangle` consistently for relationships with
the same meaning. When adopting an established notation such as UML, follow
that notation's meanings, including any meaning assigned to `triangle`.

## Relationship direction

| Relationship | Start → end |
| --- | --- |
| One-way | `none` → `arrow` or `triangle` |
| Bidirectional | `arrow` or `triangle` at both ends |
| Undirected | `none` → `none` |

Use two separate arrows when the forward and return relationships have different
meanings, conditions, or routes.

## Binding patterns (provisional)

Treat the following as starting patterns for continued investigation, not settled
rules. Choose the connection's intent first, then select a complete combination
of `snap`, `isPrecise`, `isExact`, and `normalizedAnchor`. Judge the result by
its rendered appearance and behavior after layout changes.

These recommendations come from an API-authored study on 2026-10-29 using
Obsidian tldraw plugin 1.32.0: 53 arrows across eight pages, including node moves,
resizing, side reversals, self-loops, multiple inputs, and internal annotations.
Most targets were unrotated rectangles. Previews and persisted bindings were
checked. Pointer gestures and hover behavior were not tested. The study supports
these starting patterns within that scope; it does not establish universal
behavior across shapes or SDK versions.

See the separate [Arrow binding pattern study](studies/arrow-binding/README.md)
for the editable comparison diagram, WebP previews, construction scripts, and
verification records. Preserve that evidence when revising these recommendations.

### Understand the connection as a whole

- `isPrecise: false` aims at the node's center; `true` uses the specified anchor.
  For elbow arrows, the precise anchor can also influence the attachment side.
- `isExact: false` normally stops around the outline, with visible clearance
  where appropriate. `true` reaches the anchor itself. An exact endpoint can be
  inside the node or on its boundary, depending on the anchor.
- `snap` is part of the elbow binding recipe. Setting its value alone does not
  necessarily relocate an existing anchor or change the visible route.
- `normalizedAnchor` gives the intended position relative to the target's
  bounding box: top-left `(0, 0)`, center `(0.5, 0.5)`, bottom-right `(1, 1)`.
  An intended anchor and a visible endpoint are not necessarily the same point.

Binding settings apply independently to each terminal. For example, an
annotation can leave its source at the outline but reach an exact internal
point in its target.

### Select by intent

| Intent | Provisional starting pattern | What to inspect |
| --- | --- | --- |
| Ordinary relationship between whole nodes | Straight `arc`; `isPrecise: false`, `isExact: false`, `snap: none`, anchor `(0.5, 0.5)` | Whether the line naturally points toward both visual centers, especially for diagonal connections between wide nodes |
| Whole-node elbow connection with automatic attachment-side selection | `elbow`; `isPrecise: false`, `isExact: false`, `snap: center`, anchor `(0.5, 0.5)` | Whether automatic side selection produces a readable route after moving or resizing nodes |
| Deliberate side of entry or exit, including return paths | `elbow`; `isPrecise: true`, `isExact: false`, `snap: edge-point`; choose top `(0.5, 0)`, right `(1, 0.5)`, bottom `(0.5, 1)`, or left `(0, 0.5)` | Whether keeping those sides still serves the relationship after a layout change, rather than creating an unnecessary detour |
| Separate multiple connections along one side | `elbow`; `isPrecise: true`, `isExact: false`, `snap: edge`; distribute boundary anchors, for example `(0, 0.2)`, `(0, 0.5)`, `(0, 0.8)` | Whether each line remains traceable and attachment positions have enough separation |
| External self-loop | `elbow`; both ends precise and non-exact, with `edge-point` or `edge` and two distinct boundary anchors | Whether the loop actually travels outside the node, with a clear return arrowhead |
| Annotation pointing inside a node | Usually straight `arc`; target end `isPrecise: true`, `isExact: true`, `snap: none`; specify the internal anchor | Whether the tip identifies the intended location without obscuring text; keep the source non-exact if it represents a whole annotation node |
| Deliberate contact at an outline port | At the contacting end, `isPrecise: true`, `isExact: true`, with an actual boundary anchor; tested arc used `snap: none`, tested elbow used `snap: edge-point` | Whether exact contact is necessary and the arrowhead remains distinct from the outline |

The port pattern records tested API combinations; it does not prescribe the
binding generated by a UI gesture. Do not generalize the rectangular boundary
coordinates above to a different shape without inspecting its actual outline.

### Avoid misleading shortcuts

- Do not equate precise with visually better. For ordinary diagonal connections,
  fixing side midpoints can weaken the impression of a whole-node relationship.
- Do not assume exact is required for a reliable binding. Enable it when reaching
  a specific point matters; ordinary relationships generally benefit from
  stopping around the outline rather than crossing node contents.
- Do not use `snap` names as complete attachment instructions. In the study,
  identical interior anchors with precise true and exact false produced identical
  ordinary elbow paths for all four snap values. In contrast, self-loop routing
  differed between `none` and `edge-point` with the same boundary anchors.
- Do not read `snap: none` as unbound or unrestricted. A precise anchor can still
  influence an elbow's attachment side and produce a long detour.
- Do not rely on `kind: elbow` alone for a self-loop. Center-to-center bindings
  collapsed in the tested case; a non-exact `none` variant with boundary anchors
  routed within or along the node instead of making a clear external loop.

### Continue evaluation

Keep these recommendations provisional until representative additional cases
have been inspected. Prioritize rotated and nonrectangular nodes, open paths,
crowded layouts, parallel arrows between the same pair, and pointer-generated
bindings. Do not assume arbitrary obstacle avoidance by elbow routing.

For each extension, record the environment, intent, complete binding settings,
rendered result, behavior after relevant edits, and saved-state verification.
Distinguish observed behavior from a visual preference or an inferred rule.
When evidence disagrees with a recommendation, revise its scope or recipe;
do not preserve it merely for consistency with an earlier recommendation. Recheck after relevant
SDK changes. This is an ongoing evaluation process, not a scheduled automation.

## Review checklist

- Is it immediately clear which nodes each line connects?
- Does a connection between whole nodes look naturally aligned with their visual centers of gravity?
- Can readers distinguish the main flow from exceptional and return paths?
- Do crossings, overlaps, or unnecessary bends obscure relationships?
- Do arrow direction and labels match the intended meaning?
- Are relationships with the same meaning represented consistently?
- Do the binding settings and anchors match the intended whole-node, side, port, or internal-point relationship?
- After moving or resizing nodes, are attachment sides, clearance, labels, and return paths still readable?
- If using a provisional binding pattern outside its tested scope, has its actual rendering been checked?

## Official property references

These references establish the available tldraw properties and values. The
selection recommendations above are project conventions; binding patterns retain
their explicitly provisional status.

- [Arrow properties](https://tldraw.dev/reference/tlschema/TLArrowShapeProps)
- [Arrow kind and terminal symbol definitions](https://github.com/tldraw/tldraw/blob/main/packages/tlschema/src/shapes/TLArrowShape.ts)
- [Arrow binding properties](https://tldraw.dev/reference/tlschema/TLArrowBindingProps)
- [Elbow snap values](https://tldraw.dev/reference/tlschema/ElbowArrowSnap)
