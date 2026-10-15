#!/usr/bin/env python3
"""Build or check the tracked, self-contained marketplace package."""
import argparse
import json
from pathlib import Path
import shutil
import tempfile

root = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser()
p.add_argument("--check", action="store_true", help="Fail if checked-in package is stale")
args = p.parse_args()
manifest = {
    "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
    "name": "obsidian-tldraw-bridge", "version": "0.1.0",
    "description": "Read and edit local Obsidian tldraw diagrams through a CLI and Skill."
}
def files(path):
    return {str(p.relative_to(path)):p.read_bytes() for p in path.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts and ".DS_Store" not in p.parts}
with tempfile.TemporaryDirectory() as tmp:
    package = Path(tmp) / "obsidian-tldraw-bridge"
    skill = package / "skills" / "obsidian-tldraw"
    shutil.copytree(root / "integrations/codex/skills/obsidian-tldraw", skill,
                    ignore=shutil.ignore_patterns("__pycache__", ".DS_Store"))
    scripts = skill / "scripts"
    scripts.mkdir()
    shutil.copy(root / "bridge.py", scripts / "bridge.py")
    shutil.copytree(root / "src", scripts / "src", ignore=shutil.ignore_patterns("__pycache__", ".DS_Store"))
    (package / "plugin.json").write_text(json.dumps(manifest,indent=2)+"\n")
    target = root / "plugins" / "obsidian-tldraw-bridge"
    if args.check:
        if not target.exists() or files(package) != files(target):
            raise SystemExit("Plugin package is stale: run python3 scripts/build_plugin.py")
        print("Plugin package is current")
    else:
        if target.exists():
            shutil.rmtree(target)
        target.parent.mkdir(exist_ok=True)
        shutil.copytree(package,target, ignore=shutil.ignore_patterns(".DS_Store"))
        print(target)
