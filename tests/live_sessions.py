import sys,json,time,uuid,argparse
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from obsidian_tldraw_bridge.obsidian import Client
p=argparse.ArgumentParser(description="Opt-in test: creates and deletes a temporary copy of a dedicated probe diagram")
p.add_argument("--vault",required=True)
p.add_argument("--path",required=True)
options=p.parse_args()
c=Client(options.vault)
a=options.path
b='Codex Bridge Multi '+uuid.uuid4().hex+'.md'
id='shape:multi-'+uuid.uuid4().hex
c.evaluate('(async()=>{await app.vault.create('+json.dumps(b)+',await app.vault.read(app.vault.getAbstractFileByPath('+json.dumps(a)+')));})()',True)
for _ in range(30):
 if c.evaluate('JSON.stringify(!!app.vault.getAbstractFileByPath('+json.dumps(b)+'))'):break
 time.sleep(.1)
try:
 sa=c.call('open',{'path':a});sb=c.call('open',{'path':b})
 edited=c.call('batch',{'full':True,'path':b,'revision':sb['revision'],'operations':[{'method':'createShapes','args':[[{'id':id,'type':'geo','x':500,'y':0,'props':{'geo':'ellipse','w':80,'h':80}}]]}]})
 assert any(r['id']==id for r in edited['records'])
 assert c.call('state',{'path':a})['revision']==sa['revision']
 assert edited['persistence']['saved']
 print('Multiple document sessions: independent edits and Markdown persistence passed')
finally:
 for path in [a,b]:
  if path in c.call('doctor')['documents']:c.call('close',{'path':path})
 c.evaluate('(async()=>{const f=app.vault.getAbstractFileByPath('+json.dumps(b)+');if(f)await app.vault.delete(f);})()',True)
 for _ in range(30):
  if not c.evaluate('JSON.stringify(!!app.vault.getAbstractFileByPath('+json.dumps(b)+'))'):break
  time.sleep(.1)
 else:raise RuntimeError('Temporary fixture cleanup not confirmed')
 print('Temporary Markdown fixture removed; sessions closed')
