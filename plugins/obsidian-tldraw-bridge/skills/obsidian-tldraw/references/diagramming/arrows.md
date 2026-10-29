# Arrow selection guidelines

The sections before **Binding patterns (provisional)** are established project
conventions. Binding patterns remain under evaluation. These are project
guidelines, not official tldraw rules. This is the canonical selection guide,
included in the distributed Skill. Preserve explicit user choices and meaningful
existing notation.

Choose arrows so readers can naturally understand relationships and flows from
their appearance. Use consistent representations for relationships with the
same meaning.

General appearance properties such as color and size are outside this guide's scope.

## Routing: `kind`

| Choice | Selection guideline |
| --- | --- |
| `arc` | Default for direct relationships and natural flows. Start straight (`bend: 0`); curve when it avoids overlap or improves readability. |
| `elbow` | Use for exceptional paths, loop returns, or retries when right-angle routing distinguishes them from the main flow. Also use when the layout makes this routing easier to read. |

Do not rely on routing shape alone to communicate meaning. Support it with
placement, arrow direction, and labels.

## Visual connection direction

For whole-node relationships, aim toward the nodes' centers or visual centers
of gravity. Choose specific sides or positions when they have meaning, such as
an input, output, port, or internal point.

For two wide rectangles placed diagonally, prefer a center-to-center direction,
with visible endpoints near the outlines. A diagonal joining side midpoints
misses the centers and can look less natural. Do not choose attachment points
solely for geometric regularity.

## Preserve semantic connections

Keep meaningful Arrow-to-node connections bound to the actual target nodes,
including return paths. Do not bind to a nearby caption or position an unbound
endpoint near a node merely to simulate a connection. Adjust routing, anchors,
or layout while preserving the relationship. Unbound endpoints are appropriate
when the intended meaning genuinely has no target node, such as an open endpoint
or a decorative arrow.

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

Choose the intent first, then a complete binding recipe. These starting patterns
were tested through the SDK in Obsidian tldraw plugin 1.32.0 / tldraw SDK 5.4.0,
mainly on unrotated rectangles. UI gestures and other geometries need separate
checks. Verify installed records and rendering when using another SDK version;
these patterns do not guarantee a particular route.

### Understand the connection as a whole

- `isPrecise`: `false` aims at the center of the target geometry's bounds, not
  an automatically detected visual center of gravity. `true` uses the specified
  anchor and can influence an elbow's attachment side.
- `isExact`: `false` normally stops around the outline; `true` reaches the aim
  point selected by `isPrecise`. With `isPrecise: false`, exact contact reaches
  the center even if the stored anchor is elsewhere. With `isPrecise: true`, it
  reaches the specified anchor, which may be on the boundary or inside the node.
- `snap`: use with the complete elbow recipe. Its value alone need not relocate
  an existing anchor; `none` does not mean unbound or unrestricted.
- `normalizedAnchor`: relative to the target's bounding box, from top-left
  `(0, 0)` to bottom-right `(1, 1)`. Center is `(0.5, 0.5)`.

Choose settings per terminal; the two ends may use different recipes.

### Select by intent

In the table, **precise** and **exact** mean the corresponding boolean is `true`;
**imprecise** and **non-exact** mean `false`.

| Intent | Provisional starting pattern |
| --- | --- |
| Whole-node relationship | Straight `arc`; imprecise, non-exact, `snap: none`, anchor `(0.5, 0.5)` |
| Whole-node elbow with automatic side selection | `elbow`; imprecise, non-exact, `snap: center`, anchor `(0.5, 0.5)` |
| Deliberate entry or exit side, including returns | `elbow`; precise, non-exact, `snap: edge-point`; choose a side midpoint |
| Separate connections along one side | `elbow`; precise, non-exact, `snap: edge`; distribute boundary anchors |
| External self-loop | `elbow`; both ends precise and non-exact, with `edge-point` or `edge` and distinct boundary anchors |
| Internal-point annotation | Usually straight `arc`; target precise and exact, `snap: none`, with the intended internal anchor |
| Meaningful outline-port contact | Contacting end precise and exact, with an actual boundary anchor; tested arc used `snap: none`, elbow used `edge-point` |

For rectangles, side midpoints are top `(0.5, 0)`, right `(1, 0.5)`, bottom
`(0.5, 1)`, and left `(0, 0.5)`. To separate left-side connections, for example,
use `(0, 0.2)`, `(0, 0.5)`, and `(0, 0.8)`. Inspect the actual outline for other
shapes; these are SDK recipes, not UI gesture instructions.

### Control outline clearance

Accept normal SDK clearance for ordinary connections; do not force gap removal.
Prioritize readable arrowheads and natural connection directions. Use exact
contact when touching a specific point matters, and verify the result at its
intended display size. Retain clearance if contact obscures the arrowhead.

### Check exceptions

- Reconsider fixed attachment sides after layout changes; they can cause detours.
- Verify that self-loops travel outside the node and have readable arrowheads;
  center-to-center elbow bindings collapsed in the tested case.
- Do not assume elbow routing avoids arbitrary obstacles. Adjust local routing,
  anchors, or layout if a return crosses unrelated content, preserving bindings.

## Review checklist

- Are the connected nodes, direction, and labels immediately clear?
- Are meaningful connections represented by bindings, rather than endpoints merely placed near nodes?
- Do whole-node connections naturally point toward visual centers?
- Are main flows, exceptions, and returns distinguishable and consistent?
- Are arrowheads readable without distracting crossings, overlaps, or detours?
- Do anchors match the intended relationship and remain appropriate after moves or resizes?
- Has rendering been checked at the intended size, including any use outside the tested scope?

## Official property references

These references establish the available tldraw properties and values. The
selection recommendations above are project conventions; binding patterns retain
their explicitly provisional status.

- [Arrow properties](https://tldraw.dev/reference/tlschema/TLArrowShapeProps)
- [Arrow kind and terminal symbol definitions](https://github.com/tldraw/tldraw/blob/main/packages/tlschema/src/shapes/TLArrowShape.ts)
- [Arrow binding properties](https://tldraw.dev/reference/tlschema/TLArrowBindingProps)
- [Elbow snap values](https://tldraw.dev/reference/tlschema/ElbowArrowSnap)
