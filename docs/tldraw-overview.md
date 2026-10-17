# tldraw overview: apps, file formats, related tools, and AI agent editing

Reviewed: 2026-10-17. Products, APIs, AI integrations, and terms of use change. Check official sources periodically and update this document accordingly.

This introduction explains tldraw terminology and helps you choose tools, storage options, and AI editing methods. Product and format descriptions draw on official sources; comparisons of use cases are an interpretation of those sources. Features vary by version and plan.

**tldraw is a family of infinite-canvas technologies and products built around editable shapes.** You arrange shapes, text, and freehand strokes in a large space and navigate by panning and zooming. Distinguish three layers:

| Layer | What it determines | Examples |
| --- | --- | --- |
| **Apps and SDK** | Where you draw and what you can do | tldraw.com, offline, the Obsidian plugin, the development SDK |
| **File formats** | What you save and exchange | `.tldr`, `.tldraw`, drawing Markdown, PNG |
| **Editing and execution environment** | How people and AI read, modify, and run canvas content | Shape APIs, agent integrations, shared canvases, custom behavior |

For AI use, file formats are only part of the picture. **Can the agent read and edit a live canvas and use it in a conversation?** This capability is not exclusive to tldraw, and its scope depends on the app and integration.

Reading order: [Apps and SDK](#understanding-the-tldraw-names) → [File formats](#file-formats-and-data) → [Related tools](#comparing-related-tools) → [AI editing](#editing-with-ai-agents) → [Related concepts](#related-concepts)

## Understanding the tldraw names

| Name | What it is | Main role |
| --- | --- | --- |
| **tldraw SDK** | A development library for embedding a canvas in React apps | Provides the drawing UI, shape editing, Editor API, data management, and extensions for custom shapes and tools |
| **tldraw.com** | A browser-based whiteboard app | A place to draw immediately, share boards, and collaborate |
| **tldraw offline** | A desktop app centered on local files | Supports local drawing and storage, agent integrations, and document scripts |
| **Obsidian tldraw plugin** | A plugin for using tldraw inside Obsidian | Stores drawings as notes in a vault, connecting them with links, tags, and prose |

The SDK supplies building blocks; apps and plugins turn those blocks into products. Even products using the same SDK family can differ in version, storage, sharing, external control, and extensions. [SDK](https://tldraw.dev/), [tldraw.com](https://www.tldraw.com/), [offline](https://github.com/tldraw/tldraw-offline), [Obsidian plugin](https://github.com/tldraw/obsidian-plugin)

## File formats and data

| Format | Contents and purpose | Considerations |
| --- | --- | --- |
| **`.tldr`** | The JSON format used for file import and export in the tldraw SDK; contains a format version, schema, and records such as shapes | Still used by the SDK. offline supports it as a legacy import/export format |
| **`.tldraw`** | The native tldraw offline format; packages the canvas, pages, stored media, and document scripts | Distinct from `.tldr`. Opening a `.tldr` in offline imports it into a new, unsaved document |
| **Drawing Markdown, such as `drawing.tldr.md`** | A Markdown note containing drawing data embedded as JSON by the Obsidian plugin | Its actual extension is `.md`. A filename containing `.tldr` does not make it a standalone `.tldr` JSON file |

Renaming an extension does not convert a file. Use the relevant app or SDK's import/export functions. [SDK file definition](https://github.com/tldraw/tldraw/blob/main/packages/tldraw/src/lib/utils/tldr/file.ts), [offline file formats](https://github.com/tldraw/tldraw-offline#local-files), [Obsidian plugin storage](https://github.com/tldraw/obsidian-plugin#tldraw-in-obsidian-plugin)

### Saving, synchronization, and backup

- **Saving** preserves state, **synchronization** keeps state consistent across devices or users, and **backup** preserves earlier states for recovery. Autosave or synchronization alone does not guarantee recovery from accidental deletion.
- Shared cloud boards, browser storage, and local files have different storage locations. Apps built with the SDK also choose where to persist their data. [SDK persistence](https://tldraw.dev/docs/persistence)
- File synchronization is different from collaboration between running Editors. Check how external changes are handled before modifying files directly. offline does not automatically merge external changes to an open file. [offline limitations](https://github.com/tldraw/tldraw-offline#local-files)

### Moving content between tools

Decide what must survive: **appearance, editable elements, structure such as connections, or executable behavior**. Outputs for viewing and distribution, such as PNG, SVG, and PDF, serve a different purpose from native editing data. Even SVG may not preserve original shape IDs or connections. Conversely, tools such as draw.io can embed editing data inside images. [draw.io export formats](https://www.drawio.com/docs/manual/export/export-diagram/)

tldraw has a [proposal](https://github.com/tldraw/tldraw/issues/1666) for embedding editing data in images and an [implementation PR, #4981](https://github.com/tldraw/tldraw/pull/4981), intended to allow re-editing from PNG/SVG files. That PR was closed without merging; this could not be confirmed as a standard feature as of the review date. Embedding fonts and media in official image exports makes the output self-contained for display; it is different from preserving editing data. [Image export](https://tldraw.dev/sdk-features/image-export)

Even when the same shape data is transferred, schema versions, custom shape implementations, fonts, and the contents or locations of image/video assets can affect rendering and editability. A data file does not necessarily include all required assets or implementation code. Open the result in the destination environment to verify it. [SDK assets](https://tldraw.dev/docs/assets), [Stored data migrations](https://tldraw.dev/docs/persistence)

## Comparing related tools

### Shared canvases, sketching, and notes

**For people and AI thinking and editing in the same space, canvas products such as Miro are direct comparisons.** Compare equivalent layers: hosted services, local apps, and embeddable libraries serve different roles.

| Tool | Closest tldraw comparison | What to compare |
| --- | --- | --- |
| **[Miro](https://developers.miro.com/docs/introduction)** | tldraw.com | Team board workflows, extensions within boards, and integrations with external systems and AI |
| **[FigJam](https://help.figma.com/hc/en-us/articles/1500004362321-Guide-to-FigJam)** | tldraw.com | Collaborative brainstorming and organization, and connections to Figma design work |
| **[Excalidraw](https://github.com/excalidraw/excalidraw)** | tldraw.com/offline; tldraw SDK when comparing libraries | Hand-drawn diagrams, saving and sharing, and embedding a canvas in an app. Distinguish the web app's features from the library's |
| **[Obsidian Canvas](https://obsidian.md/canvas)** | Obsidian tldraw plugin | Arranging existing notes, cards, and media in space versus drawing shapes and freehand curves |
| **[AFFiNE](https://affine.pro/blog/how-affine-classifies-editors)** | An environment combining notes and tldraw | An editing model that uses the same blocks in prose pages and freely arranged canvases |

Obsidian Canvas is a built-in Obsidian feature, separate from the tldraw plugin. It uses `.canvas` files (JSON Canvas), not tldraw drawing Markdown or `.tldr`. Excalidraw also has its own `.excalidraw` JSON format. A published file format does not guarantee conversion between tools or safe direct writes to a document being edited. [Obsidian Canvas format](https://obsidian.md/help/plugins/canvas), [Excalidraw formats and features](https://github.com/excalidraw/excalidraw#features)

For AI editing, compare **the context an agent can read, elements it can edit, storage location, and collaboration with people**, rather than product names or the presence of built-in AI. Miro, for example, offers MCP, a REST API, and a Web SDK, but their roles and operation coverage differ. For each product, check the document types and features supported by the specific API or integration. [Miro integration comparison](https://developers.miro.com/docs/mcp-server-vs-rest-api)

For development, distinguish **embedding a canvas in your own app** with the tldraw SDK or Excalidraw library from **adding features inside an existing service's boards** with the Miro Web SDK. Both allow extensions, but app ownership and distribution, data management, runtime, and terms of use differ.

These are representative comparisons. Start with Miro/FigJam for collaboration, Excalidraw for sketching, and Obsidian Canvas/AFFiNE for arranging notes in space. Consider compatibility with existing notes and team workflows. The following comparisons with draw.io, text notation, and slides concern **the working method itself**.

### diagrams.net/draw.io, Mermaid, and PlantUML

A major distinction is **placing shapes directly versus describing relationships in text to generate a diagram**.

| Tool | Basic editing method | Suitable uses | Considerations |
| --- | --- | --- | --- |
| **tldraw family** | Directly edit shapes and strokes on an infinite canvas; also controllable through code | Freeform explanatory diagrams, brainstorming, hand-drawn illustrations, and mixed images and text | Strict notation requires rules maintained by users or additional tools |
| **diagrams.net/draw.io** | Edit diagrams using shape libraries and connectors | Flowcharts, networks, and architecture diagrams with organized shapes and connections | Check whether the intended notation and connections can be represented |
| **Mermaid** | Describe nodes and relationships in a dedicated text notation and render them | Flowcharts, sequence and state diagrams in documents; diagrams managed in Git | Direct control over individual positions and freehand curves is limited |
| **PlantUML** | Generate diagrams from a dedicated text notation | UML and software design documentation; also supports non-UML diagrams | Focuses on supported notation rather than freeform layouts or illustration |

diagrams.net and draw.io are names for the same tool family. `.drawio` is an XML-based editing format. Mermaid/PlantUML generally use text as the source of truth and regenerate the diagram. [draw.io format](https://www.drawio.com/docs/manual/export/export-to-xml/), [Mermaid](https://mermaid.js.org/intro/), [PlantUML](https://plantuml.com/)

Agents can modify Mermaid/PlantUML definitions and re-render them, making relationship changes and diff reviews convenient. However, even a small text change may alter automatic layout. Shape data and APIs suit individual position, color, or text changes that should preserve a person's layout. Neither approach automatically guarantees a diagram's semantic correctness.

For draw.io, agents can generate or modify XML to create editable shapes and connections, or use integration tools. Validate shape IDs, connection targets, coordinates, and the rendered result as well as XML syntax. [AI diagram generation and validation](https://www.drawio.com/docs/reference/diagram-generation/)

Use cases overlap. Generating a diagram from text does not necessarily enable round-trip editing with the original text. When re-editing a converted diagram, decide which representation is the source of truth.

### PowerPoint and Google Slides

| Aspect | tldraw family | PowerPoint/Google Slides |
| --- | --- | --- |
| Basic unit | A large canvas with spatially arranged diagrams, annotations, and reference material | A sequence of slides with defined dimensions |
| Main purpose | Explore, organize relationships, and explain while drawing | Present and distribute information in a chosen order |
| Presentation structure | Zooming and frames define the visible area | Slide layouts, themes, and transitions organize content |
| Editability | Preserved as tldraw shapes and strokes | Preserved as slide text and shapes; a pasted PNG remains a single image |
| Example workflow | Brainstorming and drafting diagrams | Refining content into a focused presentation |
| Agent editing | Modify shapes through APIs or integrations exposed by the environment | Generate/edit PPTX files or use supported PowerPoint APIs; use authenticated Slides APIs for Google Slides |

Both slide products also offer shape editing and collaboration. Think in terms of **an infinite canvas versus an ordered slide sequence**, rather than the mere presence of individual features. Google Slides centers on browser collaboration and supports importing and directly editing PowerPoint files. However, being able to open a file does not guarantee a lossless round trip for formatting, fonts, or behavior. [PowerPoint help](https://support.microsoft.com/en-us/powerpoint/), [Google Slides](https://workspace.google.com/products/slides/)

PowerPoint's shape API supports creation, movement, and formatting; Google Slides' `batchUpdate` groups multiple changes. Agent capabilities depend on the connection method, supported API environment, and document access. Pasting a diagram as an image and creating it as text and shapes offer different levels of later partial editing. [PowerPoint shape API](https://learn.microsoft.com/en-us/office/dev/add-ins/powerpoint/shapes), [Google Slides batch updates](https://developers.google.com/workspace/slides/api/guides/batch)

## Editing with AI agents

An AI agent uses tools to read a document, make requested changes, and inspect the result. **Built-in AI, external control, and preservation of editable shapes are separate properties.** Reading, creating new content, modifying existing content, and implementing behavior are also distinct capabilities.

### From saved diagrams to interactive and executable canvases

| Use | Agent's role | Examples |
| --- | --- | --- |
| **Diagram as an artifact** | Generate or revise definitions/shapes and inspect the rendering | Create a flowchart or slides |
| **Shared workspace** | Read human edits, selections, and comments; modify part of the existing state | Fix a circled area or add labels while preserving a rearranged layout |
| **Working tool** | Implement and test behavior attached to canvas elements | Interactive prototypes, simulations, or connected AI processing nodes |

Live tldraw integrations can make a diagram **both an input and an output** for an agent. Combining visual layout and appearance with exact text, IDs, and connections from shape data supports requests such as “fix this part.” The official plugin also supplies context such as selections and comments. [SDK AI integration](https://tldraw.dev/docs/ai), [Official plugin](https://tldraw.dev/blog/introducing-tldraw-for-chatgpt-and-codex)

Custom SDK shapes, bindings, and processing logic can turn an explanatory diagram into an interactive tool. offline also supports stored document scripts. However, **connecting shapes with lines does not by itself execute a process**. Execution logic and a compatible host app are required; these capabilities are not universal across tldraw products or `.tldr` files. [SDK workflow examples](https://tldraw.dev/docs/ai), [Extending offline](https://tldraw.dev/blog/building-with-tldraw-offline)

Shared canvases and AI integrations also exist in products such as Miro. Partial editing, collaboration, and extensibility are not unique to tldraw. The distinction is less about having a proprietary format than **how well saved files, live editing state, conversational context, and executable behavior can be handled together**. Distinguish features already built into a product from those that can be implemented with an SDK.

### Ways to edit tldraw from Codex

| Route | Main target | Characteristics |
| --- | --- | --- |
| **Official tldraw plugin for ChatGPT/Codex** | tldraw.com boards | Connect an account and create/edit in a canvas inside chat; supports existing boards, collaboration, and comments |
| **offline Skill and local API** | Open tldraw offline documents | Follow Skill instructions to control the app, edit local drawings, and work with document scripts |
| **Obsidian plugin integrations/extensions** | Drawing notes in a vault | Control the Editor through the available integration; supported shapes, operations, saving, and synchronization vary |
| **Custom SDK integration** | A custom tldraw app | Expose Editor API operations to give an agent the required read/edit capabilities |
| **Third-party Skills, MCP servers, and other tools** | Depends on implementation | Distinguish control of a running app from file generation; verify the provider, target, and capabilities |
| **File generation and import** | Editing data such as `.tldr` | Generate data without connecting to a live canvas; importing, validation, and synchronization with existing edits are separate concerns |
| **Browser/desktop UI automation** | The visible editor | May work without a dedicated API, but depends on UI state and available automation tools |

The official plugin targets tldraw.com boards. Local offline documents and Obsidian drawing notes are different targets. [Official announcement](https://tldraw.dev/blog/introducing-tldraw-for-chatgpt-and-codex)

offline lets agents such as Codex read and edit open documents and create document scripts. [offline integration](https://github.com/tldraw/tldraw-offline#bring-your-own-ai), [SDK AI integration](https://tldraw.dev/docs/ai)

**Plugins, Skills, MCP, and APIs occupy different layers and can be combined.** A plugin adds and distributes capabilities; a Skill supplies operating instructions; MCP is a connection protocol; an API defines specific operations. A plugin can include Skills and an MCP server, and an agent can follow a Skill to call an API. [OpenAI plugins](https://developers.openai.com/plugins), [Skills](https://developers.openai.com/plugins/concepts/skills)

The official SDK migration Skill helps update projects using the SDK. It serves a different purpose from a Skill for editing drawings on a canvas. [SDK migration Skill](https://tldraw.dev/releases/migration-skill)

### AI editing interface standards and reference implementations

As of the review date, **a unified or de facto standard for tldraw AI editing operations across implementations could not be established from the available sources**. Distinguish three layers:

| Layer | Protocol or implementation | Role and scope |
| --- | --- | --- |
| **Connection** | MCP | Defines tool discovery and invocation, input/output schemas, and result exchange; does not define tldraw shape representations or editing commands |
| **Editing implementation** | Official SDK Editor API | Provides the foundation for creating, updating, and deleting shapes; is not a universal external API across apps |
| **AI-facing operations** | Official MCP App and Agent Starter Kit | Reference implementations for exposing operations to agents; not an interoperable editing protocol |

“MCP support” does not guarantee that identical commands work across tools with different names, coordinate systems, supported shapes, or saving behavior. [MCP tool specification](https://modelcontextprotocol.io/specification/2025-06-18/server/tools), [Editor API](https://tldraw.dev/sdk-features/editor), [Official MCP App](https://tldraw.dev/blog/tldraw-mcp-app)

A basic pattern in official implementations is to **read images alongside structured data, then validate concise, typed operations before applying them to the Editor**. The Agent Starter Kit converts model-facing shape representations into native records, validates or corrects IDs and coordinates, and provides higher-level operations such as alignment and distribution. These are design references, not requirements for conformance to a common standard. [Official AI integration guide](https://tldraw.dev/docs/ai), [Agent Starter Kit](https://tldraw.dev/starter-kits/agent)

### Common criteria for choosing an editing method

Whether creating a saved diagram or controlling a live canvas, consider:

1. **What must be preserved?** Text definitions suit managing relationships and explanations; shape data/APIs suit partial edits that preserve layout; image generation/editing suits visual texture and finish.
2. **Can the agent read existing content and target specific parts?** Check whether it can identify documents, pages, and shapes and change only the intended area. UI automation also depends on screen state and zoom.
3. **Can structure, appearance, and behavior be verified?** Beyond valid syntax or successful API calls, check connections, overlaps, clipped text, and arrow directions in previews. For interactive tools, also test operations and processing results.
4. **Are human edits and saved state protected?** Re-read current state to preserve others' changes, and distinguish applying edits from completing saves or exporting images. Check duplicate retries, partial failures, and Undo behavior.

Comparing the complete read–edit–verify–save cycle, rather than generation speed alone, helps assess suitability for continued editing.

### Data access and code execution

Even a locally saved diagram leaves the device if screenshots or shape data are sent to a cloud AI service. **Check storage location separately from AI processing location.** Integrations also depend on document permissions, available operations, plans, and API limits.

Reading/editing a diagram and executing arbitrary code require different permissions. In particular, offline `.tldraw` files can contain document scripts that may run when opened. Distinguish accepting a drawing from executing its embedded behavior. [offline agents and scripts](https://github.com/tldraw/tldraw-offline#bring-your-own-ai)

## Related concepts

- **Infinite canvas, pages, and frames:** The canvas is the placement space, pages divide it into separate workspaces, and frames enclose areas within a canvas. Adding frames does not provide all the features of a slide product.
- **Shapes, connections, and meaning:** A bound connector differs from a line that merely looks like an arrow. Preserving IDs and connections does not necessarily define business meanings such as approval, dependency, or data flow. Specify notation, labels, and data models when precision matters.
- **Git:** Text notation makes semantic changes easier to review. JSON/XML and drawing data embedded in Markdown can also be versioned, but large coordinate or compressed-data diffs can be difficult to read. This is separate from resolving collaborative editing conflicts.
- **CLI and drawing quality:** A CLI is a command-based entry point. Switching between MCP, CLI, or other entry points does not by itself improve drawing quality; available operations, model context, and drawing/verification procedures also matter.
- **Appearance and readability:** Stroke width, colors, highlights, layout, and fonts affect the impression of a drawing. Compare renderers using identical shape data and display conditions. For shared output, consider text size, contrast, distinctions beyond color, and explanatory prose where needed.
- **Pricing, distribution, and terms:** Free app use, published source code, and permission to embed an SDK in a product are different matters. Check the adopted version's terms, including cloud plans and AI usage. [SDK licensing](https://tldraw.dev/community/license)
