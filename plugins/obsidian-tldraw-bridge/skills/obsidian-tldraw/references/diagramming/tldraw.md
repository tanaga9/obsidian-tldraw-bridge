# Obsidian tldraw implementation notes

Use this bridge's Editor API, not another tldraw application's HTTP server or custom helpers. Inspect the installed SDK's records rather than assuming the latest props or text format. See [operations](../operations.md) for supported methods.

## Frames

Use actual frame shapes with descriptive names and make the relevant shapes children of the frame. Visual enclosure by a rectangle or group is insufficient. When reparenting, account for local coordinates and verify page positions. Choose parents for cross-frame arrows according to their relationship and rendering rather than moving every connector into a frame mechanically.

## Connections and rendered dimensions

Keep meaningful arrows bound to their target shapes. Touching a box visually does not establish a binding; inspect endpoint records. Decorative and annotation arrows may be unbound.

A geo shape's effective height can include `growY` after text wrapping. Equal `props.h` values and equal normalized anchors therefore do not guarantee horizontal arrows. Give peer boxes sufficient height for their labels and align their actual centers or attachment points after layout settles. Preserve bindings when correcting slopes.

## Verification

Use `state` to check frame membership and arrow bindings. Inspect `preview` for clipping, overlaps, label wrapping, and accidental slopes after layout changes. Check each edited page. Structure checks and image inspection complement each other; neither alone establishes both correctness and readability.
