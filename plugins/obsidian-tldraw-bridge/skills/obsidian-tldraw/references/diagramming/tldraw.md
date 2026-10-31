# Obsidian tldraw implementation notes

Use this bridge's Editor API, not another tldraw application's HTTP server or custom helpers. Inspect the installed SDK's records rather than assuming the latest props or text format. See [operations](../operations.md) for supported methods.

## Styles

Bold text is currently outside this workflow's supported scope. When exceptional emphasis warrants a dark node, use regular light text and verify readability in the preview.

Use `style-spec <path> --shape-type <type>` before choosing uncertain style values. Enum names do not establish appearance: `semi` need not mean translucent, and a property name can also be one of its values. SDK style defaults, ShapeUtil defaults, and the Editor's current next-shape style are separate values. Explicit props override creation styles; creation hooks may further change a shape. Unavailable fields are unknown. Verify appearance with a preview in the target environment.

For example, the inspected plugin 1.32.0 renders a blue `solid` fill as a pale tint and a blue `fill` as saturated blue. Shape `opacity` affects its label as well as its body; use separate opaque text over a translucent background shape when independent opacity is needed. Keep such label backgrounds small enough not to obscure nearby enclosure boundaries or arrowheads.

## Frames

Apply the [one-frame-per-diagram convention](index.md#project-conventions) with an actual named frame shape and make the diagram's shapes its descendants; a rectangle or group alone does not provide the diagram frame. Use ordinary shapes for internal enclosures. Frame boundaries have no `dash` style, so use enclosure shapes when a styled boundary is needed. When reparenting, account for local coordinates and verify page positions. Choose parents for cross-frame arrows according to their relationship and rendering rather than moving every connector into a frame mechanically.

### Focused views, nesting, and deliberate overlap

Use [focused views](index.md#freeform-diagram-techniques) to control how much
information an exported image presents while retaining one editable source.
Choose the mechanism by the intended result:

| Intended result | Method and conditions |
| --- | --- |
| A contained subdiagram appears both on its own and within a larger diagram | Nest its frame and make its content descendants of that frame. Accept the inner clipping and the inner frame's visible decoration in the larger export. |
| Deliberately conceal distracting content in a composed view | Overlap frames and set the hierarchy and sibling order so the foreground frame's background masks the intended region. Preserve the source shapes; verify that required labels and connections remain understandable. This changes the rendered composition wherever those frames are included. |
| Export several independent regions of one master drawing | Use `preview --bounds X Y W H` in page coordinates. Extra frames are unnecessary; visible frames can add unwanted decoration or occlusion. See [image preview](../operations.md#image-preview). |

Keep these mechanisms separate (verified with plugin 1.32.0 / SDK 5.4.0):

- **Membership:** Exporting a frame alone includes its descendants. A shape has
  one parent; an overlapping sibling's content is not included. Sending a frame
  backward can reveal shapes on the page without including them in its export.
- **Clipping:** Ordinary descendants are clipped by their ancestor frames.
  Moving content into an inner frame also clips it in the outer frame's export.
  Exporting the inner frame alone retains clipping from its ancestors; a frame
  extending beyond its parent can export smaller than its nominal dimensions.
  Arrows have a separate SDK clipping exception, so inspect boundary-crossing
  connectors rather than assuming the same behavior as boxes.
- **Stacking and decoration:** Frames have backgrounds, borders, and names.
  A foreground frame can hide a sibling shape behind its background. Rendering
  order depends on hierarchy and sibling `index`, not a single page-wide Z
  value. A single-frame export omits that frame's own decoration but retains
  nested frames' decoration.
- **Bounds:** A bounds export crops the rendered whole page, including
  surrounding shapes and their occlusion. It does not undo ancestor clipping
  or recover content hidden behind a frame background.

Inspect `state`/`observe` for actual parents and sibling order after placement;
geometric containment alone does not establish parenting. Export every intended
view and inspect its context and readability. Recheck affected views when shared
content, frame bounds, parenting, or stacking changes. GUI and Markdown embed
export paths may differ; verify the path actually used rather than extending
these SDK-export observations to all hosts.

## Connections and rendered dimensions

For arrow creation, routing, or rebinding, read [Arrow selection and bindings](arrows.md) for routing and terminal choices, semantic connections, and provisional SDK recipes. Keep meaningful arrows bound to their actual target shapes; visual contact alone does not establish a binding. An annotation aimed at a node also needs that binding; genuinely open or decorative endpoints may be unbound.

A geo shape's effective height can include `growY` after text wrapping, and a text shape's rendered width includes `props.scale`. Compare actual rendered bounds rather than raw `w`/`h` values when fitting labels or balancing padding. Equal `props.h` values and equal normalized anchors do not guarantee horizontal arrows. Give peer boxes sufficient room for their labels and align their actual centers or attachment points after layout settles. Preserve bindings when correcting slopes.

Prefer a line or arrow's native label over a separate text shape placed on top, where native labels are supported. Keeping the label with its connector reduces misalignment and missed updates when moving or reconnecting it. Use separate overlaid text when the native label cannot provide the required placement or styling, and only when the edit scope permits adding shapes.

Prefer `mono` for native connector labels when no explicit font choice or existing meaningful style takes precedence. Verify wrapping and clipping in exports at their intended display size, including incident-arrow labels after resizing or rebinding a node. Adjust the local label layout and re-export as needed. Preserve label text and bindings.

## Verification

Apply the [common quality check](index.md#quality-check) using `state` for frame membership and arrow bindings and `preview` for rendered appearance, including accidental slopes after layout changes. Structure checks and image inspection complement each other; neither alone establishes both correctness and readability.
