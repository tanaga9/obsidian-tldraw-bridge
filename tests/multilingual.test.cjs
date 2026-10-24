'use strict'
const {test}=require('node:test')
const assert=require('node:assert/strict')
const fs=require('node:fs'), os=require('node:os'), path=require('node:path')
const {spawnSync,execFileSync}=require('node:child_process')
const {reviewLanguages,languageHashes}=require('../src/obsidian_tldraw_bridge/runtime/bridge.cjs')
const copy=v=>JSON.parse(JSON.stringify(v))
function fixture(){
 const values=[{id:'document:document',typeName:'document',meta:{}},
  {id:'page:en',typeName:'page',name:'English',meta:{diagramId:'overview',language:'en'}},
  {id:'page:ja',typeName:'page',name:'日本語',meta:{diagramId:'overview',language:'ja'}},
  {id:'shape:en',typeName:'shape',type:'geo',parentId:'page:en',x:0,y:0,index:'a1',props:{w:200,h:100,text:'Review',color:'blue'}},
  {id:'shape:ja',typeName:'shape',type:'geo',parentId:'page:ja',x:0,y:0,index:'a1',props:{w:200,h:100,text:'確認',color:'blue'}}]
 values[0].meta.multilingualDiagrams={overview:{schemaVersion:2,editingSourcePageId:'page:en',languages:{en:'page:en',ja:'page:ja'},checkpoints:{ja:{algorithm:'page-content-v2',sourcePageId:'page:en',source:languageHashes(values,'page:en'),target:languageHashes(values,'page:ja')}}}}
 return values
}
const target=v=>reviewLanguages(v).diagrams.find(r=>r.language==='ja')
test('content changes, independent target edits and divergence are distinguished',()=>{
 const v=fixture();assert.equal(target(v).status,'current')
 v[3].props.text='Approve';assert.equal(target(v).status,'source-content-changed')
 v[4].props.text='検証';assert.equal(target(v).status,'diverged')
 v[3].props.text='Review';assert.equal(target(v).status,'target-content-changed')
})
test('geometry edits require presentation review; no semantic safety is claimed',()=>{
 const v=fixture(),before=copy(v);v[4].x=70;v[4].props.w=320
 assert.equal(target(v).status,'presentation-review')
 assert.equal(reviewLanguages(v).requiresReview,true)
 assert.deepEqual(v[0],before[0]);assert.equal(v[3].props.text,'Review')
 // Unknown custom properties and visual encodings remain conservative.
 v[4].props.customMeaning='new';assert.equal(target(v).status,'target-content-changed')
})
test('page names, metadata, camera and locks do not trigger translation',()=>{
 const v=fixture();v[1].name='Renamed';v[2].meta.note='UI';v[4].isLocked=true
 v.push({id:'camera:a',typeName:'camera',x:500})
 assert.equal(target(v).status,'current')
})
test('assets and nested shapes participate in freshness',()=>{
 const v=fixture();v.push({id:'asset:a',typeName:'asset',props:{src:'data:old'}});v[4].props.assetId='asset:a'
 const before=languageHashes(v,'page:ja');v.at(-1).props.src='data:new'
 assert.notEqual(languageHashes(v,'page:ja').content,before.content)
 v.push({id:'shape:child',typeName:'shape',type:'text',parentId:'shape:ja',props:{text:'Detail'}})
 assert.equal(target(v).status,'target-content-changed')
})
test('duplicate, orphaned and missing language pages require review',()=>{
 for(const change of [v=>v.push({...v[2],id:'page:dup'}),v=>v.splice(2,1),v=>delete v[0].meta.multilingualDiagrams.overview]){
  const v=fixture();change(v);const report=reviewLanguages(v)
  assert.ok(report.errors.length);assert.equal(report.requiresReview,true)
 }
})
test('diagram selection isolates unrelated diagrams and source handoff invalidates old lineage',()=>{
 const v=fixture();v[0].meta.multilingualDiagrams.other={languages:{fr:'page:missing'}}
 assert.equal(reviewLanguages(v,'overview').requiresReview,false)
 const g=v[0].meta.multilingualDiagrams.overview
 v.push({id:'page:fr',typeName:'page',meta:{diagramId:'overview',language:'fr'}});g.languages.fr='page:fr';g.editingSourcePageId='page:fr'
 assert.equal(target(v).status,'source-changed')
})
test('legacy generation and explicitly reviewed layout baselines remain readable',()=>{
 const v=fixture(),g=v[0].meta.multilingualDiagrams.overview;delete g.checkpoints
 g.translations={ja:{hashAlgorithm:'sha256-page-records-v1',sourcePageId:'page:en',sourceHash:languageHashes(v,'page:en').legacy,targetHash:languageHashes(v,'page:ja').legacy}}
 assert.equal(target(v).status,'current');v[4].y=100;assert.equal(target(v).status,'needs-review')
 g.layoutReview={classification:'layout-only',editingSourcePageId:'page:en',pageHashes:{en:languageHashes(v,'page:en').legacy,ja:languageHashes(v,'page:ja').legacy}}
 assert.equal(target(v).status,'reviewed-layout');v[3].props.text='Changed';assert.equal(target(v).status,'needs-review')
})
test('legacy asset pages cannot pass through generation or layout-only baselines',()=>{
 for (const language of ['en','ja']) {
  const v=fixture(),g=v[0].meta.multilingualDiagrams.overview;delete g.checkpoints
  v.find(r=>r.id==='shape:'+language).props.assetId='asset:image'
  v.push({id:'asset:image',typeName:'asset',props:{src:'data:old'}})
  g.translations={ja:{hashAlgorithm:'sha256-page-records-v1',sourcePageId:'page:en',sourceHash:languageHashes(v,'page:en').legacy,targetHash:languageHashes(v,'page:ja').legacy}}
  g.layoutReview={classification:'layout-only',editingSourcePageId:'page:en',pageHashes:{en:languageHashes(v,'page:en').legacy,ja:languageHashes(v,'page:ja').legacy}}
  // Even an unchanged image cannot be verified by an asset-free baseline.
  assert.equal(target(v).status,'needs-review')
  v.at(-1).props.src='data:new'
  const report=reviewLanguages(v),item=report.diagrams.find(r=>r.language==='ja')
  assert.equal(report.requiresReview,true)
  assert.equal(item.status,'needs-review')
  assert.equal(item.reviewReason,'legacy-baseline-excludes-assets')
  assert.equal(item[language==='en'?'sourceChanged':'targetChanged'],null)
 }
})
test('current page and asset hashes are independent of process locale and record order',()=>{
 const runtime=path.resolve(__dirname,'../src/obsidian_tldraw_bridge/runtime/bridge.cjs')
 const code=`const {languageHashes}=require(${JSON.stringify(runtime)});
 const values=[{id:'page:en',typeName:'page'},...['I','i'].flatMap(id=>[
 {id:'shape:'+id,typeName:'shape',type:'image',parentId:'page:en',props:{assetId:'asset:'+id}},
 {id:'asset:'+id,typeName:'asset',props:{src:'data:'+id}}])];
 const selected=rs=>{const {full,content}=languageHashes(rs,'page:en');return {full,content}};
 console.log(JSON.stringify([selected(values),selected([...values].reverse())]));`
 const results=['en_US.UTF-8','tr_TR.UTF-8'].map(locale=>{
  const run=spawnSync(process.execPath,['-e',code],{encoding:'utf8',env:{...process.env,LANG:locale,LC_ALL:locale}})
  assert.equal(run.status,0,run.stderr)
  const result=JSON.parse(run.stdout);assert.deepEqual(result[0],result[1]);return result[0]
 })
 assert.deepEqual(results[0],results[1])
})
test('Git review inspects staged blobs separately from working tree without writing',()=>{
 const root=fs.mkdtempSync(path.join(os.tmpdir(),'language-git-'))
 const git=(...args)=>execFileSync('git',args,{cwd:root,stdio:'pipe'})
 const markdown=v=>'```json !!!_START_OF_TLDRAW_DATA__DO_NOT_CHANGE_THIS_PHRASE_!!!\n'+JSON.stringify({raw:{records:v}})+'\n!!!_END_OF_TLDRAW_DATA__DO_NOT_CHANGE_THIS_PHRASE_!!!\n```'
 try{
  git('init');git('config','user.name','Test');git('config','user.email','test@example.invalid')
  const clean=markdown(fixture());fs.writeFileSync(path.join(root,'図.md'),clean);git('add','.');git('commit','-m','Initial')
  const v=fixture();v[3].props.text='Approve';fs.writeFileSync(path.join(root,'図.md'),markdown(v));git('add','図.md')
  fs.writeFileSync(path.join(root,'図.md'),clean)
  const script=path.resolve(__dirname,'../scripts/review_translations.cjs')
  const run=spawnSync(process.execPath,[script,'--strict'],{cwd:root,encoding:'utf8'})
  assert.equal(run.status,2,run.stderr)
  const report=JSON.parse(run.stdout)
  const staged=report.reports.find(r=>r.version==='index'),working=report.reports.find(r=>r.version==='worktree')
  assert.equal(staged.diagrams.find(r=>r.language==='ja').status,'source-content-changed')
  assert.equal(working.diagrams.find(r=>r.language==='ja').status,'current')
  assert.equal(fs.readFileSync(path.join(root,'図.md'),'utf8'),clean)
  assert.equal(git('show',':図.md').toString(),markdown(v))
  fs.writeFileSync(path.join(root,'new.md'),clean)
  const untracked=spawnSync(process.execPath,[script,'new.md'],{cwd:root,encoding:'utf8'})
  assert.equal(untracked.status,0,untracked.stderr)
  const newReport=JSON.parse(untracked.stdout)
  assert.equal(newReport.errors.length,0)
  assert.equal(newReport.reports.length,1)
  assert.equal(newReport.reports[0].version,'worktree')
  const marker='```json !!!_START_OF_TLDRAW_DATA__DO_NOT_CHANGE_THIS_PHRASE_!!!'
  const damaged=clean.replace(marker,'```json')
  fs.writeFileSync(path.join(root,'図.md'),damaged);git('add','図.md')
  // The staged Note remains damaged even when the working copy is repaired.
  fs.writeFileSync(path.join(root,'図.md'),clean)
  const stagedDamage=spawnSync(process.execPath,[script,'--staged','--strict'],{cwd:root,encoding:'utf8'})
  assert.equal(stagedDamage.status,1,stagedDamage.stderr)
  assert.match(JSON.parse(stagedDamage.stdout).errors[0].message,/Missing tldraw start marker/)
  git('add','図.md');fs.writeFileSync(path.join(root,'図.md'),damaged)
  const worktreeDamage=spawnSync(process.execPath,[script,'--worktree','--strict'],{cwd:root,encoding:'utf8'})
  assert.equal(worktreeDamage.status,1,worktreeDamage.stderr)
  assert.match(JSON.parse(worktreeDamage.stdout).errors[0].message,/Missing tldraw start marker/)
  assert.equal(fs.readFileSync(path.join(root,'図.md'),'utf8'),damaged)
  // Repairing a historical malformed Note must inspect the valid current data,
  // rather than report the old format error as if the repair were still broken.
  fs.writeFileSync(path.join(root,'repair.md'),clean.replace('!!!_END_OF_TLDRAW_DATA__DO_NOT_CHANGE_THIS_PHRASE_!!!','BROKEN_END'))
  git('add','repair.md');git('commit','-m','Malformed historical Note')
  fs.writeFileSync(path.join(root,'repair.md'),clean);git('add','repair.md')
  const repaired=spawnSync(process.execPath,[script,'--staged','--strict','repair.md'],{cwd:root,encoding:'utf8'})
  assert.equal(repaired.status,0,repaired.stderr)
  const repairReport=JSON.parse(repaired.stdout)
  assert.equal(repairReport.requiresReview,false)
  assert.equal(repairReport.errors.length,0)
  assert.match(repairReport.reports[0].baselineWarning,/Previous Note could not be parsed/)
  assert.equal(repairReport.reports[0].diagrams.find(r=>r.language==='ja').status,'current')
  fs.writeFileSync(path.join(root,'repair.md'),clean.replace('!!!_END_OF_TLDRAW_DATA__DO_NOT_CHANGE_THIS_PHRASE_!!!','BROKEN_END'))
  const stillBroken=spawnSync(process.execPath,[script,'--worktree','--strict','repair.md'],{cwd:root,encoding:'utf8'})
  assert.equal(stillBroken.status,1,stillBroken.stderr)
  assert.match(JSON.parse(stillBroken.stdout).errors[0].message,/Missing tldraw end marker/)
 }finally{fs.rmSync(root,{recursive:true,force:true})}
})
