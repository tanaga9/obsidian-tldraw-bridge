# Development and distribution

These steps are for maintainers. Plugin users do not need to run them.

## Build the plugin package

```sh
python3 scripts/build_plugin.py
python3 scripts/build_plugin.py --check
```

The canonical sources are `src/` and `integrations/codex/skills/obsidian-tldraw/`. The generated package at `plugins/obsidian-tldraw-bridge/` is included in the repository and referenced by the marketplace. Regenerate it after changing the canonical sources; `--check` detects stale bundled files. Both package builders exclude `.DS_Store` recursively, and the plugin consistency check ignores it in existing output directories. Source metadata files are left untouched.

For local distribution testing, register the repository's marketplace:

```sh
codex plugin marketplace add /absolute/path/to/obsidian-tldraw-bridge
```

This is a developer workflow. Public directory publication and installation through the plugin UI remain unverified. The package layout follows the [official OpenAI plugin documentation](https://developers.openai.com/plugins/build/plugins).

## Build the standalone Skill

```sh
python3 scripts/build_skill.py
```

`dist/obsidian-tldraw/` is a portable Skill for testing or standalone distribution. Normal plugin use relies on the bundled Skill and does not require copying it manually.

See [Known limitations](known-limitations.md) for accepted outstanding work. Python is an environment prerequisite; it is neither bundled nor installed automatically.

For automated checks and Obsidian integration tests, see [Testing](testing.md).
