# Frame nesting, overlap, and image export

Verified on 2026-10-31 UTC; corrected ancestor-crop check completed at
2026-10-31T16:56:00Z. Environment: Obsidian Desktop 1.14.5 (installer 1.14.4),
Obsidian tldraw plugin 1.32.0, and its embedded tldraw SDK 5.4.0.
Bridge checkout: `92635a8700e1853ed3143b0b2e6ff60c3e718246`.
This is a scoped export study, not a compatibility claim for other versions.

## Method

Created a dedicated note in the repository vault under the ignored
`workspace/drawings/` directory. Used explicit SDK parent IDs and sibling
`index` values, avoiding drag-and-drop parenting ambiguity. Exported actual WebP
images through the bridge's `preview` command, which calls `editor.toImage`.
Inspected images, recorded shape parents, render indices and masks, and verified
saved revisions. Intermediate exports and probe scripts are outside tracked
documentation in `/tmp/frame-export-study/`.

Baseline: outer frame A at (0,0), 600 × 320; inner/view frame B at (180,60),
240 × 200; a single red rectangle at page coordinates (100,90), 300 × 80.
For each of six configurations, exported A alone, B alone, and the full page
cropped to (180,60,240,200): 18 images. This crop matches B for the first five
configurations. The clipping variant moved B to (480,60), so its original crop
covered the old location and did not test the moved B. All six edits had
confirmed persistence.

The corrected check recreated only the clipping variant in a fresh dedicated
note. It obtained B's unmasked page bounds from `editor.getShapePageBounds`
and exported A alone, B alone, and the full page with bounds (480,60,240,200).
All three exports matched the saved revision. Closing and reopening retained
that revision, and another bounds export produced identical WebP bytes.

## Results

| Condition | Observed result |
| --- | --- |
| B is A's child; rectangle belongs directly to A; B is behind the rectangle | A export shows the full rectangle over B. B export is blank: the rectangle is B's sibling, not descendant. |
| Same hierarchy; B is in front of the rectangle | A export shows B's opaque background hiding the overlapping rectangle. B export is still blank. |
| Rectangle belongs to B, which belongs to A | Both exports contain the rectangle, but both clip it to B. A export also retains B's background, border and title; B export omits B's own decoration. |
| A and B are overlapping page siblings; rectangle belongs to A; B is in front | B export is blank. A export contains its rectangle and omits B. Whole-page crop includes B and its background hides the rectangle. |
| Same page siblings; B is behind A | B export remains blank. Whole-page crop shows the rectangle, because the foreground A and its content cover B. |
| B belongs to A but extends 120 units beyond A's right edge; rectangle belongs to B | B alone exports at 120 × 200 logical units. The corrected bounds export is 240 × 200, but its right half has no rectangle content: ancestor clipping persists in both paths. The bounds crop also retains B's visible border; the single-frame export omits it. |

These results distinguish three mechanisms:

1. **Export membership:** a selected frame includes its descendants, not every
   shape overlapping its rectangle. A shape has one parent; overlapping frames
   do not share ownership. Changing sibling order does not change membership.
2. **Clipping:** ordinary descendant geometry is constrained by its clipping
   ancestors, including ancestors outside the export selection. Increasing the
   enclosing frame does not reveal parts clipped by an inner frame. This study
   used rectangles; arrows have a separate clipping exception in the SDK and
   were not experimentally tested here.
3. **Rendering order:** frames have backgrounds, borders and titles. Their
   foreground/background render indices depend on hierarchy as well as sibling
   order. In these tests, moving B in front of a sibling rectangle hid that
   rectangle. Exporting a single frame omits that frame's own decoration, but
   does not omit nested frames' decoration.

## Consequence for a single editable source

Nesting works for genuinely contained subdiagrams when the inner clipping and
the visible inner frame in the overview are intended. It does not automatically
provide independent camera windows onto one unclipped master drawing.

For an overview plus arbitrary detail crops, retain one master drawing and
export page-coordinate bounds. A seventh configuration used one master frame
and one rectangle, without additional view frames. Its whole-frame export
(600 × 320) retained the full rectangle, and a bounds crop (240 × 200) showed
the corresponding portion. Both came from the same saved revision. Closing
and reopening the note preserved that revision and exactly one rectangle.

The bridge's `--bounds` crops the rendered full page, so visible frame
decorations and occlusion remain part of the crop. Avoid placing extra view
frames on the source unless their appearance is intended. Bounds also do not
undo clipping already imposed by existing parents. This study verified SDK
exports through the bridge; it did not exercise Obsidian Markdown embed exports
or manually click the application's export UI.

## Implementation evidence

The locally installed bundle was inspected alongside these official sources:

- [SDK 5.4.0 SVG export implementation](https://github.com/tldraw/tldraw/blob/v5.4.0/packages/editor/src/lib/exports/getSvgJsx.tsx): descendant selection, masked bounds, single-frame omission and sorted render elements.
- [SDK 5.4.0 frame implementation](https://github.com/tldraw/tldraw/blob/v5.4.0/packages/tldraw/src/lib/shapes/frame/FrameShapeUtil.tsx): background, border and title export.
- [Shape clipping documentation](https://tldraw.dev/sdk-features/shape-clipping): clipping ancestry and the arrow exception; current documentation is supplementary to the pinned and locally observed behavior.

## Reproduce the ancestor-clipping check

Use a fresh dedicated test note, never an existing drawing. Create it with
`python3 bridge.py --vault <vault> --request-id <unique-id> create <note.md>`.
Save the following as a temporary JavaScript file and run it with `script`,
passing the created note's returned revision. Positions inside frames are
parent-local; the rectangle's page origin is (500,90).

```js
editor.createShapes([
  {id: 'shape:outer', type: 'frame', parentId: editor.getCurrentPageId(),
   index: 'a1', x: 0, y: 0, props: {w: 600, h: 320, name: 'outer'}},
  {id: 'shape:inner', type: 'frame', parentId: 'shape:outer',
   index: 'a1', x: 480, y: 60, props: {w: 240, h: 200, name: 'inner'}},
  {id: 'shape:source', type: 'geo', parentId: 'shape:inner',
   index: 'a1', x: 20, y: 30,
   props: {w: 200, h: 80, geo: 'rectangle', color: 'red', fill: 'fill', dash: 'solid'}}
]);
const b = editor.getShapePageBounds('shape:inner');
const m = editor.getShapeMaskedPageBounds('shape:inner');
return {bounds: {x: b.x, y: b.y, w: b.w, h: b.h},
        masked: {x: m.x, y: m.y, w: m.w, h: m.h}};
```

The script result should distinguish unmasked `(480,60,240,200)` from masked
`(480,60,120,200)` bounds. Use the script's saved revision for these exports;
substitute the selected vault, note and absolute temporary output directory:

```sh
python3 bridge.py --vault <vault> preview <note.md> --revision <revision> --ids shape:outer --output <output-dir>/outer.webp
python3 bridge.py --vault <vault> preview <note.md> --revision <revision> --ids shape:inner --output <output-dir>/inner.webp
python3 bridge.py --vault <vault> preview <note.md> --revision <revision> --bounds 480 60 240 200 --output <output-dir>/crop.webp
```

Expected logical sizes are 600 × 320, 120 × 200, and 240 × 200 respectively;
the default raster dimensions are twice those values. Inspect the images as
well as dimensions: the rectangle ends at page x=600 in all three. Run `saved`,
`close`, and `open` for the test note, verify the same revision, repeat the bounds
export to another output file, and compare its SHA-256. Close that test session
when finished. The retained dedicated note can be inspected independently.

Runtime implementation was unchanged. The distributed Skill now incorporates
the resulting view-selection guidance; the correction does not change its
recommendation or clipping caveats.
