"""Opt-in integration test against an existing, dedicated probe diagram.
Run: python3 tests/live.py --vault Documents --path 'Codex Bridge Probe 20261014.md'
Adds UUID-named shapes only and removes them in finally; never replaces the file.
"""
import argparse
import json
from pathlib import Path
import sys
import uuid
import tempfile
import shutil
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from obsidian_tldraw_bridge.obsidian import Client,BridgeError
p=argparse.ArgumentParser()
p.add_argument("--vault",required=True)
p.add_argument("--path",required=True)
p.add_argument("--output",default=str(Path(tempfile.gettempdir()) / "obsidian-tldraw-bridge-live.png"))
a=p.parse_args()
c=Client(a.vault)
# A unique module path prevents Obsidian's require cache from testing old code.
runtime_dir=tempfile.TemporaryDirectory(prefix="obsidian-tldraw-live-")
runtime=Path(runtime_dir.name)/"bridge.cjs"
shutil.copy(c.module,runtime)
c.module=str(runtime)
shape="shape:bridge-test-"+uuid.uuid4().hex
args={"path":a.path}
original=c.call("open",args)
def batch(ops,rev=None,identity=None):
    current=c.call("state",args)
    return c.call("batch",args|{"revision":rev or current["revision"],"operations":ops,"full":True},identity)
def op(method,*values): return {"method":method,"args":list(values)}
def assert_restored(expected):
    current=c.call("state",args)
    assert current["revision"]==expected["revision"]
    # Check persistence before any successful edit could conceal a bad rollback.
    assert c.call("saved",args)["saved"]
    main=c.evaluate('JSON.stringify((()=>{const group=app.plugins.getPlugin("tldraw").tlDataDocumentStoreManager.storesManager.storeGroupMap.get('+json.dumps(a.path)+');return Object.values(group.main.store.getStoreSnapshot().store).sort((a,b)=>a.id.localeCompare(b.id))})())')
    assert main==expected["records"], "Shared Store was not restored"

try:
    create=[op("createShapes",[{"id":shape,"type":"geo","x":500,"y":200,"props":{"geo":"rectangle","w":160,"h":100,"color":"blue","font":"sans","richText":{"type":"doc","content":[{"type":"paragraph","content":[{"type":"text","text":"Integration test"}]}]}}}])]
    request="live-create-"+uuid.uuid4().hex
    result=batch(create,original["revision"],request)
    assert result["persistence"]["saved"]
    same=c.call("batch",args|{"revision":original["revision"],"operations":create,"full":True},request)
    assert same["revision"]==result["revision"]
    try:
        batch([op("deleteShapes",[shape])],original["revision"])
        raise AssertionError("stale revision accepted")
    except BridgeError as exc:
        assert "Revision conflict" in str(exc)
    undone=batch([op("undo")]);assert not any(r["id"]==shape for r in undone["records"])
    redone=batch([op("redo")]);assert any(r["id"]==shape for r in redone["records"])
    before=c.call("state",args)
    try:
        c.call("script",args|{"revision":before["revision"],"code":f'editor.updateShapes([{{id:{json.dumps(shape)},type:"geo",props:{{color:"green"}}}}]); throw new Error("rollback-test")'})
        raise AssertionError("script did not throw")
    except BridgeError as exc:
        assert "rollback-test" in str(exc)
    assert_restored(before)
    after=c.call("state",args)
    updated=c.call("script",args|{"full":True,"revision":after["revision"],"code":f'editor.updateShapes([{{id:{json.dumps(shape)},type:"geo",props:{{color:"violet"}}}}]);'})
    assert next(r for r in updated["records"] if r["id"]==shape)["props"]["color"]=="violet"
    before_document=c.call("state",args)
    try:
        c.call("script",args|{"revision":before_document["revision"],"code":'editor.updateDocumentSettings({gridSize:999}); throw new Error("document-rollback-test")'})
        raise AssertionError("document script did not throw")
    except BridgeError as exc:
        assert "document-rollback-test" in str(exc)
    assert_restored(before_document)
    for code,expected_error in [
        ('throw null','null'),
        ('throw undefined','undefined'),
        ('throw "live failure"','live failure'),
        ('throw new Error("live failure")','live failure'),
        ('throw {get message(){throw null},toString(){throw undefined}}','Unknown error (unprintable thrown value)'),
    ]:
        try:
            c.call("script",args|{"revision":before_document["revision"],"code":'editor.updateDocumentSettings({gridSize:999}); '+code})
            raise AssertionError("Expected script failure")
        except BridgeError as exc:
            assert str(exc).startswith(expected_error+" (request "),str(exc)
        assert_restored(before_document)
        assert c.call("doctor")["supported"]
    document=next(r for r in before_document["records"] if r["typeName"]=="document")
    try:
        changed=c.call("script",args|{"revision":before_document["revision"],"code":f'editor.updateDocumentSettings({{gridSize:{document["gridSize"]+1}}});'})
        assert changed["revision"]!=before_document["revision"]
        assert changed["persistence"]["saved"]
    finally:
        current=c.call("state",args)
        c.call("script",args|{"revision":current["revision"],"code":f'editor.updateDocumentSettings({{gridSize:{document["gridSize"]}}});'})
    preview=c.call("preview",args|{"output":str(Path(a.output).resolve())})
    assert Path(preview["path"]).read_bytes().startswith(b"\x89PNG")
    print(json.dumps({"passed":["CRUD/persistence","idempotent-retry","revision-conflict","undo","redo","script-rollback","SDK-script","document-rollback","arbitrary-exception-shared-store-and-persistence","document-only-save","PNG"],"preview":preview},indent=2))
finally:
    current=c.call("state",args)
    if any(r["id"]==shape for r in current["records"]):
        batch([op("deleteShapes",[shape])])
    c.call("close",args)
    c.forget(request)
    runtime_dir.cleanup()
