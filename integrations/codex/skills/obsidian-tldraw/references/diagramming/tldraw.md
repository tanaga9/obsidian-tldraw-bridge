# Obsidian tldraw implementation notes

Use this bridge's Editor API, not another tldraw application's HTTP server or custom helpers. Inspect the installed SDK's records rather than assuming the latest props or text format. See [operations](../operations.md) for supported methods.

## Styles

Use `style-spec <path> --shape-type <type>` before choosing uncertain style values. Enum names do not establish appearance: `semi` need not mean translucent, and a property name can also be one of its values. SDK style defaults, ShapeUtil defaults, and the Editor's current next-shape style are separate values. Explicit props override creation styles; creation hooks may further change a shape. Unavailable fields are unknown. Verify appearance with a preview in the target environment.

## Frames

Use actual frame shapes with descriptive names and make the relevant shapes children of the frame. Visual enclosure by a rectangle or group is insufficient. When reparenting, account for local coordinates and verify page positions. Choose parents for cross-frame arrows according to their relationship and rendering rather than moving every connector into a frame mechanically.

## Connections and rendered dimensions

Keep meaningful arrows bound to their target shapes. Touching a box visually does not establish a binding; inspect endpoint records. Decorative and annotation arrows may be unbound.

A geo shape's effective height can include `growY` after text wrapping. Equal `props.h` values and equal normalized anchors therefore do not guarantee horizontal arrows. Give peer boxes sufficient height for their labels and align their actual centers or attachment points after layout settles. Preserve bindings when correcting slopes.

## Verification

Apply the [common quality check](index.md#quality-check) using `state` for frame membership and arrow bindings and `preview` for rendered appearance, including accidental slopes after layout changes. Structure checks and image inspection complement each other; neither alone establishes both correctness and readability.
