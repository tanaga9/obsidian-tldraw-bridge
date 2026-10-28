'use strict'

// Keep this loader stable: only the drawing runtime is replaced on updates.
const fs = require('node:fs')
const crypto = require('node:crypto')
const Module = require('node:module')
const path = require('node:path')
const apps = new WeakMap()
const delay = () => new Promise(resolve => setTimeout(resolve, 10))
let sequence = 0

function context(app, filename) {
  if (!apps.has(app)) apps.set(app, new Map())
  const contexts = apps.get(app)
  if (!contexts.has(filename)) {
    const legacy = require.cache[require.resolve(filename)]?.exports
    contexts.set(filename, {
      active: legacy, digest: null, versions: legacy ? [legacy] : [],
      jobs: new Map(), pendingUpdate: null,
    })
  }
  return contexts.get(filename)
}

function retained(ctx, app, id) {
  for (const runtime of ctx.versions) {
    try { return { runtime, job: JSON.parse(runtime.poll(app, id)) } } catch (error) {
      if (error.message !== 'Unknown CLI job') throw error
    }
  }
  return null
}

async function invoke(runtime, app, action, args) {
  const id = `loader-${crypto.randomUUID()}`
  runtime.dispatch(app, action, args, id)
  while (true) {
    const job = JSON.parse(runtime.poll(app, id))
    if (job.status !== 'running') {
      runtime.forget(app, id)
      if (job.status === 'failed') throw Object.assign(new Error(job.error), job.failure)
      return job.result
    }
    await delay()
  }
}

async function refresh(ctx, app, filename) {
  let source
  try {
    source = fs.readFileSync(filename, 'utf8')
  } catch (error) {
    if (!ctx.active) throw error
    // An unavailable source must not prevent existing sessions from being used
    // or explicitly closed. No replacement can be loaded until it is readable.
    ctx.pendingUpdate = { reason: 'source_unavailable', error: error.message }
    return
  }
  const digest = crypto.createHash('sha256').update(source).digest('hex')
  if (ctx.digest === digest) {
    ctx.pendingUpdate = null
    return
  }
  if (ctx.active) {
    const previous = await invoke(ctx.active, app, 'doctor', {})
    if (previous.documents.length) {
      // Keep a single session owner. Updating never captures, closes or reopens
      // documents; explicit close retains the runtime's persistence checks.
      ctx.pendingUpdate = { reason: 'open_sessions', documents: previous.documents }
      return
    }
  }
  const fresh = new Module(filename, module)
  fresh.filename = filename
  fresh.paths = Module._nodeModulePaths(path.dirname(filename))
  fresh._compile(source, filename)
  const missing = ['dispatch', 'poll', 'forget'].filter(method => typeof fresh.exports?.[method] !== 'function')
  if (missing.length) {
    throw Object.assign(new Error(`Required runtime APIs are unavailable: ${missing.join(', ')}`),
      { code: 'INVALID_RUNTIME', outcome: 'not_applied' })
  }
  ctx.active = fresh.exports
  // Old runtimes retain receipts only, with no open document sessions.
  ctx.versions.push(fresh.exports)
  ctx.digest = digest
  ctx.pendingUpdate = null
}

module.exports = {
  dispatch(app, filename, action, args = {}, requestedId) {
    const ctx = context(app, filename)
    const id = requestedId || `loader-job-${++sequence}`
    const request = JSON.stringify([action, args])
    if (ctx.jobs.has(id)) {
      const job = ctx.jobs.get(id)
      if (job.request !== request) throw Object.assign(new Error('Job id already used for another request'), { code: 'REQUEST_ID_REUSED', outcome: 'not_applied' })
      return JSON.stringify(job)
    }
    // Receipts from before the update still own their ids, including running jobs.
    const previous = retained(ctx, app, id)
    if (previous) return previous.runtime.dispatch(app, action, args, id)
    if ([...ctx.jobs.values()].some(job => job.status === 'running')) throw Object.assign(new Error('CLI job still running'), { code: 'RUNTIME_BUSY', outcome: 'not_applied' })
    if (ctx.jobs.size >= 128) throw Object.assign(new Error('Receipt capacity reached: use the CLI forget command to release completed request ids'), { code: 'RECEIPT_CAPACITY', outcome: 'not_applied' })
    const job = { id, request, status: 'running' }
    ctx.jobs.set(id, job)
    Promise.resolve().then(async () => {
      await refresh(ctx, app, filename)
      const result = await invoke(ctx.active, app, action, args)
      return action === 'doctor' ? { ...result, pendingUpdate: ctx.pendingUpdate } : result
    }).then(
      result => { job.result = result; job.status = 'complete' },
      error => {
        job.error = error?.message || String(error); job.status = 'failed'
        job.failure = { code: error?.code || 'RUNTIME_ERROR', message: job.error, outcome: error?.outcome || 'unknown',
          ...(error?.details ? { details: error.details } : {}) }
      }
    )
    return JSON.stringify(job)
  },
  poll(app, filename, id) {
    const ctx = context(app, filename)
    const job = ctx.jobs.get(id) || retained(ctx, app, id)?.job
    if (!job) throw Object.assign(new Error('Unknown CLI job'), { code: 'REQUEST_NOT_FOUND', outcome: 'unknown' })
    return JSON.stringify(job)
  },
  forget(app, filename, id) {
    const ctx = context(app, filename)
    const job = ctx.jobs.get(id)
    if (job?.status === 'running') throw Object.assign(new Error('CLI job still running'), { code: 'RUNTIME_BUSY', outcome: 'not_applied' })
    if (job) return JSON.stringify({ forgotten: ctx.jobs.delete(id) })
    const previous = retained(ctx, app, id)
    return previous ? previous.runtime.forget(app, id) : JSON.stringify({ forgotten: false })
  },
}
