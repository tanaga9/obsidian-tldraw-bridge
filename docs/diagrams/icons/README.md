# Architecture diagram icons

The diagram uses original generated icons for all components. All icons are
embedded in the editable [tldraw note](../architecture.md). The README displays a
flattened [WebP preview](../architecture.webp). Separate icon files are not
committed; extract the embedded images from the note when needed for reuse.
This directory retains source and usage notes and generation prompts.

## References and usage notes

Reviewed on 2026-10-19 for identifying components in this project's README
architecture diagram; this is not a general redistribution license for the marks.

| Component | Decision | Source and conditions |
| --- | --- | --- |
| Python | Use a generated illustration of interlocking blue and yellow snakes. | [Official logo page](https://www.python.org/community/logos/), [original PNG](https://s3.dualstack.us-east-2.amazonaws.com/pythondotorg-assets/media/community/logos/python-logo-only.png), [PSF Trademark Usage Policy](https://www.python.org/psf/trademarks/). The policy expressly permits identifying software implemented in Python using its name or unaltered logos. That permission is not a blanket license for generated or modified logos. |
| Obsidian | Use a generated purple flaked shard cutout, enlarged and centered on transparency without a dark tile. | [Brand guidelines](https://obsidian.md/brand) require contacting Obsidian for commercial use of its assets. No permission covering commercial reuse of this project's diagram was established. |
| Codex | Use a generated blue-violet cloud and white terminal prompt cutout, enlarged and centered on transparency without an outer tile. | [OpenAI design guidelines](https://openai.com/brand/) govern marks and prohibit misleading affiliation. A Codex-specific icon distribution and reuse permission for this diagram was not established; the illustration is not an official Codex logo. |

Python and the Python logos are trademarks or registered trademarks of the Python
Software Foundation. The generated Python illustration identifies the implementation language and does
not imply PSF sponsorship or endorsement. The PSF policy's CC0 notice applies to the policy
text, not to the Python logo.

All seven icons were generated with the built-in image generation tool. For compact
embedding, they are resized to 128 pixels and encoded as WebP at quality 0.9,
preserving transparency and their display dimensions (36–48 pixels). Obsidian, Codex and Python illustrations use official icons as visual references,
not as distributed diagram assets.
Generation does not itself grant rights to the referenced trademarks. Reference
context: [Obsidian icon design](https://obsidian.md/blog/new-obsidian-icon/) and
[Codex app icon](https://help.openai.com/en/articles/20001276-moving-to-the-new-chatgpt-desktop-app).

## Prompt set

### obsidian

Edit the attached generated Obsidian-inspired diagram icon. Remove the entire black/charcoal rounded-square tile and all dark background pixels. Keep only the central purple flaked stone/shard, preserving its recognizable asymmetric silhouette, curved facets, pale lavender upper-left face, and rich violet lower faces. Enlarge and center the complete stone so it fills about 88 percent of the square canvas height, with a small clear margin on every side. Show the whole stone without clipping any tip or edge. Use a genuinely transparent alpha background everywhere outside the stone. Clean smooth edges, no black border or outline, no square tile, no drop shadow, no halo, no text or watermark. The final deliverable is a single large purple stone cutout on transparency, in the same illustration style as the input.

### tldraw

Use case: productivity-visual. Asset type: standalone architecture diagram icon. Subject: A small white drawing board with a dark rounded outline, a purple circle and blue square connected by a short line, and a violet pencil crossing its lower right corner; communicates tldraw visual diagram editing. Style: crisp minimal flat illustration, bold smooth dark-indigo outline, violet/blue accents, large clear forms readable at 40 pixels, no texture, no shadows. Composition: one centered icon occupying 85 percent of a square canvas. Background: actual transparent alpha. No lettering, captions, watermark or decorative background. Original generated artwork; no downloaded images.

### agent

Edit the attached generated Codex-inspired diagram icon. Remove the entire outer white/gray rounded-square app tile, every border, fringe, shadow and background surrounding the central object. Keep ONLY the blue-to-violet six-lobed rounded cloud/flower and its white terminal chevron and underscore >_ inside it. Preserve the recognizable six-lobed silhouette, gentle blue/periwinkle gradient, and thick white terminal strokes. Enlarge and center the complete cloud so it fills about 88 percent of the square canvas, leaving a small clear margin on every side. Show the entire cloud without cropping any lobe. Outside the cloud use genuinely transparent alpha, not white or black. The white >_ stays opaque inside the blue cloud. Smooth crisp antialiased contour, no surrounding tile, no black frame, no outline, no shadow, no halo, no stray pixels or watermark. Single large cloud-and-terminal cutout on transparency.

### cli

Use case: productivity-visual. Asset type: standalone architecture diagram icon. Subject: A rounded dark indigo terminal window, with a clearly visible pale cyan greater-than prompt and short white underscore, a slim violet top bar. Style: crisp minimal flat illustration, bold smooth dark-indigo outline, violet/blue accents, large clear forms readable at 40 pixels, no texture, no shadows. Composition: one centered icon occupying 85 percent of a square canvas. Background: actual transparent alpha. No lettering, captions, watermark or decorative background. Original generated artwork; no downloaded images.

### python

Create an original Python-inspired icon for an architecture diagram, using the attached official Python logo only as a visual reference. Preserve the recognizable idea of two interlocking rounded snake forms, blue upper-left and golden-yellow lower-right, each with a small round eye. Redraw with slightly fuller rounded proportions, a thin dark-blue outline and subtle blue/yellow highlights so this is a distinct illustration rather than the original asset. No square app tile. No floating shadow under the snakes. Crisp simple shapes readable at 40 pixels. Square composition, centered interlocking snakes occupying about 88 percent of the canvas. Background must be genuinely transparent alpha; no text, wordmark, trademark symbols, watermark or stray marks. Match the clean illustration style used in technical diagrams.

### document

Use case: productivity-visual. Asset type: standalone architecture diagram icon. Subject: A white document page with a folded upper-right corner, dark indigo outline, three short violet horizontal lines, and a small green save checkmark at its lower right. Style: crisp minimal flat illustration, bold smooth dark-indigo outline, violet/blue accents, large clear forms readable at 40 pixels, no texture, no shadows. Composition: one centered icon occupying 85 percent of a square canvas. Background: actual transparent alpha. No lettering, captions, watermark or decorative background. Original generated artwork; no downloaded images.

### editor

Use case: productivity-visual. Generate a standalone icon for a Dedicated Editor component in a software architecture diagram. Subject: a compact rounded drawing-canvas window with a thin violet top bar, a small blue outlined rectangle and two connected nodes inside, and a clearly recognizable small violet gear overlapping the bottom-right corner. The canvas represents a dedicated offscreen editing environment and the gear represents programmatic editing. It must be visibly different from a drawing board with a pencil: no pencil, no brush, no robot, no text, no letters. Style: clean minimal flat illustration, bold smooth dark-indigo outlines, white canvas interior, blue and violet accents, large simple forms legible at 40 pixels, no texture and no shadows. Square composition, centered icon filling 88 percent of the image. Fully transparent alpha background outside the icon. No watermark or decorative elements.
