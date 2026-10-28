'use strict'
const { test } = require('node:test')
const assert = require('node:assert/strict')
const fs = require('node:fs')
const os = require('node:os')
const path = require('node:path')
const loader = require('../src/obsidian_tldraw_bridge/runtime/loader.cjs')

function fixture(t) {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'bridge-loader-test-'))
  const filename = path.join(directory, 'bridge.cjs')
  t.after(() => { delete require.cache[filename]; fs.rmSync(directory, { recursive: true, force: true }) })
  const app = { documents: new Set(), events: [], calls: [], edits: 0 }
  function write(version) {
    fs.writeFileSync(filename, `
      const jobs = new Map();
      const pages = new Map();
      const documents = new Set();
      module.exports = {
        dispatch(app, action, args, id) {
          if (jobs.has(id)) {
            if(jobs.get(id).request !== JSON.stringify([action,args])) throw new Error('Job id already used for another request');
            return JSON.stringify(jobs.get(id));
          }
          if(app.busy) throw new Error('CLI job still running');
          const job = {id,request:JSON.stringify([action,args]),status:'complete'};
          app.calls.push({action,path:args.path,version:${version}});
          if(action==='doctor') job.result={documents:[...documents],version:${version}};
          if(action==='open' || action==='create') {
            if(app.blockOpen===args.path) throw new Error('Markdown document required');
            pages.set(args.path,args.currentPageId || 'page:first');
            documents.add(args.path);app.documents.add(args.path);app.events.push('open-${version}');job.result={version:${version}};
          }
          if(action==='state') {
            job.result={records:[{id:'document:preserved'}],revision:'unchanged',...(app.oldState ? {} : {currentPageId:pages.get(args.path)})};
          }
          if(action==='select') pages.set(args.path,args.page);
          if(action==='script') new Function('editor','app',args.code)({getCurrentPageId:()=>pages.get(args.path)},app);
          if(action==='close') {
            if(app.unsaved || app.blockClose===args.path) {job.status='failed';job.error='Timed out waiting for Markdown persistence';job.failure={code:'ENOENT',outcome:'not_applied'};}
            else {documents.delete(args.path);app.documents.delete(args.path);pages.delete(args.path);app.events.push('close-${version}');job.result={closed:true};}
          }
          if(action==='structured-failure') {job.status='failed';job.error='save unavailable';job.failure={code:'SAVE_UNCONFIRMED',message:job.error,outcome:'applied',details:{revision:'after-edit'}};}
          if(action==='edit') {app.edits++;job.result={version:${version},edits:app.edits,page:pages.get(args.path)};}
          jobs.set(id,job);return JSON.stringify(job);
        },
        poll(app,id) {if(!jobs.has(id))throw new Error('Unknown CLI job');return JSON.stringify(jobs.get(id));},
        forget(app,id) {return JSON.stringify({forgotten:jobs.delete(id)});}
      };
    `)
  }
  async function run(action, args = {}, id = 'request-' + Math.random()) {
    loader.dispatch(app, filename, action, args, id)
    for(let i=0;i<100;i++) {
      const job=JSON.parse(loader.poll(app, filename, id))
      if(job.status==='failed') throw new Error(job.error)
      if(job.status==='complete') return job.result
      await new Promise(resolve=>setTimeout(resolve,5))
    }
    throw new Error('Job did not finish')
  }
  write(1)
  return {filename,app,write,run}
}

test('updates wait for all sessions to be explicitly closed',async t=>{
  const h=fixture(t)
  await h.run('open',{path:'a.md'})
  await h.run('open',{path:'b.md'})
  await h.run('select',{path:'a.md',page:'page:second'})
  const before=await h.run('state',{path:'a.md'})
  h.write(2)
  const status=await h.run('doctor')
  assert.equal(status.version,1)
  assert.deepEqual(status.pendingUpdate,{reason:'open_sessions',documents:['a.md','b.md']})
  assert.deepEqual(await h.run('state',{path:'a.md'}),before)
  assert.equal((await h.run('edit',{path:'a.md'})).page,'page:second')
  assert.deepEqual(h.app.events,['open-1','open-1'])
  await h.run('close',{path:'a.md'})
  assert.equal((await h.run('doctor')).version,1)
  await h.run('close',{path:'b.md'})
  assert.deepEqual(h.app.events,['open-1','open-1','close-1','close-1'])
  const updated=await h.run('doctor')
  assert.equal(updated.version,2)
  assert.equal(updated.pendingUpdate,null)
  assert.deepEqual(updated.documents,[])
  assert.equal((await h.run('open',{path:'a.md'})).version,2)
})

test('missing-document close failure does not block diagnostics or unrelated work',async t=>{
  const h=fixture(t)
  await h.run('open',{path:'deleted.md'})
  const before=await h.run('state',{path:'deleted.md'})
  h.app.blockClose='deleted.md'
  h.write(2)
  assert.equal((await h.run('doctor')).version,1)
  assert.deepEqual(h.app.events,['open-1'])
  assert.deepEqual(await h.run('state',{path:'deleted.md'}),before)
  await assert.rejects(h.run('close',{path:'deleted.md'}),/Markdown persistence/)
  assert.deepEqual(h.app.events,['open-1'])
  assert.equal((await h.run('create',{path:'new.md'})).version,1)
  assert.equal((await h.run('edit',{path:'new.md'})).version,1)
  await h.run('close',{path:'new.md'})
  assert.deepEqual((await h.run('doctor')).pendingUpdate.documents,['deleted.md'])
  assert.deepEqual(h.app.calls.filter(call=>call.action==='close').map(call=>call.path),['deleted.md','new.md'])
  h.app.blockClose=null
  await h.run('close',{path:'deleted.md'})
  assert.equal((await h.run('doctor')).version,2)
})

test('adopts legacy sessions without capture, disposal or receipt loss',async t=>{
  const h=fixture(t), legacy=require(h.filename)
  legacy.dispatch(h.app,'open',{path:'legacy.md'},'old-open')
  legacy.dispatch(h.app,'edit',{path:'legacy.md'},'old-edit')
  h.app.blockClose='legacy.md'
  h.write(2)
  assert.equal((await h.run('doctor')).version,1)
  assert.deepEqual(h.app.calls.map(call=>call.action),['open','edit','doctor','doctor'])
  assert.equal((await h.run('edit',{path:'legacy.md'},'old-edit')).version,1)
  assert.equal(h.app.edits,1)
  assert.throws(()=>loader.dispatch(h.app,h.filename,'doctor',{},'old-edit'),/another request/)
  h.app.blockClose=null
  await h.run('close',{path:'legacy.md'})
  assert.equal((await h.run('doctor')).version,2)
  assert.equal((await h.run('edit',{path:'legacy.md'},'old-edit')).version,1)
  assert.deepEqual(JSON.parse(loader.forget(h.app,h.filename,'old-edit')),{forgotten:true})
})

test('busy legacy runtime is not switched or disposed',async t=>{
  const h=fixture(t)
  require(h.filename).dispatch(h.app,'open',{path:'a.md'},'legacy')
  h.app.busy=true
  h.write(2)
  await assert.rejects(h.run('doctor'),/still running/)
  assert.deepEqual(h.app.events,['open-1'])
  h.app.busy=false
  assert.equal((await h.run('edit',{path:'a.md'})).version,1)
})

test('latest pending source wins and reverting the source clears the pending update',async t=>{
  const h=fixture(t)
  await h.run('open',{path:'a.md'})
  h.write(2)
  assert.ok((await h.run('doctor')).pendingUpdate)
  h.write(1)
  assert.equal((await h.run('doctor')).pendingUpdate,null)
  h.write(2)
  await h.run('doctor')
  h.write(3)
  await h.run('close',{path:'a.md'})
  assert.equal((await h.run('doctor')).version,3)
})

for (const source of ['invalid javascript !!','module.exports=null;', 'module.exports={};',
  ...['dispatch','poll','forget'].map(method=>`module.exports={dispatch(){},poll(){},forget(){},${method}:true};`)]) {
  test(`invalid pending source does not prevent using or closing existing sessions: ${source}`,async t=>{
    const h=fixture(t)
    await h.run('open',{path:'a.md'})
    fs.writeFileSync(h.filename,source)
    assert.equal((await h.run('doctor')).version,1)
    assert.equal((await h.run('edit',{path:'a.md'})).version,1)
    await h.run('close',{path:'a.md'})
    await assert.rejects(h.run('doctor'))
    h.write(2)
    assert.equal((await h.run('doctor')).version,2)
  })
}

test('invalid initial exports can be corrected without restarting',async t=>{
  const h=fixture(t)
  fs.writeFileSync(h.filename,'module.exports={};')
  await assert.rejects(h.run('doctor'),/Required runtime APIs/)
  h.write(2)
  assert.equal((await h.run('doctor')).version,2)
})

test('unavailable source leaves the existing runtime usable',async t=>{
  const h=fixture(t)
  await h.run('open',{path:'a.md'})
  fs.unlinkSync(h.filename)
  assert.equal((await h.run('doctor')).pendingUpdate.reason,'source_unavailable')
  assert.equal((await h.run('edit',{path:'a.md'})).version,1)
  await h.run('close',{path:'a.md'})
  h.write(2)
  assert.equal((await h.run('doctor')).version,2)
})

test('loader serializes jobs and protects running receipts',async t=>{
  const h=fixture(t)
  const first=loader.dispatch(h.app,h.filename,'edit',{},'in-flight')
  assert.equal(JSON.parse(first).status,'running')
  assert.equal(loader.dispatch(h.app,h.filename,'edit',{},'in-flight'),first)
  assert.throws(()=>loader.dispatch(h.app,h.filename,'edit',{},'other'),/still running/)
  assert.throws(()=>loader.forget(h.app,h.filename,'in-flight'),/still running/)
  assert.equal((await h.run('edit',{},'in-flight')).edits,1)
})

test('structured failures and completed request ids survive replacement',async t=>{
  const h=fixture(t)
  const before=await h.run('edit',{},'stable-id')
  await assert.rejects(h.run('structured-failure',{},'failed-edit'),/save unavailable/)
  const failure=JSON.parse(loader.poll(h.app,h.filename,'failed-edit')).failure
  assert.equal(failure.code,'SAVE_UNCONFIRMED')
  assert.equal(failure.outcome,'applied')
  assert.equal(failure.details.revision,'after-edit')
  h.write(2)
  assert.equal((await h.run('doctor')).version,2)
  assert.deepEqual(await h.run('edit',{},'stable-id'),before)
  assert.equal(h.app.edits,1)
  assert.deepEqual(JSON.parse(loader.poll(h.app,h.filename,'failed-edit')).failure,failure)
  assert.deepEqual(JSON.parse(loader.forget(h.app,h.filename,'stable-id')),{forgotten:true})
})
