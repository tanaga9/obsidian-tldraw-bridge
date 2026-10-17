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
  const app = { documents: new Set(), events: [], edits: 0 }
  function write(version) {
    fs.writeFileSync(filename, `
      const jobs = new Map();
      const pages = new Map();
      module.exports = {
        dispatch(app, action, args, id) {
          if (jobs.has(id)) {
            if(jobs.get(id).request !== JSON.stringify([action,args])) throw new Error('Job id already used for another request');
            return JSON.stringify(jobs.get(id));
          }
          if(app.busy) throw new Error('CLI job still running');
          const job = {id,request:JSON.stringify([action,args]),status:'complete'};
          if(action==='doctor') job.result={documents:[...app.documents],version:${version}};
          if(action==='open') {
            if(app.blockOpen===args.path) throw new Error('Markdown document required');
            pages.set(args.path,args.currentPageId || 'page:first');
            app.documents.add(args.path);app.events.push('open-${version}');job.result={version:${version}};
          }
          if(action==='state') job.result={revision:'unchanged',...(app.oldState ? {} : {currentPageId:pages.get(args.path)})};
          if(action==='select') pages.set(args.path,args.page);
          if(action==='script') new Function('editor','app',args.code)({getCurrentPageId:()=>pages.get(args.path)},app);
          if(action==='close') {
            if(app.unsaved) {job.status='failed';job.error='Timed out waiting for Markdown persistence';}
            else {app.documents.delete(args.path);pages.delete(args.path);app.events.push('close-${version}');job.result={closed:true};}
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

test('changed source closes saved sessions and reopens them using new runtime',async t=>{
  const h=fixture(t)
  await h.run('open',{path:'a.md'})
  h.write(2)
  assert.equal((await h.run('edit')).version,2)
  assert.deepEqual(h.app.events,['open-1','close-1','open-2'])
  await h.run('doctor')
  assert.deepEqual(h.app.events,['open-1','close-1','open-2'])
})

test('completed request ids survive updates without repeating edits',async t=>{
  const h=fixture(t)
  const before=await h.run('edit',{},'stable-id')
  h.write(2)
  await h.run('doctor')
  assert.deepEqual(await h.run('edit',{},'stable-id'),before)
  assert.equal(h.app.edits,1)
  assert.throws(()=>loader.dispatch(h.app,h.filename,'doctor',{},'stable-id'),/another request/)
  assert.deepEqual(JSON.parse(loader.forget(h.app,h.filename,'stable-id')),{forgotten:true})
})

test('adopts legacy require cache and preserves its receipts',async t=>{
  const h=fixture(t), legacy=require(h.filename)
  legacy.dispatch(h.app,'open',{path:'legacy.md'},'old-open')
  legacy.dispatch(h.app,'edit',{},'old-edit')
  h.write(2)
  assert.equal((await h.run('doctor')).version,2)
  assert.deepEqual(h.app.events,['open-1','close-1','open-2'])
  assert.equal((await h.run('edit',{},'old-edit')).version,1)
  assert.equal(h.app.edits,1)
  assert.deepEqual(JSON.parse(loader.forget(h.app,h.filename,'old-edit')),{forgotten:true})
})

test('a busy legacy runtime is not disposed or edited',async t=>{
  const h=fixture(t)
  require(h.filename).dispatch(h.app,'open',{path:'a.md'},'legacy')
  h.app.busy=true
  h.write(2)
  await assert.rejects(h.run('edit'),/still running/)
  assert.deepEqual(h.app.events,['open-1'])
  assert.equal(h.app.edits,0)
  h.app.busy=false
  assert.equal((await h.run('edit')).version,2)
})

test('persistence failure stops update before disposal or edit',async t=>{
  const h=fixture(t)
  await h.run('open',{path:'a.md'})
  h.app.unsaved=true
  h.write(2)
  await assert.rejects(h.run('edit'),/Markdown persistence/)
  assert.deepEqual(h.app.events,['open-1'])
  assert.equal(h.app.edits,0)
  h.app.unsaved=false
  assert.equal((await h.run('edit')).version,2)
})

test('invalid updated code leaves the old sessions intact',async t=>{
  const h=fixture(t)
  await h.run('open',{path:'a.md'})
  fs.writeFileSync(h.filename,'invalid javascript !!')
  await assert.rejects(h.run('edit'),/Unexpected/)
  assert.deepEqual(h.app.events,['open-1'])
  h.write(2)
  assert.equal((await h.run('edit')).version,2)
})

test('loader serializes jobs and protects running receipts',async t=>{
  const h=fixture(t)
  const first=loader.dispatch(h.app,h.filename,'edit',{},'in-flight')
  assert.equal(JSON.parse(first).status,'running')
  assert.equal(loader.dispatch(h.app,h.filename,'edit',{},'in-flight'),first)
  assert.throws(()=>loader.dispatch(h.app,h.filename,'edit',{},'other'),/still running/)
  assert.throws(()=>loader.forget(h.app,h.filename,'in-flight'),/still running/)
  const result=await h.run('edit',{},'in-flight')
  assert.equal(result.edits,1)
})

test('reload preserves selected page for edits without changing revision',async t=>{
  const h=fixture(t)
  await h.run('open',{path:'a.md'})
  await h.run('select',{path:'a.md',page:'page:second'})
  const before=await h.run('state',{path:'a.md'})
  h.write(2)
  const edited=await h.run('edit',{path:'a.md'})
  assert.equal(edited.page,'page:second')
  assert.deepEqual(await h.run('state',{path:'a.md'}),before)
})

test('captures selected page from a legacy runtime without page reporting',async t=>{
  const h=fixture(t), legacy=require(h.filename)
  legacy.dispatch(h.app,'open',{path:'a.md'},'legacy-open')
  legacy.dispatch(h.app,'select',{path:'a.md',page:'page:second'},'legacy-select')
  h.app.oldState=true
  h.write(2)
  const edited=await h.run('edit',{path:'a.md'})
  assert.equal(edited.page,'page:second')
  assert.equal(Object.getOwnPropertySymbols(h.app).length,0)
})

test('failed reopen is isolated, reported, retriable, and dismissible',async t=>{
  const h=fixture(t)
  await h.run('open',{path:'a.md'})
  await h.run('open',{path:'b.md'})
  await h.run('select',{path:'a.md',page:'page:second'})
  h.app.blockOpen='a.md'
  h.write(2)
  const status=await h.run('doctor')
  assert.deepEqual(status.documents,['b.md'])
  assert.deepEqual(status.reloadErrors,[{path:'a.md',currentPageId:'page:second',error:'Markdown document required'}])
  assert.equal((await h.run('edit',{path:'b.md'})).version,2)
  await h.run('close',{path:'b.md'})
  await h.run('open',{path:'c.md'})
  await assert.rejects(h.run('edit',{path:'a.md'}),/Session could not be reopened/)
  assert.equal(h.app.edits,1)
  await assert.rejects(h.run('open',{path:'a.md'}),/Markdown document required/)
  h.app.blockOpen=null
  await h.run('open',{path:'a.md'})
  assert.equal((await h.run('edit',{path:'a.md'})).page,'page:second')
  assert.deepEqual((await h.run('doctor')).reloadErrors,[])
  h.app.blockOpen='a.md'
  h.write(3)
  await h.run('doctor')
  await h.run('close',{path:'a.md'})
  assert.deepEqual((await h.run('doctor')).reloadErrors,[])
})


test('loader preserves structured failure and applied revision in retained receipts',async t=>{
  const h=fixture(t)
  await assert.rejects(h.run('structured-failure',{},'failed-edit'),/save unavailable/)
  const job=JSON.parse(loader.poll(h.app,h.filename,'failed-edit'))
  assert.equal(job.failure.code,'SAVE_UNCONFIRMED')
  assert.equal(job.failure.outcome,'applied')
  assert.equal(job.failure.details.revision,'after-edit')
  assert.deepEqual(JSON.parse(loader.dispatch(h.app,h.filename,'structured-failure',{},'failed-edit')),job)
})
