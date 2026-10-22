# Obsidian tldraw implementation notes

Use this bridge's Editor API, not another tldraw application's HTTP server or custom helpers. Inspect the installed SDK's records rather than assuming the latest props or text format. See [operations](../operations.md) for supported methods.

## Styles

Bold text is currently outside this workflow's supported scope. When exceptional emphasis warrants a dark node, use regular light text and verify readability in the preview.

Use `style-spec <path> --shape-type <type>` before choosing uncertain style values. Enum names do not establish appearance: `semi` need not mean translucent, and a property name can also be one of its values. SDK style defaults, ShapeUtil defaults, and the Editor's current next-shape style are separate values. Explicit props override creation styles; creation hooks may further change a shape. Unavailable fields are unknown. Verify appearance with a preview in the target environment.

For example, the inspected plugin 1.32.0 renders a blue `solid` fill as a pale tint and a blue `fill` as saturated blue. Shape `opacity` affects its label as well as its body; use separate opaque text over a translucent background shape when independent opacity is needed. Keep such label backgrounds small enough not to obscure nearby enclosure boundaries or arrowheads.

## Frames

Apply the [one-frame-per-diagram convention](index.md#project-conventions) with an actual named frame shape and make the diagram's shapes its descendants; a rectangle or group alone does not provide the diagram frame. Use ordinary shapes for internal enclosures. Frame boundaries have no `dash` style, so use enclosure shapes when a styled boundary is needed. When reparenting, account for local coordinates and verify page positions. Choose parents for cross-frame arrows according to their relationship and rendering rather than moving every connector into a frame mechanically.

## Connections and rendered dimensions

Keep meaningful arrows bound to their target shapes. Touching a box visually does not establish a binding; inspect endpoint records. Decorative and annotation arrows may be unbound.

A geo shape's effective height can include `growY` after text wrapping, and a text shape's rendered width includes `props.scale`. Compare actual rendered bounds rather than raw `w`/`h` values when fitting labels or balancing padding. Equal `props.h` values and equal normalized anchors do not guarantee horizontal arrows. Give peer boxes sufficient room for their labels and align their actual centers or attachment points after layout settles. Preserve bindings when correcting slopes.

Check incident-arrow labels after resizing or rebinding a node. In plugin 1.32.0 / SDK 5.4.0, native `sans` arrow labels have been observed vertically clipped in raster previews despite complete stored text. If this occurs, test a local label-layout or font adjustment and re-export; `mono` resolved the reproduced case. Preserve label text and bindings. Use a separate text label only when the edit scope permits adding shapes.

## Verification

Apply the [common quality check](index.md#quality-check) using `state` for frame membership and arrow bindings and `preview` for rendered appearance, including accidental slopes after layout changes. Structure checks and image inspection complement each other; neither alone establishes both correctness and readability.
