#!/usr/bin/env python3
"""Dependency-free checkout entry point."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from obsidian_tldraw_bridge.cli import main
raise SystemExit(main())
