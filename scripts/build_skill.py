#!/usr/bin/env python3
"""Build a portable Skill; no installation or account changes."""
from pathlib import Path
import shutil
root = Path(__file__).resolve().parents[1]
out = root / "dist" / "obsidian-tldraw"
if out.exists():
    shutil.rmtree(out)
shutil.copytree(root / "integrations/codex/skills/obsidian-tldraw", out)
scripts = out / "scripts"
scripts.mkdir()
shutil.copy(root / "bridge.py", scripts / "bridge.py")
shutil.copytree(root / "src", scripts / "src", ignore=shutil.ignore_patterns("__pycache__"))
print(out)
