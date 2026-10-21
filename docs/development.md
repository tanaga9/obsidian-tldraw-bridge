# Development and distribution

These steps are for maintainers. Plugin users do not need to run them.
macOS is the primary development target; examples use `python3` from the selected
Python environment, or its absolute interpreter path when needed. On Windows,
use PowerShell and substitute a verified Python 3.9.6+ command such
as `python` or `py -3`.

## Compatibility policy

The bridge has no backward-compatibility guarantee. CLI commands and arguments, Python/JavaScript and transport APIs, JSON input/output formats, and CI workflows (including job names, test commands, and matrices) may change without prior notice or a deprecation period. Contributors and agents may make breaking changes within the requested task's scope without asking for separate compatibility approval. Legacy aliases, compatibility adapters, dual formats, and migration periods are not required solely to preserve historical callers unless explicitly requested.

Update affected in-repository callers, tests, documentation, Skills, and generated packages together to describe and verify the new behavior. Use current interfaces rather than assuming older examples remain valid. This policy concerns compatibility across versions; it does not waive document preservation, revision checks, persistence verification, or other correctness requirements of the current implementation.

## Python compatibility and dependencies

The minimum supported Python version is 3.9.6. The current policy is to use only the Python standard library for the bridge runtime, so normal plugin use requires no additional Python packages. Build dependencies declared in `pyproject.toml` apply to optional package installation, not running the bundled CLI.

This policy can be revisited as requirements evolve. Evaluate additional Python packages or a higher minimum version case by case, considering their benefit, compatibility, and user setup cost.

## Build the plugin package

```sh
python3 scripts/build_plugin.py
python3 scripts/build_plugin.py --check
```

The canonical sources are `src/` and `integrations/codex/skills/obsidian-tldraw/`. The generated package at `plugins/obsidian-tldraw-bridge/` is included in the repository and referenced by the marketplace. Regenerate it after changing the canonical sources; `--check` detects stale bundled files. Both package builders exclude `.DS_Store` recursively, and the plugin consistency check ignores it in existing output directories. Source metadata files are left untouched. Git checks text files out with LF line endings on all operating systems (`.gitattributes`); the generated JSON manifest is UTF-8 with LF as well. Keep canonical sources and bundled copies under that policy so a clean checkout passes `--check` on every CI OS.

The plugin display name is **Obsidian Tldraw Bridge**, defined in `scripts/build_plugin.py` under `extensions.com.openai.interface.displayName`. The stable plugin identifier and package directory remain `obsidian-tldraw-bridge`. The marketplace title is set separately in `.agents/plugins/marketplace.json`.

## README architecture diagram

The README uses [architecture.webp](diagrams/architecture.webp), rendered from the
editable Obsidian tldraw note [architecture.md](diagrams/architecture.md). Open the
note in Obsidian with the tldraw plugin, edit the diagram, and render the named
`README architecture` frame directly to WebP with a light background:

```sh
python3 bridge.py --vault obsidian-tldraw-bridge open docs/diagrams/architecture.md
python3 bridge.py --vault obsidian-tldraw-bridge preview docs/diagrams/architecture.md --ids shape:readme-architecture --format webp --quality 0.9 --scale 0.8 --output docs/diagrams/architecture.webp
python3 bridge.py --vault obsidian-tldraw-bridge close docs/diagrams/architecture.md
```

The SDK raster pixel ratio is 2. For this 1200-pixel-wide frame, scale 0.8
produces a 1920-pixel-wide WebP. Substitute the registered vault containing your
checkout. No intermediate PNG or external image converter is required.
Commit the note and WebP together.
Verify the rendered image for clipping and readable labels at README width.
The WebP is a flattened preview; the note remains the editable source.

Generated icons are embedded in the note as 128-pixel transparent
WebP images (quality 0.9); do not commit separate image copies. Source and usage notes and generation prompts are kept in
[diagrams/icons](diagrams/icons/README.md). Extract embedded images from the note
when needed for reuse, and update the note and rendered WebP together when replacing icons.

## Maintaining diagramming guidance

Keep diagramming guidance inside the canonical Skill's [references](../integrations/codex/skills/obsidian-tldraw/references/diagramming/index.md) so both builds remain self-contained.

- Assume the agent knows familiar diagram types; name them and their purpose rather than writing tutorials.
- Add knowledge that changes decisions: project preferences, unfamiliar notation, or demonstrated implementation pitfalls. State when it applies and any useful exception; include evidence or a compact example when needed.
- Keep drawing conventions in `diagramming/index.md`, SDK details in `diagramming/tldraw.md`, and operation contracts in `operations.md`. Split a reference only when its size or independent use justifies it.
- Update existing guidance before adding new rules. Keep history in Git rather than cumulative activity logs.

After knowledge-only changes, rebuild the plugin, run `python3 scripts/build_plugin.py --check`, and run `python3 -m unittest discover -s tests -p 'test_package.py'`. Package tests check that local Markdown references are self-contained and reachable from `SKILL.md`. These checks do not establish drawing quality; live tests are needed for runtime changes.

Local notes and demo files go in `workspace/` (drawings in `workspace/drawings/`).
Both `/workspace/` and local Obsidian settings in `/.obsidian/` are ignored by Git.

## Local distribution testing

For local distribution testing, register the repository's marketplace:

```sh
codex plugin marketplace add /absolute/path/to/obsidian-tldraw-bridge
```

This is a developer workflow. The package layout follows the [official OpenAI plugin documentation](https://developers.openai.com/plugins/build/plugins).

## Build the standalone Skill

```sh
python3 scripts/build_skill.py
```

`dist/obsidian-tldraw/` is a portable Skill for testing or standalone distribution. Normal plugin use relies on the bundled Skill and does not require copying it manually.

See [Known limitations](known-limitations.md) for accepted outstanding work. Python is an environment prerequisite; it is neither bundled nor installed automatically.

For automated checks and Obsidian integration tests, see [Testing](testing.md).
