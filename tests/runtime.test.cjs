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
    getShape:id=>values.find(r=>r.id===id),
    getCurrentPageId:()=> 'page:a',
  }
  const markdown=records=>'```json !!!_START_OF_TLDRAW_DATA__DO_NOT_CHANGE_THIS_PHRASE_!!!\n'+JSON.stringify({raw:{records}})+'\n!!!_END_OF_TLDRAW_DATA__DO_NOT_CHANGE_THIS_PHRASE_!!!'
  const plugin={manifest:{version:'1.32.0'},openTldrFile:async()=>{},getFontOverrides:()=>({}),
    tlDataDocumentStoreManager:{register:()=>{},storesManager:{storeGroupMap:new Map()}}}
  const app={vault:{getName:()=> 'test',read:async()=>markdown(disk)},plugins:{getPlugin:()=>plugin},workspace:{getActiveFile:()=>null,getLeavesOfType:()=>[]}}
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
  return {api,access,editor,app,plugin,invoke,values:()=>values,markdown,setDisk:value=>{disk=copy(value)}}
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

test('part preview exports only tagged current-page strokes at the requested scale',async()=>{
  const h=setup(), dir=fs.mkdtempSync(path.join(os.tmpdir(),'bridge-detail-')),output=path.join(dir,'out.png')
  h.values().find(r=>r.id==='shape:a').meta={bridgeFreehand:{part:'detail'}}
  h.values().push({id:'shape:other',typeName:'shape',meta:{bridgeFreehand:{part:'detail'}}})
  let received
  h.editor.toImage=async(ids,options)=>{
    received={ids:Array.from(ids),scale:options.scale}
    return {blob:{arrayBuffer:async()=>Buffer.from('detail')},width:300,height:300}
  }
  try {
    await h.invoke('preview',{path:'a.md',part:'detail',scale:3,output})
    assert.deepEqual(received,{ids:['shape:a'],scale:3})
  } finally {fs.rmSync(dir,{recursive:true,force:true})}
})

test('bad preview selections and scales leave existing output untouched',async()=>{
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'bridge-bad-detail-')),output=path.join(dir,'out.png')
  fs.writeFileSync(output,'original')
  try {
    for(const args of [{ids:[]},{ids:['shape:missing']},{part:'missing'},{ids:['shape:a'],part:'detail'},
      {bounds:{x:0,y:0,w:0,h:20}},{bounds:{x:NaN,y:0,w:20,h:20}},
      {bounds:{x:0,y:0,w:20,h:20},part:'detail'},{bounds:null},
      {scale:0},{scale:5},{scale:NaN}]){
      const h=setup()
      h.editor.toImage=async()=>{throw new Error('Unexpected render')}
      await assert.rejects(h.invoke('preview',{path:'a.md',output,...args}),error=>!error.message.includes('Unexpected render'))
      assert.equal(fs.readFileSync(output,'utf8'),'original')
    }
  } finally {fs.rmSync(dir,{recursive:true,force:true})}
})

test('bounds preview includes surrounding shapes and crops without changing cached bounds',async()=>{
  const h=setup(), dir=fs.mkdtempSync(path.join(os.tmpdir(),'bridge-crop-')),output=path.join(dir,'out.png')
  h.editor.getCurrentPageShapeIds=()=>['shape:a','shape:b']
  const geometry={x:0,y:0,w:800,h:1000,clone(){return {...this}}}
  h.editor.getShapePageBounds=()=>geometry
  let received
  h.editor.toImage=async(ids,options)=>{
    received={ids:Array.from(ids),bounds:options.bounds,padding:options.padding}
    return {blob:{arrayBuffer:async()=>Buffer.from('crop')},width:200,height:150}
  }
  try {
    const before=h.access.revision(h.editor)
    const bounds={x:100,y:120,w:200,h:150}
    const result=await h.invoke('preview',{path:'a.md',bounds,output})
    assert.deepEqual(received.ids,['shape:a','shape:b'])
    for(const key of ['x','y','w','h'])assert.equal(received.bounds[key],bounds[key])
    assert.equal(received.padding,0)
    assert.deepEqual([geometry.x,geometry.y,geometry.w,geometry.h],[0,0,800,1000])
    assert.equal(result.revision,before)
    assert.equal(h.access.revision(h.editor),before)
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
  assert.deepEqual(flushed,['source','source listener removed','main','main listener removed',
    'source','source listener removed','main','main listener removed'])
})

function createFixture() {
  const h = setup()
  const files = new Map()
  const calls = []
  const plugin = {
    ...h.plugin,
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

test('create allows untested versions with the required plugin APIs',async()=>{
  const h=createFixture()
  h.plugin.manifest.version='99.0.0'
  assert.equal((await h.invoke('create',{path:'plan.md'})).created,true)
})

test('create checks required APIs before writing, including for tested versions',async()=>{
  for(const name of ['createTldrFile','openTldrFile','getFontOverrides']) {
    const h=createFixture()
    delete h.plugin[name]
    await assert.rejects(h.invoke('create',{path:'plan.md'}),new RegExp(`plugin.${name}`))
    assert.equal(h.calls.length,0)
    assert.equal(h.files.size,0)
    const job=JSON.parse(h.api.poll(h.app,'job'))
    assert.equal(job.failure.code,'TLDRAW_UNSUPPORTED')
    assert.equal(job.failure.outcome,'not_applied')
  }
})

test('doctor and capabilities distinguish API availability from tested versions',async()=>{
  for(const version of ['1.31.0','1.32.0','99.0.0']) {
    const h=setup()
    h.plugin.manifest.version=version
    for(const action of ['doctor','capabilities']) {
      const result=await h.invoke(action,{},action)
      assert.equal(result.supported,true)
      assert.equal(result.versionTested,version!=='99.0.0')
      assert.deepEqual(result.testedPluginVersions,['1.31.0','1.32.0'])
      assert.deepEqual(result.missingCapabilities,[])
    }
  }
  const h=setup()
  delete h.plugin.tlDataDocumentStoreManager.register
  const result=await h.invoke('doctor')
  assert.equal(result.supported,false)
  assert.deepEqual(result.missingCapabilities,['plugin.tlDataDocumentStoreManager.register'])
})

function openFixture() {
  const h=setup(), cleanup=[]
  const file={path:'new.md',extension:'md'}
  h.app.vault.getAbstractFileByPath=()=>file
  const document={body:{appendChild:()=>{}},createElement:()=>({
    ownerDocument:document,style:{},remove:()=>cleanup.push('container'),
  })}
  Object.assign(h.editor,{
    shapeUtils:{geo:{constructor:class Geo {}}},bindingUtils:{},assetUtils:{},root:{children:{}},
    getContainer:()=>({ownerDocument:document}),getPage:()=>({id:'page:a'}),setCurrentPage:()=>{},
    getShapeUtil:()=>({}),getShapePageBounds:()=>({}),dispose:()=>cleanup.push('editor'),
    constructor:function Editor(options) {return {...h.editor,store:options.store}},
  })
  h.plugin.currTldrawEditor=h.editor
  const registration={documentStore:{store:h.editor.store},syncToMain:()=>{},unregister:()=>cleanup.push('registration')}
  h.plugin.tlDataDocumentStoreManager.register=()=>registration
  return Object.assign(h,{registration,cleanup})
}

test('open allows an untested version and verifies the Editor APIs',async()=>{
  const h=openFixture()
  h.plugin.manifest.version='99.0.0'
  const result=await h.invoke('open',{path:'new.md'})
  assert.equal(result.pluginVersion,'99.0.0')
  assert.equal(result.dedicatedEditor,true)
  assert.equal((await h.invoke('saved',{path:'new.md'},'saved')).saved,true)
})

test('open and read work without editing APIs or the view-opening API when an Editor is live',async()=>{
  const h=openFixture()
  delete h.plugin.openTldrFile
  delete h.editor.run
  delete h.editor.markHistoryStoppingPoint
  delete h.editor.bailToMark
  delete h.editor.store.getStoreSnapshot
  delete h.editor.store.applyDiff
  assert.equal((await h.invoke('doctor',{},'doctor')).supported,true)
  const result=await h.invoke('open',{path:'new.md'},'open')
  assert.equal((await h.invoke('saved',{path:'new.md'},'saved')).saved,true)
  assert.equal((await h.invoke('observe',{path:'new.md'},'observe')).shapes.length,1)
  await assert.rejects(h.invoke('apply',{path:'new.md',revision:result.revision,operations:[
    {op:'updateShapes',shapes:[{id:'shape:a',props:{color:'red'}}]},
  ]},'edit'),/editor.store.applyDiff/)
  await assert.rejects(h.invoke('script',{path:'new.md',revision:result.revision,
    code:'app.scriptExecuted = true'},'script'),/editor.store.applyDiff/)
  assert.equal(h.app.scriptExecuted,undefined)
  assert.equal((await h.invoke('state',{path:'new.md'},'state')).revision,result.revision)
})

test('open requires the view-opening API only when no Editor is live',async()=>{
  const h=openFixture()
  delete h.plugin.currTldrawEditor
  delete h.plugin.openTldrFile
  await assert.rejects(h.invoke('open',{path:'new.md'}),/plugin.openTldrFile/)
  assert.equal(h.access.sessionsFor(h.app).has('new.md'),false)
})

test('open reports missing core Editor APIs and releases the session',async()=>{
  const h=openFixture()
  delete h.editor.getCurrentPageId
  await assert.rejects(h.invoke('open',{path:'new.md'}),/editor.getCurrentPageId/)
  assert.deepEqual(h.cleanup,['editor','registration','container'])
  assert.equal(h.access.sessionsFor(h.app).has('new.md'),false)
})

test('open cleans up an incompatible registration and preserves the API error',async()=>{
  const h=openFixture()
  delete h.registration.syncToMain
  await assert.rejects(h.invoke('open',{path:'new.md'}),/registration.syncToMain/)
  assert.deepEqual(h.cleanup,['registration','container'])
  assert.equal(h.access.sessionsFor(h.app).has('new.md'),false)
})

test('batch checks every requested SDK method before applying any edits',()=>{
  const h=setup(), before=h.access.revision(h.editor)
  assert.throws(()=>h.access.batch(h.app,'a.md',[
    {method:'updateShapes',args:[[{id:'shape:a',props:{color:'red'}}]]},
    {method:'rotateShapesBy',args:[['shape:a'],1]},
  ],before),/editor.rotateShapesBy/)
  assert.equal(h.access.revision(h.editor),before)
})

test('preview reports a missing export API without changing records',async()=>{
  const h=setup(), before=h.access.revision(h.editor)
  await assert.rejects(h.invoke('preview',{path:'a.md',output:'unused.png'}),/editor.toImage/)
  assert.equal(h.access.revision(h.editor),before)
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

test('compact edit results count net additions, updates and removals without returning records',async()=>{
  const h=setup()
  h.values().push({id:'shape:removed',typeName:'shape',props:{color:'red'}})
  h.editor.createShapes=shapes=>h.values().push(...shapes)
  h.editor.deleteShapes=ids=>{
    for(let i=h.values().length-1;i>=0;i--) if(ids.includes(h.values()[i].id)) h.values().splice(i,1)
  }
  const result=h.access.batch(h.app,'a.md',[
    {method:'createShapes',args:[[{id:'shape:new',typeName:'shape',props:{color:'green'}}]]},
    {method:'updateShapes',args:[[{id:'shape:a',props:{color:'violet'}}]]},
    {method:'deleteShapes',args:[['shape:removed']]},
  ],h.access.revision(h.editor))
  assert.deepEqual(copy(result.changes),{added:1,updated:1,removed:1})
  assert.deepEqual(Object.keys(result).sort(),['changes','currentPageId','path','revision'])
  const state=await h.invoke('state',{path:'a.md'})
  assert.equal(state.revision,result.revision)
  assert.ok(state.records.some(r=>r.id==='shape:new'))
  assert.ok(!state.records.some(r=>r.id==='shape:removed'))
})

test('script summary counts document settings but ignores camera-only changes and no-op writes',()=>{
  const h=setup()
  h.editor.moveCamera=()=>{h.values().find(r=>r.typeName==='camera').x=123}
  const settings=h.access.script(h.app,'a.md','editor.updateDocumentSettings({gridSize:20});',h.access.revision(h.editor))
  assert.deepEqual(copy(settings.changes),{added:0,updated:1,removed:0})
  const camera=h.access.script(h.app,'a.md','editor.moveCamera();editor.updateDocumentSettings({gridSize:20});',settings.revision)
  assert.deepEqual(copy(camera.changes),{added:0,updated:0,removed:0})
  assert.equal(camera.revision,settings.revision)
})

test('dispatch returns compact saved results by default and full records on request',async()=>{
  const h=setup(), revision=h.access.revision(h.editor)
  const args={path:'a.md',revision,code:';'}
  const compact=await h.invoke('script',args,'compact')
  assert.equal(compact.persistence.saved,true)
  assert.equal('records' in compact,false)
  assert.deepEqual(copy(compact.changes),{added:0,updated:0,removed:0})
  assert.deepEqual(copy(await h.invoke('script',args,'compact')),copy(compact))
  const full=await h.invoke('script',{...args,full:true},'full')
  assert.ok(full.records.length)
  assert.equal(full.persistence.saved,true)
  assert.equal(full.revision,compact.revision)
  assert.deepEqual(copy(full.changes),copy(compact.changes))
})

test('observe returns scoped text, page bounds, touching bindings and revision-pinned pagination',async()=>{
  const h=setup()
  h.values().find(r=>r.id==='shape:a').type='geo'
  h.values().push({id:'shape:b',typeName:'shape',type:'text',props:{}},
    {id:'binding:ab',typeName:'binding',fromId:'shape:a',toId:'shape:b',type:'arrow',props:{terminal:'end'}})
  h.editor.getCurrentPageShapeIds=()=>['shape:b','shape:a']
  h.editor.getShapePageBounds=id=>({x:id==='shape:a'?10:100,y:20,w:30,h:40})
  h.editor.getShapeUtil=()=>({getText:shape=>shape.id==='shape:a'?'Exact label':'Other'})
  const before=h.access.revision(h.editor)
  const first=await h.invoke('observe',{path:'a.md',limit:1},'first')
  assert.equal(first.total,2)
  assert.equal(first.shapes[0].id,'shape:a')
  assert.equal(first.shapes[0].text,'Exact label')
  assert.equal(first.shapes[0].bounds.x,10)
  assert.equal(first.bindings[0].toId,'shape:b')
  assert.equal(first.nextOffset,1)
  assert.equal(h.access.revision(h.editor),before)
  const next=await h.invoke('observe',{path:'a.md',limit:1,offset:1,revision:first.revision,pageId:first.currentPageId},'next')
  assert.equal(next.shapes[0].id,'shape:b')
  assert.equal(next.nextOffset,null)
  const crop=await h.invoke('observe',{path:'a.md',bounds:{x:0,y:0,w:50,h:100}},'crop')
  assert.equal(crop.total,1)
  h.editor.getCurrentPageId=()=> 'page:other'
  await assert.rejects(h.invoke('observe',{path:'a.md',offset:1,revision:first.revision,pageId:first.currentPageId},'page-switch'),/Current page changed/)
  h.editor.getCurrentPageId=()=> 'page:a'
  h.editor.updateDocumentSettings({name:'concurrent edit'})
  await assert.rejects(h.invoke('observe',{path:'a.md',offset:1,revision:first.revision,pageId:first.currentPageId},'stale'),/Revision conflict/)
  const job=JSON.parse(h.api.poll(h.app,'stale'))
  assert.equal(job.failure.code,'REVISION_CONFLICT')
  assert.equal(job.failure.outcome,'not_applied')
})

test('named operations validate the whole batch before any edit and use existing persistence checks',async()=>{
  const h=setup(), before=h.access.revision(h.editor)
  await assert.rejects(h.invoke('apply',{path:'a.md',revision:before,operations:[
    {op:'updateShapes',shapes:[{id:'shape:a',props:{color:'red'}}]},
    {op:'alignShapes',ids:['shape:a'],alignment:'invalid'},
  ]},'invalid'),/Invalid alignment/)
  assert.equal(h.access.revision(h.editor),before)
  h.app.vault.read=async()=>h.markdown(copy(h.values()))
  const result=await h.invoke('apply',{path:'a.md',revision:before,operations:[
    {op:'updateShapes',shapes:[{id:'shape:a',props:{color:'red'}}]},
  ]},'valid')
  assert.equal(result.persistence.saved,true)
  assert.equal(result.changes.updated,1)
})

test('save failure reports applied revision and retains the result for recovery',async()=>{
  const h=setup()
  h.app.vault.read=async()=>{throw new Error('disk unavailable')}
  const args={path:'a.md',revision:h.access.revision(h.editor),operations:[
    {op:'updateShapes',shapes:[{id:'shape:a',props:{color:'red'}}]},
  ]}
  await assert.rejects(h.invoke('apply',args,'save-failure'),/disk unavailable/)
  const job=JSON.parse(h.api.poll(h.app,'save-failure'))
  assert.equal(job.failure.code,'SAVE_UNCONFIRMED')
  assert.equal(job.failure.outcome,'applied')
  assert.equal(job.failure.details.revision,h.access.revision(h.editor))
  assert.equal(JSON.parse(h.api.dispatch(h.app,'apply',args,'save-failure')).status,'failed')
})


test('apply can pin the current page even when a page switch leaves the revision unchanged',async()=>{
  const h=setup(), before=h.access.revision(h.editor)
  await assert.rejects(h.invoke('apply',{path:'a.md',revision:before,pageId:'page:old',
    operations:[{op:'updateShapes',shapes:[{id:'shape:a',props:{color:'red'}}]}]},'wrong-page'),/Current page changed/)
  assert.equal(h.access.revision(h.editor),before)
  assert.equal(JSON.parse(h.api.poll(h.app,'wrong-page')).failure.code,'PAGE_CONFLICT')
})

function withPendingGui(h) {
  let pending
  const trace=[]
  const peer={isSynchronizingToMain:()=>true,store:{listen:()=>{
    trace.push('gui')
    if(pending){ h.editor.updateShapes([pending]); pending=null }
    return ()=>{}
  }}}
  const inactive={isSynchronizingToMain:()=>false,store:{listen:()=>{throw new Error('Read-only instance must not publish edits')}}}
  const plugin={manifest:{version:'1.32.0'},tlDataDocumentStoreManager:{storesManager:{storeGroupMap:new Map([
    ['a.md',{instances:[inactive,peer,{store:h.editor.store,isSynchronizingToMain:()=>true}],main:{store:{listen:()=>{
      trace.push('main'); h.setDisk(h.values()); return ()=>{}
    }}}}],
  ])}}}
  h.app.plugins.getPlugin=()=>plugin
  return {queue:change=>{pending=change},trace}
}

test('pending GUI notifications are reconciled before revision checking, not after editing',async()=>{
  const h=setup(), gui=withPendingGui(h), old=h.access.revision(h.editor)
  gui.queue({id:'shape:a',props:{color:'green'}})
  await assert.rejects(h.invoke('apply',{path:'a.md',revision:old,operations:[
    {op:'updateShapes',shapes:[{id:'shape:a',props:{color:'red'}}]},
  ]},'pending-gui'),/Revision conflict/)
  assert.equal(h.editor.getShape('shape:a').props.color,'green')
  assert.equal(JSON.parse(h.api.poll(h.app,'pending-gui')).failure.code,'REVISION_CONFLICT')
  assert.ok(gui.trace.indexOf('gui')<gui.trace.indexOf('main'))
})

test('state and observe include pending GUI edits and expose parent-local positions',async()=>{
  const h=setup(), gui=withPendingGui(h)
  h.editor.getShapePageBounds=()=>({x:150,y:260,w:80,h:40})
  h.editor.getShapeUtil=()=>({getText:()=>''})
  gui.queue({id:'shape:a',x:50,y:60,props:{color:'green'}})
  const observed=await h.invoke('observe',{path:'a.md'},'pending-observe')
  assert.equal(observed.shapes[0].props.color,'green')
  assert.deepEqual(copy(observed.shapes[0].localPosition),{x:50,y:60})
  assert.equal(observed.shapes[0].bounds.x,150)
  gui.queue({id:'shape:a',props:{color:'orange'}})
  const current=await h.invoke('state',{path:'a.md'},'pending-state')
  assert.equal(current.records.find(r=>r.id==='shape:a').props.color,'orange')
})

test('a change during persistence cannot turn a superseded edit into successful completion',async()=>{
  const h=setup(), before=h.access.revision(h.editor)
  let changed=false
  h.app.vault.read=async()=>{
    if(!changed){changed=true; h.editor.updateShapes([{id:'shape:a',props:{color:'green'}}])}
    return h.markdown(copy(h.values()))
  }
  await assert.rejects(h.invoke('apply',{path:'a.md',revision:before,operations:[
    {op:'updateShapes',shapes:[{id:'shape:a',props:{color:'red'}}]},
  ]},'save-conflict'),/changed while saving/)
  const receipt=JSON.parse(h.api.poll(h.app,'save-conflict'))
  assert.equal(receipt.failure.code,'SAVE_CONFLICT')
  assert.equal(receipt.failure.outcome,'applied')
  assert.notEqual(receipt.failure.details.revision,receipt.failure.details.actualRevision)
  assert.equal(h.editor.getShape('shape:a').props.color,'green')
})

test('preview detects GUI notifications queued during asynchronous export',async()=>{
  const h=setup(), gui=withPendingGui(h), dir=fs.mkdtempSync(path.join(os.tmpdir(),'bridge-peer-preview-'))
  const output=path.join(dir,'existing.png');fs.writeFileSync(output,'original')
  h.editor.toImage=async()=>{
    gui.queue({id:'shape:a',props:{color:'green'}})
    return {blob:{arrayBuffer:async()=>Buffer.from('stale')},width:1,height:1}
  }
  try {
    await assert.rejects(h.invoke('preview',{path:'a.md',output},'pending-preview'),/Revision conflict/)
    assert.equal(fs.readFileSync(output,'utf8'),'original')
  } finally {fs.rmSync(dir,{recursive:true,force:true})}
})
