from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
class PackageTest(unittest.TestCase):
    def test_standalone_plugin(self):
        package=ROOT/"plugins/obsidian-tldraw-bridge"
        self.assertEqual(json.loads((package/"plugin.json").read_text())["name"],"obsidian-tldraw-bridge")
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/"plugin"
            shutil.copytree(package,target)
            cli=target/"skills/obsidian-tldraw/scripts/bridge.py"
            proc=subprocess.run([sys.executable,str(cli),"--help"],capture_output=True,text=True,cwd=tmp)
            self.assertEqual(proc.returncode,0,proc.stderr)
            self.assertIn("--vault",proc.stdout)

    def test_skill_metadata_and_references(self):
        skill=ROOT/"integrations/codex/skills/obsidian-tldraw"
        text=(skill/"SKILL.md").read_text()
        self.assertTrue(text.startswith("---\n"))
        metadata=text.split("---",2)[1]
        self.assertIn("name: obsidian-tldraw",metadata)
        self.assertIn("description:",metadata)
        self.assertTrue((skill/"references/operations.md").is_file())
        marketplace=json.loads((ROOT/".agents/plugins/marketplace.json").read_text())
        for entry in marketplace["plugins"]:
            self.assertTrue((ROOT/entry["source"]["path"]/"plugin.json").is_file())
