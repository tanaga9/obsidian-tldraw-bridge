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
      jobs: new Map(), reopen: new Map(), reloadErrors: new Map(),
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

async function capturePage(runtime, app, document) {
  const state = await invoke(runtime, app, 'state', { path: document })
  if (state.currentPageId) return state.currentPageId
  // Runtimes from before page reporting still support synchronous scripts.
  const key = `bridge-reload-page-${crypto.randomUUID()}`
  const slot = Symbol.for(key)
  try {
    await invoke(runtime, app, 'script', {
      path: document, revision: state.revision,
      code: `app[Symbol.for(${JSON.stringify(key)})] = editor.getCurrentPageId();`,
    })
    if (!app[slot]) throw new Error('Cannot capture current page before runtime update')
    return app[slot]
  } finally {
    delete app[slot]
  }
}

async function refresh(ctx, app, filename) {
  const source = fs.readFileSync(filename, 'utf8')
  const digest = crypto.createHash('sha256').update(source).digest('hex')
  if (ctx.digest !== digest) {
    // Compile and validate before closing anything or retaining the new runtime.
    const fresh = new Module(filename, module)
    fresh.filename = filename
    fresh.paths = Module._nodeModulePaths(path.dirname(filename))
    fresh._compile(source, filename)
    const missing = ['dispatch', 'poll', 'forget'].filter(method => typeof fresh.exports?.[method] !== 'function')
    if (missing.length) {
      throw Object.assign(new Error(`Required runtime APIs are unavailable: ${missing.join(', ')}`),
        { code: 'INVALID_RUNTIME', outcome: 'not_applied' })
    }
    if (ctx.active) {
      const previous = await invoke(ctx.active, app, 'doctor', {})
      for (const document of previous.documents) {
        ctx.reopen.set(document, await capturePage(ctx.active, app, document))
      }
      // close checks persistence before disposing. A busy old runtime rejects
      // doctor above, so a running edit is never interrupted by an update.
      for (const document of previous.documents) {
        await invoke(ctx.active, app, 'close', { path: document })
      }
    }
    ctx.active = fresh.exports
    ctx.versions.push(fresh.exports)
    ctx.digest = digest
  }
  for (const [document, currentPageId] of ctx.reopen) {
    try {
      await invoke(ctx.active, app, 'open', { path: document, currentPageId })
      ctx.reloadErrors.delete(document)
    } catch (error) {
      ctx.reloadErrors.set(document, { path: document, currentPageId, error: error.message || String(error) })
    }
    // One failed document must not block diagnostics or unrelated documents.
    ctx.reopen.delete(document)
  }
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
      const failed = ctx.reloadErrors.get(args.path)
      if (failed && action === 'close') {
        const status = await invoke(ctx.active, app, 'doctor', {})
        if (status.documents.includes(args.path)) await invoke(ctx.active, app, 'close', args)
        ctx.reloadErrors.delete(args.path)
        return { closed: true }
      }
      if (failed && action !== 'open') {
        throw new Error(`Session could not be reopened: ${args.path}: ${failed.error}. Use open to retry or close to dismiss.`)
      }
      const requestArgs = failed ? { currentPageId: failed.currentPageId, ...args } : args
      const result = await invoke(ctx.active, app, action, requestArgs)
      if (action === 'open') ctx.reloadErrors.delete(args.path)
      return action === 'doctor' ? { ...result, reloadErrors: [...ctx.reloadErrors.values()] } : result
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
