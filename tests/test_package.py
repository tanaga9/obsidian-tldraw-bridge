from pathlib import Path
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import unquote, urlsplit

ROOT=Path(__file__).resolve().parents[1]
class PackageTest(unittest.TestCase):
    def test_standalone_plugin(self):
        package=ROOT/"plugins/obsidian-tldraw-bridge"
        self.assertEqual(json.loads((package/"plugin.json").read_text(encoding="utf-8"))["name"],"obsidian-tldraw-bridge")
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/"plugin"
            shutil.copytree(package,target)
            cli=target/"skills/obsidian-tldraw/scripts/bridge.py"
            proc=subprocess.run([sys.executable,str(cli),"--help"],capture_output=True,text=True,cwd=tmp)
            self.assertEqual(proc.returncode,0,proc.stderr)
            self.assertIn("--vault",proc.stdout)

    def test_skill_metadata_and_references(self):
        skill=ROOT/"integrations/codex/skills/obsidian-tldraw"
        text=(skill/"SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        metadata=text.split("---",2)[1]
        self.assertIn("name: obsidian-tldraw",metadata)
        self.assertIn("description:",metadata)
        self.assertTrue((skill/"references/operations.md").is_file())
        marketplace=json.loads((ROOT/".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
        for entry in marketplace["plugins"]:
            self.assertTrue((ROOT/entry["source"]["path"]/"plugin.json").is_file())

    def test_skill_local_references_resolve_in_both_distributions(self):
        # Walk from the actual entrypoint, checking transitive references after
        # copying each distribution out of the checkout. Repository-only links
        # must not accidentally make an installed Skill appear self-contained.
        source=ROOT/"integrations/codex/skills/obsidian-tldraw"
        plugin=ROOT/"plugins/obsidian-tldraw-bridge/skills/obsidian-tldraw"
        for origin in (source, plugin):
            with self.subTest(origin=origin), tempfile.TemporaryDirectory() as tmp:
                skill=Path(tmp)/"skill"
                shutil.copytree(origin, skill)
                pending=[skill/"SKILL.md"]
                visited=set()
                while pending:
                    document=pending.pop()
                    if document in visited:
                        continue
                    visited.add(document)
                    # References use inline Markdown links; skip code examples.
                    content=re.sub(r"```.*?```", "", document.read_text(encoding="utf-8"), flags=re.S)
                    for target in re.findall(r"(?<!!)\[[^\]]+\]\(([^\s)]+)\)", content):
                        url=urlsplit(target)
                        if url.scheme or url.netloc or not url.path:
                            continue
                        linked=(document.parent/unquote(url.path)).resolve()
                        self.assertIn(skill.resolve(), linked.parents,
                                      f"Reference escapes Skill: {document}: {target}")
                        self.assertTrue(linked.is_file(),
                                        f"Missing reference: {document}: {target}")
                        if linked.suffix == ".md":
                            pending.append(linked)
                documents={p.resolve() for p in (skill/"references").rglob("*.md")}
                self.assertFalse(documents-visited,
                                 f"References unreachable from SKILL.md: {documents-visited}")

class BuildMetadataTest(unittest.TestCase):
    def prepare_fixture(self, root):
        for directory in ('scripts', 'src/runtime', 'integrations/codex/skills/obsidian-tldraw/references'):
            (root/directory).mkdir(parents=True, exist_ok=True)
        for script in ('build_plugin.py', 'build_skill.py'):
            shutil.copy(ROOT/'scripts'/script, root/'scripts'/script)
        (root/'bridge.py').write_text('# Example CLI\n')
        (root/'src/runtime/bridge.cjs').write_text('// Example runtime\n')
        skill=root/'integrations/codex/skills/obsidian-tldraw'
        (skill/'SKILL.md').write_text('# Example skill\n')
        (skill/'references/operations.md').write_text('# Example operations\n')
        for directory in (root/'src', root/'src/runtime', skill, skill/'references'):
            (directory/'.DS_Store').write_bytes(b'source metadata')

    def run_builder(self, root, script, *args):
        return subprocess.run([sys.executable, str(root/'scripts'/script), *args],
                              capture_output=True, text=True, cwd=root)

    def test_plugin_build_and_check_ignore_metadata_but_detect_source_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            self.prepare_fixture(root)
            built=self.run_builder(root, 'build_plugin.py')
            self.assertEqual(built.returncode, 0, built.stderr)
            package=root/'plugins/obsidian-tldraw-bridge'
            self.assertEqual(list(package.rglob('.DS_Store')), [])
            for directory in (package, package/'skills/obsidian-tldraw/scripts/src/runtime'):
                (directory/'.DS_Store').write_bytes(b'different output metadata')
            checked=self.run_builder(root, 'build_plugin.py', '--check')
            self.assertEqual(checked.returncode, 0, checked.stderr)
            self.assertEqual((root/'src/.DS_Store').read_bytes(), b'source metadata')
            (root/'src/runtime/bridge.cjs').write_text('// Updated runtime\n')
            stale=self.run_builder(root, 'build_plugin.py', '--check')
            self.assertNotEqual(stale.returncode, 0)
            self.assertIn('Plugin package is stale', stale.stderr)

    def test_standalone_skill_build_excludes_metadata_recursively(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            self.prepare_fixture(root)
            built=self.run_builder(root, 'build_skill.py')
            self.assertEqual(built.returncode, 0, built.stderr)
            skill=root/'dist/obsidian-tldraw'
            self.assertEqual(list(skill.rglob('.DS_Store')), [])
            self.assertTrue((skill/'SKILL.md').is_file())
            self.assertTrue((skill/'scripts/src/runtime/bridge.cjs').is_file())
            self.assertEqual((root/'src/.DS_Store').read_bytes(), b'source metadata')
