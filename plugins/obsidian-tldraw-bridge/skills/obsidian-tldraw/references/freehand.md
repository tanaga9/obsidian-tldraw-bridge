# Direct freehand drawing

For authored line art, use `freehand` to turn curves into editable draw shapes. No image generation or tracing is needed. The command compiles to the existing synchronous `script` operation, keeping revision checks, rollback, persistence, and request receipts.

Input example (the named frame must already exist):

```json
{"strokes": [
  {"id": "shape:curve-a", "part": "detail", "parentId": "shape:study",
   "path": "M 100 160 Q 125 140 150 160", "scale": 0.7},
  {"id": "shape:paint-a", "part": "lighting", "parentId": "shape:study",
   "path": "M 90 180 Q 125 130 160 180 Z", "color": "light-blue",
   "fill": "fill", "opacity": 0.4}
]}
```

Paths support explicit absolute `M`, `L`, `Q`, `C`, and final `Z` commands. Use one initial `M` per stroke; use separate IDs for pen lifts. Coordinates are local to the parent. Optional `x` and `y` offset the path. The compiler normalizes local points and handles SDK point encoding.

Each ID creates a stroke or redraws an existing draw shape on the current page. Other strokes are untouched. Redraws apply a complete geometry/style definition: omitted styles revert to defaults (`color: black`, `size: s`, `scale: 1`, `pressure: 0.5`, `taper: 0.15`, `fill: none`, `opacity: 1`). An omitted parent or part preserves the existing value. Parts are labels stored in `meta.bridgeFreehand.part`, not new tldraw shape types or groups. Non-draw ID collisions and parents on other pages are rejected. Use `batch` to delete strokes or edit styles alone.

Closed paths ending in `Z` can be painted in the same edit: `fill: fill` uses the full stroke color, while `fill: solid` uses the pale interior color. Other supported fill styles are `none`, `semi`, `pattern`, and `lined-fill`. `opacity` (0–1) affects the entire stroke, including its fill. Filled open paths are rejected before connecting. Create background regions first, then foreground regions and detail strokes, so later strokes paint over earlier ones. Do not redraw a stroke without its fill/opacity when those styles should be retained.

Use `scale` for line width, `pressure` (0–1) for pen pressure, and `taper` (0–1) for endpoint pressure reduction. Root-level `spacing` controls curve sampling (default 2). Keep edits in small passes; oversized inputs fail before connecting and should be split. After a human moves a stroke, read state and account for its new local position before redrawing it.

Examples use macOS `python3`; follow `SKILL.md` for interpreter selection in
other environments. Choose an existing local output directory for previews;
relative output paths below resolve against the process working directory.

```sh
python3 "<skill-directory>/scripts/bridge.py" --vault <vault> --request-id stroke-pass-1 freehand study.md --revision <revision> --input strokes.json
python3 "<skill-directory>/scripts/bridge.py" --vault <vault> preview study.md --part detail --scale 3 --output detail.png
python3 "<skill-directory>/scripts/bridge.py" --vault <vault> preview study.md --ids shape:curve-a --scale 4 --output stroke.png
python3 "<skill-directory>/scripts/bridge.py" --vault <vault> preview study.md --bounds 80 100 180 160 --scale 3 --output context.png
```

Start with the overall structure, inspect the whole drawing, then refine one part at a time. Keep stable IDs across redraws and tag related strokes with a part. Inspect the relevant detail after changing it and the whole drawing after changing its layout. Do not automatically replace a request for directly authored strokes with image generation or contour extraction.

Preview selectors (`--part` or `--ids`) export only matching current-page shapes, fitted to their bounds; `--scale` is greater than 0 and at most 4. Unselected surroundings are omitted. Use the whole-page preview when checking overlap with other parts. These options do not change the GUI camera or document records.

For a detail in context (such as eyes beneath bangs), use `--bounds X Y W H`: it crops the full current page to that rectangle in page coordinates, retaining surrounding shapes, backgrounds, and occlusion. Width and height must be positive. Bounds cannot be combined with `--part` or `--ids`. Use a specific part label such as `face` only for that region; tagging distant details with the same label expands a part preview to include them.
