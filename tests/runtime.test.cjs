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

test('saved receipts identify the persisted document revision, including changes during reads',async()=>{
  const h=setup()
  const first=await h.access.saved(h.app,'a.md')
  h.app.vault.read=async()=>{
    h.editor.updateDocumentSettings({name:'Changed during read'})
    return h.markdown(copy(h.values()))
  }
  const second=await h.access.saved(h.app,'a.md')
  assert.equal(second.revision,h.access.revision(h.editor))
  assert.notEqual(second.revision,first.revision)
})

test('save waits for document settings to reach Markdown',async()=>{
  const h=setup(), old=copy(h.values())
  h.editor.updateDocumentSettings({name:'Unsaved'})
  let reads=0
  h.app.vault.read=async()=>h.markdown(++reads===1?old:copy(h.values()))
  const receipt=await h.access.saved(h.app,'a.md')
  assert.equal(receipt.saved,true)
  assert.equal(receipt.revision,h.access.revision(h.editor))
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
    await assert.rejects(h.invoke('preview',{path:'a.md',format:'png',revision:h.access.revision(h.editor),output}),/Revision conflict during preview/)
    assert.equal(fs.readFileSync(output,'utf8'),'existing preview')
  } finally {fs.rmSync(dir,{recursive:true,force:true})}
})

test('apply preview saves and renders one revision; retained replay performs neither again',async()=>{
  const h=setup(), dir=fs.mkdtempSync(path.join(os.tmpdir(),'bridge-apply-preview-')),output=path.join(dir,'out.webp')
  let edits=0, renders=0, reads=0
  const update=h.editor.updateShapes
  h.editor.updateShapes=changes=>{edits++;update(changes)}
  h.app.vault.read=async()=>{reads++;return h.markdown(h.values())}
  const bytes=Buffer.from('RIFF1234WEBPencoded image')
  h.editor.toImage=async(ids,options)=>{
    renders++
    assert.equal(reads,1,'Persistence must be checked before rendering')
    assert.deepEqual(Array.from(ids),['shape:a'])
    assert.equal(options.scale,.8)
    return {blob:{type:'image/webp',arrayBuffer:async()=>bytes},width:200,height:100}
  }
  const args={path:'a.md',revision:h.access.revision(h.editor),pageId:'page:a',
    operations:[{op:'updateShapes',shapes:[{id:'shape:a',x:20}]}],preview:{output,scale:.8}}
  try {
    const result=await h.invoke('apply',args,'edit-preview')
    assert.notEqual(result.revision,args.revision)
    assert.equal(result.persistence.saved,true)
    assert.equal(result.revision,result.persistence.revision)
    assert.equal(result.revision,result.preview.revision)
    assert.equal(result.preview.sha256,require('node:crypto').createHash('sha256').update(bytes).digest('hex'))
    assert.equal(result.changes.updated,1)
    assert.deepEqual(fs.readFileSync(output),bytes)
    fs.writeFileSync(output,'replaced after export')
    assert.deepEqual(await h.invoke('apply',args,'edit-preview'),result)
    assert.deepEqual([edits,renders,reads],[1,1,1])
    assert.equal(fs.readFileSync(output,'utf8'),'replaced after export')
    assert.throws(()=>h.api.dispatch(h.app,'apply',{...args,preview:{output,scale:1}},'edit-preview'),/already used/)
  } finally {fs.rmSync(dir,{recursive:true,force:true})}
})

test('direct callers cannot attach edit previews to other mutation actions',async()=>{
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'bridge-unsupported-preview-')),output=path.join(dir,'out.webp')
  try {
    for(const action of ['batch','script','insert-image','language-checkpoint']) {
      const h=setup(),before=copy(h.values())
      h.app.vault.read=async()=>h.markdown(h.values())
      h.editor.toImage=async()=>{throw new Error('Unexpected export')}
      await assert.rejects(h.invoke(action,{path:'a.md',revision:h.access.revision(h.editor),
        operations:[{method:'updateShapes',args:[[{id:'shape:a',x:20}]]}],
        code:'editor.updateDocumentSettings({gridSize:999})',preview:{output}},action),/only supported by apply/)
      const failure=JSON.parse(h.api.poll(h.app,action)).failure
      assert.equal(failure.code,'INVALID_INPUT')
      assert.equal(failure.outcome,'not_applied')
      assert.deepEqual(copy(h.values()),before)
      assert.equal(fs.existsSync(output),false)
    }
  } finally {fs.rmSync(dir,{recursive:true,force:true})}
})

test('invalid edit preview configuration fails before editing with an available export API',async()=>{
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'bridge-apply-invalid-')),output=path.join(dir,'out.webp')
  try {
    for(const preview of [null,[],{}, {output,revision:'override'}, {output,format:'jpeg'},
      {output,format:'png',quality:.9}, {output,scale:0}, {output,ids:[]},
      {output,ids:['shape:a'],bounds:{}}, {output,bounds:{x:0,y:0,w:0,h:1}},
      {output:path.join(dir,'missing','out.webp')},{output:dir}]) {
      const h=setup(),before=copy(h.values())
      h.editor.toImage=async()=>{throw new Error('Unexpected export')}
      await assert.rejects(h.invoke('apply',{path:'a.md',revision:h.access.revision(h.editor),
        operations:[{op:'updateShapes',shapes:[{id:'shape:a',x:20}]}],preview}))
      assert.deepEqual(copy(h.values()),before)
      const failure=JSON.parse(h.api.poll(h.app,'job')).failure
      assert.equal(failure.code,'INVALID_INPUT')
      assert.equal(failure.outcome,'not_applied')
    }
  } finally {fs.rmSync(dir,{recursive:true,force:true})}
})

test('valid edit preview configuration with a missing export API fails before editing',async()=>{
  const h=setup(),dir=fs.mkdtempSync(path.join(os.tmpdir(),'bridge-apply-no-export-'))
  const before=copy(h.values())
  try {
    await assert.rejects(h.invoke('apply',{path:'a.md',revision:h.access.revision(h.editor),
      operations:[{op:'updateShapes',shapes:[{id:'shape:a',x:20}]}],
      preview:{output:path.join(dir,'out.webp')}}),/editor.toImage/)
    const failure=JSON.parse(h.api.poll(h.app,'job')).failure
    assert.equal(failure.code,'TLDRAW_UNSUPPORTED')
    assert.equal(failure.outcome,'not_applied')
    assert.deepEqual(copy(h.values()),before)
  } finally {fs.rmSync(dir,{recursive:true,force:true})}
})

for(const kind of ['stale','page','save','save-conflict','render','selection','during-render','write']) {
  test(`apply preview recovers without reapplying after ${kind} failure`,async()=>{
    const h=setup(),dir=fs.mkdtempSync(path.join(os.tmpdir(),'bridge-apply-fail-')),output=path.join(dir,'out.webp')
    fs.writeFileSync(output,'existing preview')
    let edits=0,renders=0
    const update=h.editor.updateShapes
    h.editor.updateShapes=changes=>{edits++;update(changes)}
    h.app.vault.read=async()=>{
      if(kind==='save')throw new Error('disk unavailable')
      if(kind==='save-conflict')h.editor.updateDocumentSettings({gridSize:30})
      return h.markdown(h.values())
    }
    h.editor.toImage=async()=>{
      renders++
      if(kind==='render')throw new Error('encoder failed')
      if(kind==='during-render')h.editor.updateDocumentSettings({gridSize:40})
      if(kind==='write')fs.mkdirSync(output+'.dir')
      return {blob:{type:'image/webp',arrayBuffer:async()=>Buffer.from('RIFF1234WEBPencoded image')},width:1,height:1}
    }
    const args={path:'a.md',revision:kind==='stale'?'old':h.access.revision(h.editor),
      pageId:kind==='page'?'page:other':'page:a',
      operations:[{op:'updateShapes',shapes:[{id:'shape:a',x:20}]}],
      preview:{output:kind==='write'?output+'.dir':output,...(kind==='selection'?{ids:['shape:missing']}:{})}}
    try {
      await assert.rejects(h.invoke('apply',args,'failed-edit'))
      const receipt=JSON.parse(h.api.poll(h.app,'failed-edit')),failure=receipt.failure
      if(['stale','page'].includes(kind)) {
        assert.equal(edits,0)
        assert.equal(failure.outcome,'not_applied')
        assert.equal(renders,0)
      } else {
        assert.equal(edits,1)
        assert.equal(failure.outcome,'applied')
        if(kind.startsWith('save')) {
          assert.equal(failure.code,kind==='save'?'SAVE_UNCONFIRMED':'SAVE_CONFLICT')
          assert.equal(renders,0)
        } else {
          assert.equal(failure.code,'EDIT_PREVIEW_FAILED')
          assert.equal(failure.details.result.persistence.saved,true)
          assert.equal(failure.details.result.revision,failure.details.result.persistence.revision)
          assert.equal(failure.details.result.changes.updated,1)
          if(kind==='during-render')assert.equal(failure.details.cause.code,'REVISION_CONFLICT')
        }
      }
      assert.equal(fs.readFileSync(output,'utf8'),'existing preview')
      const counts=[edits,renders]
      await assert.rejects(h.invoke('apply',args,'failed-edit'))
      assert.deepEqual([edits,renders],counts)
      assert.deepEqual(JSON.parse(h.api.poll(h.app,'failed-edit')),receipt)
    } finally {fs.rmSync(dir,{recursive:true,force:true})}
  })
}

test('unchanged preview writes bytes tagged with the captured revision',async()=>{
  const h=setup(), dir=fs.mkdtempSync(path.join(os.tmpdir(),'bridge-preview-')),output=path.join(dir,'out.png')
  h.editor.toImage=async(ids,options)=>{
    assert.equal(options.format,'png')
    assert.equal(options.quality,undefined)
    return {blob:{arrayBuffer:async()=>Buffer.from('image')},width:1,height:1}
  }
  try {
    const before=h.access.revision(h.editor)
    const result=await h.invoke('preview',{path:'a.md',format:'png',output})
    assert.equal(result.revision,before)
    assert.equal(result.sha256,require('node:crypto').createHash('sha256').update(fs.readFileSync(output)).digest('hex'))
    assert.equal(result.format,'png')
    assert.equal(fs.readFileSync(output,'utf8'),'image')
  } finally {fs.rmSync(dir,{recursive:true,force:true})}
})

test('WebP default and explicit export pass quality and selection to SDK',async()=>{
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'bridge-webp-')),output=path.join(dir,'out.webp')
  const bytes=Buffer.from('RIFF1234WEBPencoded image')
  try {
    for(const format of [undefined,'webp'])for(const quality of [undefined,0,.7,1]){
      const h=setup(),before=h.access.revision(h.editor)
      assert.equal((await h.invoke('capabilities',{},'caps')).preview.defaultFormat,'webp')
      h.editor.toImage=async(ids,options)=>{
        assert.deepEqual(Array.from(ids),['shape:a'])
        assert.equal(options.format,'webp')
        assert.equal(options.quality,quality??.9)
        assert.equal(options.scale,2)
        return {blob:{type:'image/webp',arrayBuffer:async()=>bytes},width:200,height:100}
      }
      const result=await h.invoke('preview',{path:'a.md',ids:['shape:a'],scale:2,...(format===undefined?{}:{format}),...(quality===undefined?{}:{quality}),output})
      assert.equal(result.sha256,require('node:crypto').createHash('sha256').update(bytes).digest('hex'))
      assert.equal(result.format,'webp')
      assert.equal(result.revision,before)
      assert.equal(h.access.revision(h.editor),before)
      assert.deepEqual(fs.readFileSync(output),bytes)
    }
  } finally {fs.rmSync(dir,{recursive:true,force:true})}
})

test('WebP encoder fallback, corrupt bytes and revision conflicts preserve the output',async()=>{
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'bridge-webp-fail-')),output=path.join(dir,'out.webp')
  fs.writeFileSync(output,'original')
  try {
    for(const kind of ['mime','bytes','revision']){
      const h=setup()
      h.editor.toImage=async()=>({blob:{type:kind==='mime'?'image/png':'image/webp',arrayBuffer:async()=>{
        if(kind==='revision')h.editor.updateDocumentSettings({name:'Changed'})
        return Buffer.from(kind==='bytes'?'invalid image':'RIFF1234WEBPencoded image')
      }},width:1,height:1})
      await assert.rejects(h.invoke('preview',{path:'a.md',format:'webp',output}),kind==='revision'?/Revision conflict/:/WebP export failed/)
      assert.equal(fs.readFileSync(output,'utf8'),'original')
    }
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
    await h.invoke('preview',{path:'a.md',format:'png',part:'detail',scale:3,output})
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
      {scale:0},{scale:5},{scale:NaN},{format:'jpeg'},{format:null},
      {quality:NaN},{format:'png',quality:.8},{format:'webp',quality:NaN},
      {format:'webp',quality:true},{format:'webp',quality:-1},{format:'webp',quality:2}]){
      const h=setup()
      h.editor.toImage=async()=>{throw new Error('Unexpected render')}
      await assert.rejects(h.invoke('preview',{path:'a.md',format:'png',output,...args}),error=>!error.message.includes('Unexpected render'))
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
    const result=await h.invoke('preview',{path:'a.md',format:'png',bounds,output})
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

for (const [name, thrown, expectedCode] of [
  ['throwing code getter', '{message:"original failure",get code(){throw new Error("code getter failed")}}', 'SCRIPT_FAILED'],
  ['throwing Proxy metadata', 'new Proxy({message:"original failure"},{get(target,key){if(key==="code")throw new Error("code trap failed");return Reflect.get(target,key)}})', 'SCRIPT_FAILED'],
  ['code read once', '{message:"original failure",get code(){if(++app.codeReads>1)throw new Error("code read twice");return "SCRIPT_RESULT_INVALID"}}', 'SCRIPT_RESULT_INVALID'],
]) {
  test(`${name} preserves script failure, rollback and retained replay`,async()=>{
    const h=setup(), before=copy(h.values()), revision=h.access.revision(h.editor)
    h.app.externalSideEffects=0
    h.app.codeReads=0
    const args={path:'a.md',revision,code:
      `app.externalSideEffects++;editor.updateDocumentSettings({gridSize:999});throw ${thrown}`}
    await assert.rejects(h.invoke('script',args,'metadata-failure'),/original failure/)
    const receipt=JSON.parse(h.api.poll(h.app,'metadata-failure'))
    assert.equal(receipt.failure.code,expectedCode)
    assert.equal(receipt.failure.message,'original failure')
    assert.equal(receipt.failure.outcome,'unknown')
    assert.equal(receipt.failure.details.storeRevision,revision)
    assert.match(receipt.failure.details.recovery,/outside the Store/)
    assert.deepEqual(copy(h.values()),before)
    assert.equal(h.app.externalSideEffects,1)
    if (name==='code read once') assert.equal(h.app.codeReads,1)
    await assert.rejects(h.invoke('script',args,'metadata-failure'),/original failure/)
    assert.deepEqual(JSON.parse(h.api.poll(h.app,'metadata-failure')),receipt)
    assert.equal(h.app.externalSideEffects,1)
    assert.equal((await h.invoke('doctor',{},'after-metadata-failure')).vault,'test')
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
  const h = openFixture()
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
      plugin.currTldrawEditor=h.editor
      const leaf={view:{file}}
      h.app.workspace.getLeavesOfType=()=>[leaf]
      return leaf
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
  const replay=await h.invoke('create',{path:'Drawings/project-plan.md'},'create-plan')
  assert.equal(replay.revision,result.revision)
  assert.equal(h.calls.length,1)
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
  for(const name of ['createTldrFile','getFontOverrides']) {
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
    constructor:function Editor(options) {return {...h.editor,isDisposed:false,store:options.store}},
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

test('create reuses a live Editor without opening or selecting a GUI tab',async()=>{
  const h=createFixture(), selected={id:'user-tab'}
  h.app.workspace.activeLeaf=selected
  h.app.workspace.setActiveLeaf=()=>{throw new Error('Must not move focus')}
  delete h.plugin.openTldrFile
  const result=await h.invoke('create',{path:'plan.md'})
  assert.equal(result.persistence.saved,true)
  assert.equal(h.calls.length,1)
  assert.equal(h.app.workspace.activeLeaf,selected)
})

test('create waits for metadata recognition without opening a GUI tab or creating twice',async()=>{
  const h=createFixture()
  let recognized=false, checks=0
  h.plugin.isTldrawFile=()=>{checks++;return recognized}
  h.plugin.openTldrFile=()=>{throw new Error('Must not open a GUI tab')}
  h.api.dispatch(h.app,'create',{path:'plan.md'},'metadata')
  setTimeout(()=>{recognized=true},10)
  await new Promise(resolve=>setTimeout(resolve,150))
  const job=JSON.parse(h.api.poll(h.app,'metadata'))
  assert.equal(job.status,'complete',job.error)
  assert.equal(job.result.persistence.saved,true)
  assert.ok(checks>=2)
  assert.equal(h.calls.length,1)
})

test('initialization opens one tab and preserves a user tab switch while waiting',async()=>{
  const h=createFixture(), selected={id:'user-tab'}, leaf={id:'initialization-tab'}
  delete h.plugin.currTldrawEditor
  let opens=0
  h.plugin.openTldrFile=async()=>{
    opens++
    h.plugin.currTldrawEditor=h.editor
    h.app.workspace.activeLeaf=selected
    return leaf
  }
  h.app.workspace.setActiveLeaf=()=>{throw new Error('Must not restore focus')}
  const result=await h.invoke('create',{path:'plan.md'})
  assert.equal(result.bootstrap,'opened-existing-view')
  assert.equal(opens,1)
  assert.equal(h.app.workspace.activeLeaf,selected)
})

test('closing an initialization tab before readiness stops without reopening and retains the note',async()=>{
  const h=createFixture()
  delete h.plugin.currTldrawEditor
  let opens=0
  h.plugin.openTldrFile=async()=>{opens++;return {id:'closed-tab'}}
  h.app.workspace.getLeavesOfType=()=>[]
  await assert.rejects(h.invoke('create',{path:'plan.md'}),/Created plan.md.*initialization tab was closed.*Use open/)
  assert.equal(opens,1)
  assert.ok(h.files.has('plan.md'))
  assert.equal(h.access.sessionsFor(h.app).has('plan.md'),false)
})

test('closing the seed after capture does not break initialization or subsequent edits',async()=>{
  const h=openFixture(), originalRead=h.app.vault.read
  const updateShapes=h.editor.updateShapes
  h.editor.updateShapes=changes=>{updateShapes(changes);h.setDisk(h.values())}
  let reads=0
  h.app.vault.read=async file=>{
    if(++reads===2) {
      h.editor.isDisposed=true
      h.editor.getContainer=()=>{throw new Error('Disposed seed accessed')}
      h.editor.shapeUtils=undefined
      h.editor.bindingUtils=undefined
      h.editor.assetUtils=undefined
      h.editor.root=undefined
      delete h.plugin.currTldrawEditor
    }
    return originalRead(file)
  }
  const result=await h.invoke('open',{path:'new.md'},'open')
  assert.equal(result.guiEditorDisposed,true)
  const applied=await h.invoke('apply',{path:'new.md',revision:result.revision,operations:[
    {op:'updateShapes',shapes:[{id:'shape:a',props:{color:'red'}}]},
  ]},'edit')
  assert.equal(applied.persistence.saved,true)
})

test('initialization rereads Markdown after awaiting the GUI bootstrap',async()=>{
  const h=openFixture(), read=h.app.vault.read
  let reads=0, registeredText
  h.app.vault.read=async file=>{
    if(++reads===2) {
      h.editor.updateDocumentSettings({name:'Saved while initializing'})
      h.setDisk(h.values())
    }
    return read(file)
  }
  h.plugin.tlDataDocumentStoreManager.register=(file,getText)=>{
    registeredText=getText()
    return h.registration
  }
  await h.invoke('open',{path:'new.md'})
  assert.match(registeredText,/Saved while initializing/)
})

test('a closed initialization window stops without registering or opening another tab',async()=>{
  const h=openFixture(), read=h.app.vault.read
  const document=h.editor.getContainer().ownerDocument
  document.defaultView={closed:false}
  let reads=0
  h.app.vault.read=async file=>{
    if(++reads===2) document.defaultView.closed=true
    return read(file)
  }
  h.plugin.openTldrFile=()=>{throw new Error('Must not reopen a window')}
  h.plugin.tlDataDocumentStoreManager.register=()=>{throw new Error('Must not register')}
  await assert.rejects(h.invoke('open',{path:'new.md'}),/initialization window was closed/)
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
  await assert.rejects(h.invoke('preview',{path:'a.md',format:'png',output:'unused.png'}),/editor.toImage/)
  assert.equal(h.access.revision(h.editor),before)
})

function imageFixture() {
  const h=setup()
  const document={createElement:type=>type==='img'?{
    naturalWidth:800,naturalHeight:400,
    decode:async()=>{if(h.decode) await h.decode()},
  }:{getContext:()=>({drawImage:()=>{h.drawn=true}}),toDataURL:(mime,quality)=>{
    h.encoding={mime,quality}
    return h.encodedSrc??'data:'+mime+';base64,'+Buffer.from('encoded').toString('base64')
  }}}
  h.editor.getContainer=()=>({ownerDocument:document})
  h.app.workspace.containerEl={ownerDocument:document}
  h.editor.createAssets=assets=>h.values().push(...copy(assets))
  h.editor.createShapes=shapes=>{
    h.values().push(...copy(shapes).map(shape=>({...shape,typeName:'shape'})))
    h.setDisk(h.values())
  }
  h.args={path:'a.md',revision:h.access.revision(h.editor),name:'photo.webp',
    src:'data:image/webp;base64,'+Buffer.from('RIFF\x04\0\0\0WEBP','binary').toString('base64'),
    shapeId:'shape:photo',x:40,y:60,width:320}
  return h
}

test('image insertion saves original PNG/WebP/JPEG bytes and replays without duplicates',async()=>{
  for(const mime of ['webp','jpeg','png']) {
    const h=imageFixture()
    if(mime==='jpeg') h.args.src='data:image/jpeg;base64,'+Buffer.from([255,216,255,224]).toString('base64')
    if(mime==='png') h.args.src='data:image/png;base64,iVBORw0KGgo='
    const result=await h.invoke('insert-image',h.args,'photo')
    assert.equal(result.shapeId,'shape:photo')
    assert.equal(result.width,320)
    assert.equal(result.height,160)
    assert.equal(result.mimeType,'image/'+mime)
    assert.equal(result.persistence.saved,true)
    assert.deepEqual(result.changes,{added:2,updated:0,removed:0})
    assert.equal(result.records,undefined)
    const shape=h.editor.getShape(result.shapeId)
    assert.equal(shape.parentId,'page:a')
    assert.equal(shape.x,40)
    assert.equal(shape.y,60)
    assert.equal(h.values().find(r=>r.id===result.assetId).props.src,h.args.src)
    assert.deepEqual(await h.invoke('insert-image',h.args,'photo'),result)
    assert.equal(h.values().filter(r=>r.typeName==='asset').length,1)
    assert.equal(h.drawn,undefined)
  }
})

test('image insertion supports natural dimensions, height-only scaling and an explicit parent',async()=>{
  for(const dimensions of [{}, {height:100}, {width:120,height:90}]) {
    const h=imageFixture()
    delete h.args.width
    const result=await h.invoke('insert-image',{...h.args,...dimensions,parentId:'shape:a',pageId:'page:a'})
    assert.equal(result.width,dimensions.width??(dimensions.height?dimensions.height*2:800))
    assert.equal(result.height,dimensions.height??400)
    assert.equal(h.editor.getShape(result.shapeId).parentId,'shape:a')
  }
})

test('unsupported/spoofed image types, decode errors and ID collisions leave the document unchanged',async()=>{
  for(const change of [
    {src:'data:image/gif;base64,R0lGODlh'},
    {src:'data:image/webp;base64,iVBORw0KGgo='},
    {width:0}, {x:true}, {shapeId:'shape:a'}, {parentId:'shape:missing'},
    {pageId:'page:other'}, {decode:async()=>{throw new Error('corrupt image')}},
  ]) {
    const h=imageFixture(), before=h.access.revision(h.editor)
    if(change.decode) h.decode=change.decode
    const {decode,...args}=change
    await assert.rejects(h.invoke('insert-image',{...h.args,...args}))
    assert.equal(h.access.revision(h.editor),before)
    assert.equal(h.values().some(r=>r.typeName==='asset'),false)
    assert.equal(JSON.parse(h.api.poll(h.app,'job')).failure.outcome,'not_applied')
  }
})

test('image-info reports source and embedded sizes without editing or requiring a session',async()=>{
  const h=imageFixture(), before=h.access.revision(h.editor)
  h.access.sessionsFor(h.app).clear()
  const report=await h.invoke('image-info',{name:h.args.name,src:h.args.src})
  assert.deepEqual(report.source,{mimeType:'image/webp',width:800,height:400,bytes:12})
  assert.deepEqual(report.output,{mimeType:'image/webp',width:800,height:400,bytes:12,dataUrlBytes:Buffer.byteLength(h.args.src)})
  assert.equal(report.transformed,false)
  assert.equal(h.access.revision(h.editor),before)
})

test('pixel resizing and WebP encoding require explicit options and report processed dimensions',async()=>{
  const h=imageFixture()
  const result=await h.invoke('insert-image',{...h.args,maxDimension:200,format:'webp',quality:.7})
  const asset=h.values().find(r=>r.id===result.assetId)
  assert.equal(asset.props.w,200)
  assert.equal(asset.props.h,100)
  assert.equal(result.image.source.width,800)
  assert.equal(result.image.output.width,200)
  assert.equal(result.image.transformed,true)
  assert.deepEqual(h.encoding,{mime:'image/webp',quality:.7})
  assert.equal(result.width,320) // Display dimensions do not control encoded pixels.
  const noUpscale=imageFixture()
  const info=await noUpscale.invoke('image-info',{name:noUpscale.args.name,src:noUpscale.args.src,maxDimension:1600})
  assert.equal(info.transformed,false)
  assert.equal(noUpscale.drawn,undefined)
})

test('size limits, unavailable encoders and animated transformations stop before insertion',async()=>{
  for(const kind of ['size','encoder','animation']) {
    const h=imageFixture(), before=h.access.revision(h.editor)
    let args={...h.args}
    if(kind==='size') args.maxBytes=1
    if(kind==='encoder') {args.format='webp';h.encodedSrc='data:image/png;base64,iVBORw0KGgo='}
    if(kind==='animation') {
      const bytes=Buffer.alloc(21)
      bytes.write('RIFF',0);bytes.write('WEBP',8);bytes.write('VP8X',12);bytes[20]=2
      args.src='data:image/webp;base64,'+bytes.toString('base64');args.maxDimension=200
    }
    await assert.rejects(h.invoke('insert-image',args),/exceeds maxBytes|cannot encode|Animated images/)
    assert.equal(h.access.revision(h.editor),before)
    assert.equal(h.values().some(r=>r.typeName==='asset'),false)
  }
})

test('image decoding cannot apply an insertion after a GUI edit or page switch',async()=>{
  for(const kind of ['revision','page']) {
    const h=imageFixture()
    h.decode=async()=>{
      if(kind==='revision') h.editor.updateDocumentSettings({name:'GUI edit'})
      else h.editor.getCurrentPageId=()=> 'page:other'
    }
    await assert.rejects(h.invoke('insert-image',h.args),/changed|Revision conflict/)
    assert.equal(h.values().some(r=>r.typeName==='asset'),false)
    assert.equal(h.editor.getShape('shape:photo'),undefined)
  }
})

test('failed image shape creation rolls back the newly created asset',async()=>{
  const h=imageFixture(), before=h.access.revision(h.editor)
  h.editor.createShapes=()=>{throw new Error('Invalid image shape')}
  await assert.rejects(h.invoke('insert-image',h.args),/Invalid image shape/)
  assert.equal(h.access.revision(h.editor),before)
  assert.equal(h.values().some(r=>r.typeName==='asset'),false)
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
  delete h.plugin.currTldrawEditor
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
    await assert.rejects(h.invoke('preview',{path:'a.md',format:'png',output},'pending-preview'),/Revision conflict/)
    assert.equal(fs.readFileSync(output,'utf8'),'original')
  } finally {fs.rmSync(dir,{recursive:true,force:true})}
})

function installStyles(h, editor = h.editor, next = 'solid') {
  const fill = { id: 'tldraw:fill', values: ['none','semi','solid','pattern','fill','lined-fill'], defaultValue: 'none' }
  const dash = { id: 'tldraw:dash', values: ['draw','solid'], defaultValue: 'draw' }
  editor.shapeUtils = {geo:{getDefaultProps:()=>({fill:'none',dash:'draw'})}}
  editor.styleProps = {geo:new Map([[fill,'fill'],[dash,'dash']])}
  editor.getStyleForNextShape = style => style === fill ? next : 'draw'
  return {fill,dash}
}

test('style-spec reads the specified session without edits, history marks or file reads',async()=>{
  const h=setup(), before=copy(h.values()), rev=h.access.revision(h.editor)
  const {fill}=installStyles(h)
  fill.values.push('custom')
  const other={...h.editor}
  installStyles(h,other,'pattern')
  h.access.sessionsFor(h.app).set('b.md',{path:'b.md',editor:other})
  h.app.vault.read=()=>{throw new Error('unexpected file read')}
  h.editor.markHistoryStoppingPoint=()=>{throw new Error('unexpected history change')}
  const a=await h.invoke('style-spec',{path:'a.md',shapeType:'geo'},'styles-a')
  const b=await h.invoke('style-spec',{path:'b.md',shapeType:'geo'},'styles-b')
  assert.equal(a.pluginVersion,'1.32.0')
  assert.equal(a.properties.status,'available')
  const props=a.properties.value
  assert.deepEqual(props.fill.values.value,['none','semi','solid','pattern','fill','lined-fill','custom'])
  assert.equal(props.fill.styleId.value,'tldraw:fill')
  assert.equal(props.fill.styleDefault.value,'none')
  assert.equal(props.fill.shapeDefault.value,'none')
  assert.equal(props.fill.nextShapeStyle.value,'solid')
  assert.equal(b.properties.value.fill.nextShapeStyle.value,'pattern')
  assert.equal(props.dash.values.status,'available')
  assert.equal(h.access.revision(h.editor),rev)
  assert.deepEqual(copy(h.values()),before)
  assert.ok((await h.invoke('capabilities',{},'style-caps')).actions.includes('style-spec'))
})

test('style-spec distinguishes unsupported, unavailable, empty and null fields',async()=>{
  const h=setup(), {fill,dash}=installStyles(h)
  fill.values=[]
  fill.defaultValue=null
  delete dash.values
  delete h.editor.getStyleForNextShape
  h.editor.shapeUtils.geo.getDefaultProps=()=>{throw new Error('defaults unavailable')}
  const props=(await h.invoke('style-spec',{path:'a.md',shapeType:'geo'},'fields')).properties.value
  assert.deepEqual(props.fill.values.value,[])
  assert.equal(props.fill.styleDefault.value,null)
  assert.equal(props.fill.styleDefault.status,'available')
  assert.equal(props.dash.values.status,'unsupported')
  assert.equal('value' in props.dash.values,false)
  assert.equal(props.fill.nextShapeStyle.status,'unavailable')
  assert.equal(props.fill.shapeDefault.status,'unavailable')
  assert.match(props.fill.shapeDefault.reason,/defaults unavailable/)
  delete h.editor.styleProps
  assert.equal((await h.invoke('style-spec',{path:'a.md',shapeType:'geo'},'mapping')).properties.status,'unavailable')
  for (const args of [{path:'missing.md',shapeType:'geo'}, {path:'a.md',shapeType:'missing'}, {shapeType:'geo'}]) {
    await assert.rejects(h.invoke('style-spec',args,JSON.stringify(args)))
  }
})

test('script results distinguish absence, null and falsy values in compact and full responses',async()=>{
  const h=setup(), revision=h.access.revision(h.editor)
  for (const full of [false,true]) {
    for (const [code,expected] of [[';', {hasValue:false}], ['return undefined',{hasValue:false}],
      ['return null',{hasValue:true,value:null}], ['return false',{hasValue:true,value:false}],
      ['return 0',{hasValue:true,value:0}], ['return ""',{hasValue:true,value:''}],
      ['return {value:42,text:"青😀",list:[true,null]}',{hasValue:true,value:{value:42,text:'青😀',list:[true,null]}}]]) {
      const args={path:'a.md',revision,code,full}, id=`result-${full}-${code}`
      const result=await h.invoke('script',args,id)
      assert.deepEqual(result.scriptResult,expected)
      assert.equal(result.persistence.saved,true)
      assert.equal('records' in result,full)
      assert.deepEqual(await h.invoke('script',args,id),result)
    }
  }
})

for (const code of ['return 1n','return ()=>{}','return Symbol("x")','return NaN','return Infinity',
  'return {value:undefined}','return [undefined]','return Array(2)','return new Date()',
  'return new Map()','return new (class extends Array {})()', 'return Object.setPrototypeOf([],null)',
  'const a={};a.self=a;return a',
  'return {get value(){app.getterCalled=true;throw new Error("getter ran")}}',
  'return {get then(){app.getterCalled=true;throw new Error("then getter ran")}}',
  'return {toJSON(){app.getterCalled=true;return 42}}',
  'return {[Symbol("key")]:1}', 'return Object.defineProperty({},"hidden",{value:1})',
  'return new Proxy({}, {ownKeys(){app.getterCalled=true;return []}})']) {
  test(`invalid script result rolls back and remains pollable: ${code}`,async()=>{
    const h=setup(), before=copy(h.values()), revision=h.access.revision(h.editor)
    await assert.rejects(h.invoke('script',{path:'a.md',revision,
      code:'editor.updateDocumentSettings({gridSize:999});'+code},'bad-result'))
    const receipt=JSON.parse(h.api.poll(h.app,'bad-result'))
    assert.equal(receipt.failure.code,'SCRIPT_RESULT_INVALID')
    assert.equal(receipt.failure.outcome,'unknown')
    assert.equal(receipt.failure.details.storeRevision,revision)
    assert.deepEqual(copy(h.values()),before)
    assert.equal(h.app.getterCalled,undefined)
    assert.equal((await h.access.saved(h.app,'a.md')).saved,true)
  })
}

test('script result limits count JSON UTF-8 bytes and container depth with rollback',async()=>{
  const h=setup(), revision=h.access.revision(h.editor)
  for(const expression of ['"a".repeat(65534)', '"青".repeat(21844)+"aa"', '"\\u0000".repeat(10922)+"aa"',
    'Array.from({length:32}).reduce(a=>[a],null)']) {
    const result=await h.invoke('script',{path:'a.md',revision,code:`return ${expression}`},expression)
    assert.equal(result.persistence.saved,true)
  }
  for(const expression of ['"a".repeat(65535)', '"青".repeat(21845)', '"\\u0000".repeat(10923)',
    'Array.from({length:33}).reduce(a=>[a],null)', 'Array(10000000).fill(null)']) {
    await assert.rejects(h.invoke('script',{path:'a.md',revision,
      code:`editor.updateDocumentSettings({gridSize:999});return ${expression}`},expression))
    assert.equal(JSON.parse(h.api.poll(h.app,expression)).failure.code,'SCRIPT_RESULT_TOO_LARGE')
    assert.equal(h.access.revision(h.editor),revision)
  }
})

test('script results detach mutable references before persistence and preserve proto keys',async()=>{
  const h=setup(), revision=h.access.revision(h.editor)
  h.app.value={n:1}
  h.app.vault.read=async()=>{h.app.value.n=2;return h.markdown(h.values())}
  const args={path:'a.md',revision,code:'editor.updateDocumentSettings({gridSize:20}); return {ref:app.value,["__proto__"]:{safe:true}}'}
  const result=await h.invoke('script',args,'detached')
  assert.equal(result.changes.updated,1)
  assert.equal(result.scriptResult.value.ref.n,1)
  assert.deepEqual(result.scriptResult.value.__proto__,{safe:true})
  assert.equal(h.app.value.n,2)
  assert.deepEqual(await h.invoke('script',args,'detached'),result)
})

for (const conflict of [false,true]) {
  test(`save failure preserves script results and retained replay (conflict=${conflict})`,async()=>{
    const h=setup(), revision=h.access.revision(h.editor)
    h.app.vault.read=async()=>{
      if (!conflict) throw new Error('disk unavailable')
      h.editor.updateDocumentSettings({gridSize:30})
      return h.markdown(h.values())
    }
    const args={path:'a.md',revision,code:'editor.updateDocumentSettings({gridSize:20});return {value:42}'}
    await assert.rejects(h.invoke('script',args,'save-result'))
    const receipt=JSON.parse(h.api.poll(h.app,'save-result'))
    assert.equal(receipt.failure.code,conflict?'SAVE_CONFLICT':'SAVE_UNCONFIRMED')
    assert.equal(receipt.failure.outcome,'applied')
    assert.deepEqual(receipt.failure.details.scriptResult,{hasValue:true,value:{value:42}})
    assert.equal(receipt.failure.details.changes.updated,1)
    assert.notEqual(receipt.failure.details.revision,revision)
    await assert.rejects(h.invoke('script',args,'save-result'))
    assert.deepEqual(JSON.parse(h.api.poll(h.app,'save-result')),receipt)
  })
}

test('returned rejected Promises roll back without an unhandled rejection',async()=>{
  const h=setup(), revision=h.access.revision(h.editor)
  await assert.rejects(h.invoke('script',{path:'a.md',revision,
    code:'editor.updateDocumentSettings({gridSize:999});return Promise.reject(new Error("async failure"))'},'promise'),/must be synchronous/)
  assert.equal(h.access.revision(h.editor),revision)
})


test('style-spec isolates broken SDK fields from otherwise available values',async()=>{
  const h=setup(), {fill}=installStyles(h)
  Object.defineProperty(fill,'values',{get(){throw new Error('values unavailable')}})
  h.editor.shapeUtils.geo.getDefaultProps=()=>({fill:'none',other:undefined})
  const props=(await h.invoke('style-spec',{path:'a.md',shapeType:'geo'},'partial-sdk')).properties.value
  assert.equal(props.fill.values.status,'unavailable')
  assert.match(props.fill.values.reason,/values unavailable/)
  assert.equal(props.fill.shapeDefault.value,'none')
  assert.equal(props.fill.nextShapeStyle.value,'solid')
  assert.equal(props.dash.values.status,'available')
  h.editor.styleProps.geo=new Map()
  assert.deepEqual((await h.invoke('style-spec',{path:'a.md',shapeType:'geo'},'no-styles')).properties.value,{})
  delete h.editor.shapeUtils
  await assert.rejects(h.invoke('style-spec',{path:'a.md',shapeType:'geo'},'no-utils'),/editor.shapeUtils/)
  assert.equal(JSON.parse(h.api.poll(h.app,'no-utils')).failure.code,'TLDRAW_UNSUPPORTED')
})

test('language checkpoint uses revision, rollback, persistence and retained receipts without editing shapes',async()=>{
  const h=setup()
  h.values().push({id:'page:ja',typeName:'page',name:'日本語',meta:{}},
    {id:'shape:ja',typeName:'shape',parentId:'page:ja',type:'geo',props:{text:'確認'}})
  h.values().find(r=>r.id==='shape:a').parentId='page:a'
  const puts=[]
  h.editor.store.put=rs=>{puts.push(...rs);for(const r of rs){const i=h.values().findIndex(x=>x.id===r.id);h.values()[i]=r}}
  h.app.vault.read=async()=>h.markdown(copy(h.values()))
  const beforeShapes=copy(h.values().filter(r=>r.typeName==='shape'))
  const checkpoint={diagramId:'overview',editingSourcePageId:'page:a',languages:{en:'page:a',ja:'page:ja'},targetLanguage:'ja',kind:'adopt',reviewed:true,reason:'Both pages inspected'}
  const result=await h.invoke('language-checkpoint',{path:'a.md',revision:h.access.revision(h.editor),checkpoint},'checkpoint')
  assert.equal(result.persistence.saved,true)
  assert.deepEqual(h.values().filter(r=>r.typeName==='shape'),beforeShapes)
  const report=await h.invoke('language-status',{path:'a.md'},'status-after-checkpoint')
  assert.equal(report.diagrams.find(r=>r.language==='ja').status,'current')
  const duplicate=JSON.parse(h.api.poll(h.app,'checkpoint'));assert.equal(duplicate.result.revision,result.revision)
  const before=h.access.revision(h.editor)
  await assert.rejects(h.invoke('language-checkpoint',{path:'a.md',revision:'stale',checkpoint},'stale-checkpoint'),/Revision conflict/)
  assert.equal(h.access.revision(h.editor),before)
  h.values().find(r=>r.id==='shape:ja').props.text='独立した変更'
  const changed=h.access.revision(h.editor)
  await assert.rejects(h.invoke('language-checkpoint',{path:'a.md',revision:changed,checkpoint:{...checkpoint,kind:'layout'}},'invalid-layout'),/Layout checkpoint cannot accept content changes/)
  assert.equal(h.access.revision(h.editor),changed)
})

function languageHarness() {
  const h=setup()
  h.values().find(r=>r.id==='shape:a').parentId='page:a'
  for(const name of ['ja','fr','workflow-en','workflow-ja']) {
    h.values().push({id:'page:'+name,typeName:'page',name,meta:{}},
      {id:'shape:'+name,typeName:'shape',parentId:'page:'+name,type:'geo',props:{text:name}})
  }
  h.editor.store.put=rs=>{for(const r of rs){const i=h.values().findIndex(x=>x.id===r.id);h.values()[i]=r}}
  h.app.vault.read=async()=>h.markdown(copy(h.values()))
  let sequence=0
  h.checkpoint=async checkpoint=>h.invoke('language-checkpoint',{
    path:'a.md',revision:h.access.revision(h.editor),checkpoint:{kind:'adopt',reviewed:true,reason:'Inspected corresponding fixture pages',...checkpoint}
  },'language-check-'+(++sequence))
  h.review=async()=>h.invoke('language-status',{path:'a.md'},'language-report-'+(++sequence))
  h.group=name=>h.values().find(r=>r.typeName==='document').meta.multilingualDiagrams[name]
  return h
}

test('valid diagram and language keys do not collide with inherited object properties',async()=>{
  const h=languageHarness()
  await h.checkpoint({diagramId:'toString',editingSourcePageId:'page:a',languages:{en:'page:a',ja:'page:ja'},targetLanguage:'ja'})
  assert.equal((await h.review()).diagrams.find(r=>r.language==='ja').status,'current')
  await h.checkpoint({diagramId:'valueOf',editingSourcePageId:'page:workflow-en',languages:{en:'page:workflow-en',toString:'page:workflow-ja'},targetLanguage:'toString'})
  const report=await h.review()
  assert.equal(report.errors.length,0)
  assert.equal(report.diagrams.find(r=>r.diagramId==='valueOf'&&r.language==='toString').status,'current')
  delete h.group('valueOf').checkpoints.toString
  assert.equal((await h.review()).diagrams.find(r=>r.diagramId==='valueOf'&&r.language==='toString').status,'untracked')
})

test('three-language handoff retains third-language review and isolates other diagrams',async()=>{
  const h=languageHarness()
  const overview={diagramId:'overview',editingSourcePageId:'page:a',languages:{en:'page:a',ja:'page:ja',fr:'page:fr'}}
  await h.checkpoint({...overview,targetLanguage:'ja'})
  await h.checkpoint({...overview,targetLanguage:'fr'})
  const workflow={diagramId:'workflow',editingSourcePageId:'page:workflow-en',languages:{en:'page:workflow-en',ja:'page:workflow-ja'},targetLanguage:'ja'}
  await h.checkpoint(workflow)
  const protectedGroup=copy(h.group('workflow'))
  const protectedRecords=copy(h.values().filter(r=>r.id.includes('workflow')))
  const jaSource={...overview,editingSourcePageId:'page:ja'}
  // Simulate a reviewed content update and explicit handoff to Japanese.
  h.values().find(r=>r.id==='shape:a').props.text='Approve'
  h.values().find(r=>r.id==='shape:ja').props.text='承認'
  await h.checkpoint({...jaSource,targetLanguage:'en',kind:'translation'})
  let report=await h.review()
  const status=(diagram,lang)=>report.diagrams.find(r=>r.diagramId===diagram&&r.language===lang).status
  assert.equal(status('overview','ja'),'editing-source')
  assert.equal(status('overview','en'),'current')
  assert.equal(status('overview','fr'),'source-changed')
  assert.equal(report.requiresReview,true)
  assert.equal(status('workflow','ja'),'current')
  h.values().find(r=>r.id==='shape:fr').props.text='Approuver'
  await h.checkpoint({...jaSource,targetLanguage:'fr',kind:'translation'})
  report=await h.review()
  assert.equal(status('overview','fr'),'current')
  assert.equal(report.requiresReview,false)
  // Accepting one pair's layout must not acknowledge a different target.
  h.values().find(r=>r.id==='shape:ja').x=100
  h.values().find(r=>r.id==='shape:fr').x=120
  await h.checkpoint({...jaSource,targetLanguage:'fr',kind:'layout'})
  report=await h.review()
  assert.equal(status('overview','fr'),'current')
  assert.equal(status('overview','en'),'presentation-review')
  assert.equal(report.requiresReview,true)
  assert.equal(status('workflow','ja'),'current')
  assert.deepEqual(copy(h.group('workflow')),protectedGroup)
  assert.deepEqual(copy(h.values().filter(r=>r.id.includes('workflow'))),protectedRecords)
})
