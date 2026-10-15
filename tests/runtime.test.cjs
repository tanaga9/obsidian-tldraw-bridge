'use strict'
const { test } = require('node:test')
const assert = require('node:assert/strict')
const fs = require('node:fs')
const os = require('node:os')
const path = require('node:path')
const vm = require('node:vm')
const source = fs.readFileSync(path.join(__dirname, '../src/obsidian_tldraw_bridge/runtime/bridge.cjs'), 'utf8')
const copy = value => JSON.parse(JSON.stringify(value))
function setup() {
  const context = { require, module: {exports: {}}, Buffer, setTimeout }
  vm.runInNewContext(source + '\nmodule.exports.testAccess = { sessionsFor, revision, saved, script, batch };', context)
  const api = context.module.exports
  const access = api.testAccess
  let values = [
    {id:'document:document', typeName:'document', name:'Original', gridSize:10},
    {id:'page:a', typeName:'page', name:'Page'},
    {id:'shape:a', typeName:'shape', props:{color:'blue'}},
    {id:'camera:a', typeName:'camera', x:0},
  ]
  let disk = copy(values)
  const editor = {
    isDisposed:false,
    store: {
      scopedTypes: {document:new Set(['document','page','shape','asset','binding','custom'])},
      allRecords:()=>values,
      listen:()=>()=>{},
      getStoreSnapshot:()=>({store:Object.fromEntries(copy(values).map(r=>[r.id,r]))}),
      applyDiff:diff=>{
        const map = new Map(values.map(r=>[r.id,r]))
        for(const r of Object.values(diff.added)) map.set(r.id,r)
        for(const [,r] of Object.values(diff.updated)) map.set(r.id,r)
        for(const id of Object.keys(diff.removed)) map.delete(id)
        values=[...map.values()]
      },
    },
    run:fn=>fn(),
    markHistoryStoppingPoint:()=>copy(values.find(r=>r.id==='shape:a')),
    // Simulate the actual limitation: document settings are not in undo history.
    bailToMark:mark=>{values=values.map(r=>r.id===mark.id?mark:r)},
    updateDocumentSettings:settings=>Object.assign(values.find(r=>r.typeName==='document'),settings),
    updateShapes:changes=>{for(const change of changes)Object.assign(values.find(r=>r.id===change.id),change)},
    getCurrentPageShapeIds:()=>['shape:a'],
    getCurrentPageId:()=> 'page:a',
  }
  const markdown=records=>'```json !!!_START_OF_TLDRAW_DATA__DO_NOT_CHANGE_THIS_PHRASE_!!!\n'+JSON.stringify({raw:{records}})+'\n!!!_END_OF_TLDRAW_DATA__DO_NOT_CHANGE_THIS_PHRASE_!!!'
  const app={vault:{getName:()=> 'test',read:async()=>markdown(disk)},plugins:{getPlugin:()=>({manifest:{version:'1.32.0'}})},workspace:{getActiveFile:()=>null,getLeavesOfType:()=>[]}}
  access.sessionsFor(app).set('a.md',{path:'a.md',file:{path:'a.md'},editor,seed:editor})
  async function invoke(action,args={},id='job') {
    api.dispatch(app,action,args,id)
    for(let i=0;i<30;i++) {
      await new Promise(resolve=>setImmediate(resolve))
      const job=JSON.parse(api.poll(app,id))
      if(job.status==='failed') throw new Error(job.error)
      if(job.status==='complete') return job.result
    }
    throw new Error('Test job did not finish')
  }
  return {api,access,editor,app,invoke,values:()=>values,markdown,setDisk:value=>{disk=copy(value)}}
}

test('document scope drives revisions and includes custom persistent types',()=>{
  const h=setup(), before=h.access.revision(h.editor)
  h.editor.updateDocumentSettings({gridSize:20})
  assert.notEqual(h.access.revision(h.editor),before)
  const after=h.access.revision(h.editor)
  h.values().find(r=>r.typeName==='camera').x=20
  assert.equal(h.access.revision(h.editor),after)
  h.values().push({id:'custom:a',typeName:'custom',value:1})
  assert.notEqual(h.access.revision(h.editor),after)
})

test('save waits for document settings to reach Markdown',async()=>{
  const h=setup(), old=copy(h.values())
  h.editor.updateDocumentSettings({name:'Unsaved'})
  let reads=0
  h.app.vault.read=async()=>h.markdown(++reads===1?old:copy(h.values()))
  assert.equal((await h.access.saved(h.app,'a.md')).saved,true)
  assert.equal(reads,2)
})

test('synchronous failure restores history-ignored document changes',()=>{
  const h=setup(), before=h.access.revision(h.editor)
  assert.throws(()=>h.access.script(h.app,'a.md', 'editor.updateDocumentSettings({name:"changed"}); editor.updateShapes([{id:"shape:a",props:{color:"red"}}]); throw new Error("failure")',before),/failure/)
  assert.equal(h.access.revision(h.editor),before)
})

test('batch failure restores document records even when undo ignores them',()=>{
  const h=setup(), before=h.access.revision(h.editor)
  h.editor.updateShapes=()=>{h.editor.updateDocumentSettings({gridSize:99});throw new Error('bad operation')}
  assert.throws(()=>h.access.batch(h.app,'a.md',[{method:'updateShapes',args:[[]]}],before),/bad operation/)
  assert.equal(h.access.revision(h.editor),before)
})

test('preview fails without replacing an output file if export changes revision',async()=>{
  const h=setup(), dir=fs.mkdtempSync(path.join(os.tmpdir(),'bridge-preview-')),output=path.join(dir,'out.png')
  fs.writeFileSync(output,'existing preview')
  h.editor.toImage=async()=>({blob:{arrayBuffer:async()=>{h.editor.updateDocumentSettings({name:'during export'});return Buffer.from('old image')}},width:1,height:1})
  try {
    await assert.rejects(h.invoke('preview',{path:'a.md',revision:h.access.revision(h.editor),output}),/Revision conflict during preview/)
    assert.equal(fs.readFileSync(output,'utf8'),'existing preview')
  } finally {fs.rmSync(dir,{recursive:true,force:true})}
})

test('unchanged preview writes bytes tagged with the captured revision',async()=>{
  const h=setup(), dir=fs.mkdtempSync(path.join(os.tmpdir(),'bridge-preview-')),output=path.join(dir,'out.png')
  h.editor.toImage=async()=>({blob:{arrayBuffer:async()=>Buffer.from('image')},width:1,height:1})
  try {
    const before=h.access.revision(h.editor)
    assert.equal((await h.invoke('preview',{path:'a.md',output})).revision,before)
    assert.equal(fs.readFileSync(output,'utf8'),'image')
  } finally {fs.rmSync(dir,{recursive:true,force:true})}
})

test('receipt limit preserves replay and frees capacity only on explicit forget',async()=>{
  const h=setup()
  for(let i=0;i<128;i++)await h.invoke('doctor',{},'id-'+i)
  assert.throws(()=>h.api.dispatch(h.app,'doctor',{},'overflow'),/Receipt capacity/)
  assert.equal(JSON.parse(h.api.dispatch(h.app,'doctor',{},'id-0')).status,'complete')
  assert.throws(()=>h.api.dispatch(h.app,'state',{path:'a.md'},'id-0'),/another request/)
  assert.equal(JSON.parse(h.api.forget(h.app,'id-0')).forgotten,true)
  assert.equal((await h.invoke('doctor',{},'new-id')).vault,'test')
})

for (const [name,code,message] of [
  ['null', 'throw null', 'null'],
  ['undefined', 'throw undefined', 'undefined'],
  ['string', 'throw "script failure"', 'script failure'],
  ['Error', 'throw new Error("normal failure")', 'normal failure'],
  ['unprintable object', 'throw {get message(){throw null},toString(){throw undefined}}', 'Unknown error (unprintable thrown value)'],
]) {
  test(`thrown ${name} fails cleanly and allows the next request`,async()=>{
    const h=setup(), before=h.access.revision(h.editor)
    const args={path:'a.md',revision:before,code:'editor.updateDocumentSettings({name:"temporary"}); '+code}
    await assert.rejects(h.invoke('script',args,'failure'),error=>error.message===message)
    const job=JSON.parse(h.api.poll(h.app,'failure'))
    assert.equal(job.status,'failed')
    assert.equal(job.error,message)
    assert.equal(h.access.revision(h.editor),before)
    assert.equal((await h.invoke('doctor',{},'after-failure')).vault,'test')
  })
}

test('a non-Error rollback failure preserves both error messages and releases the job',async()=>{
  const h=setup()
  h.editor.bailToMark=()=>{throw null}
  await assert.rejects(h.invoke('script',{path:'a.md',revision:h.access.revision(h.editor),code:'throw "original failure"'},'rollback-failure'),/original failure; record restoration failed: null/)
  assert.equal(JSON.parse(h.api.poll(h.app,'rollback-failure')).status,'failed')
  assert.equal((await h.invoke('doctor',{},'after-rollback-failure')).vault,'test')
})

test('failed scripts restore shared records when SDK transaction aborts do not restore queued notifications',async()=>{
  const h=setup(), before=h.access.revision(h.editor)
  let shared=copy(h.values())
  let depth=0
  let notifications=[]
  const apply=h.editor.store.applyDiff
  const update=h.editor.updateDocumentSettings
  const snapshot=()=>copy(h.values().find(r=>r.typeName==='document'))
  h.editor.updateDocumentSettings=settings=>{update(settings);notifications.push(snapshot())}
  h.editor.store.applyDiff=diff=>{
    apply(diff)
    if(Object.keys(diff.added).length || Object.keys(diff.updated).length || Object.keys(diff.removed).length) notifications.push(snapshot())
  }
  h.editor.run=fn=>{
    const root=depth++===0
    const initial=snapshot()
    try {return fn()} catch(error) {
      // The SDK abort restores reactive records, but its plain notification
      // accumulator can retain a forward change made by the failed callback.
      if(root) apply({added:{},updated:{[initial.id]:[snapshot(),initial]},removed:{}})
      throw error
    } finally {
      depth--
      if(root) setImmediate(()=>{
        for(const record of notifications) shared=shared.map(r=>r.id===record.id?record:r)
        notifications=[]
        h.setDisk(shared)
      })
    }
  }
  await assert.rejects(h.invoke('script',{path:'a.md',revision:before,code:'editor.updateDocumentSettings({gridSize:999}); throw new Error("failed script")'},'failed-script'),/failed script/)
  await new Promise(resolve=>setImmediate(resolve))
  assert.equal(h.access.revision(h.editor),before)
  assert.equal(shared.find(r=>r.typeName==='document').gridSize,10)
  assert.equal((await h.access.saved(h.app,'a.md')).saved,true)
})

test('save drains source and shared notifications before checking Markdown',async()=>{
  const h=setup(), flushed=[]
  h.editor.updateDocumentSettings({gridSize:20})
  h.editor.store.listen=()=>{flushed.push('source');return ()=>flushed.push('source listener removed')}
  const main={listen:()=>{
    assert.equal(flushed[0],'source')
    flushed.push('main')
    h.setDisk(h.values())
    return ()=>flushed.push('main listener removed')
  }}
  h.app.plugins.getPlugin=()=>({tlDataDocumentStoreManager:{storesManager:{storeGroupMap:new Map([['a.md',{main:{store:main}}]])}}})
  assert.equal((await h.access.saved(h.app,'a.md')).saved,true)
  assert.deepEqual(flushed,['source','source listener removed','main','main listener removed'])
})

function createFixture() {
  const h = setup()
  const files = new Map()
  const calls = []
  const plugin = {
    manifest: {version:'1.32.0'},
    async createTldrFile(filename, options) {
      calls.push({filename,options})
      const actual = h.actualPath || [options.foldername,filename].filter(Boolean).join('/')
      const file = {path:actual,extension:'md'}
      files.set(actual,file)
      return file
    },
    async openTldrFile(file, location, type) {
      calls.push({opened:file.path,location,type})
      if(h.openError) throw new Error(h.openError)
      // Model the already-open session boundary; real Editor construction is
      // exercised by the opt-in create integration test.
      h.access.sessionsFor(h.app).set(file.path,{path:file.path,file,editor:h.editor,seed:h.editor})
    },
  }
  h.app.plugins.getPlugin=()=>plugin
  h.app.vault.getAbstractFileByPath=path=>files.get(path)
  return Object.assign(h,{files,calls,plugin})
}

test('create delegates Markdown generation to plugin and returns saved editable session',async()=>{
  const h=createFixture()
  const result=await h.invoke('create',{path:'Drawings/project-plan.md'},'create-plan')
  assert.equal(result.created,true)
  assert.equal(result.path,'Drawings/project-plan.md')
  assert.equal(result.requestedPath,result.path)
  assert.equal(result.persistence.saved,true)
  assert.equal(result.currentPageId,'page:a')
  assert.ok(result.revision)
  assert.deepEqual(copy(h.calls[0]),{filename:'project-plan.md',options:{foldername:'Drawings',inMarkdown:true}})
  assert.deepEqual(h.calls[1],{opened:'Drawings/project-plan.md',location:'new-tab',type:'tldraw-view'})
  const replay=await h.invoke('create',{path:'Drawings/project-plan.md'},'create-plan')
  assert.equal(replay.revision,result.revision)
  assert.equal(h.calls.length,2)
})

test('create refuses existing files or folders without changing them',async()=>{
  const h=createFixture(), existing={path:'existing.md',content:'keep me'}
  h.files.set(existing.path,existing)
  await assert.rejects(h.invoke('create',{path:existing.path}),/already exists/)
  assert.equal(h.files.get(existing.path),existing)
  assert.equal(h.calls.length,0)
})

test('create refuses unsafe paths even when called without CLI validation',async()=>{
  for(const path of ['/absolute.md','../escape.md','a/../escape.md','a/./x.md','a//x.md','a\\x.md','x.tldr','.md','a/\u0000x.md']) {
    const h=createFixture()
    await assert.rejects(h.invoke('create',{path}),/vault-relative Markdown path/)
    assert.equal(h.calls.length,0)
  }
})

test('create checks plugin compatibility before writing',async()=>{
  const h=createFixture()
  h.plugin.manifest.version='0.0.0'
  await assert.rejects(h.invoke('create',{path:'plan.md'}),/Unsupported/)
  assert.equal(h.calls.length,0)
})

test('create reports actual plugin-assigned path if a competing creation takes the requested name',async()=>{
  const h=createFixture()
  h.actualPath='plan 1.md'
  const result=await h.invoke('create',{path:'plan.md'})
  assert.equal(result.path,'plan 1.md')
  assert.equal(result.requestedPath,'plan.md')
  assert.equal(result.persistence.path,'plan 1.md')
})

test('initialization failure retains created file and reports recovery path without recreating on replay',async()=>{
  const h=createFixture()
  h.openError='Editor unavailable'
  await assert.rejects(h.invoke('create',{path:'plan.md'},'create-failed'),/Created plan.md.*Editor unavailable.*Use open/)
  assert.ok(h.files.has('plan.md'))
  await assert.rejects(h.invoke('create',{path:'plan.md'},'create-failed'),/Created plan.md/)
  assert.equal(h.calls.filter(c=>c.filename).length,1)
})

test('create refuses to reuse a stale session path',async()=>{
  const h=createFixture()
  await assert.rejects(h.invoke('create',{path:'a.md'}),/Close the existing session/)
  assert.equal(h.calls.length,0)
})
