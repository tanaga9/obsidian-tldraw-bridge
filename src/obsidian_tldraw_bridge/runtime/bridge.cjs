'use strict'

// A plain local script, not an Obsidian Plugin. No HTTP listener is created.
const apps = new WeakMap()
const crypto = require('node:crypto')
function sessionsFor(app) {
  if (!apps.has(app)) apps.set(app, new Map())
  return apps.get(app)
}
function sessionFor(app, path) {
  const map = sessionsFor(app)
  const session = path ? map.get(path) : map.size === 1 ? [...map.values()][0] : null
  if (!session) throw new Error('Specify an open document path')
  return session
}
function revision(editor) {
  return crypto.createHash('sha256').update(JSON.stringify(records(editor))).digest('hex')
}
function documentRecords(editor, values) {
  const types = editor.store.scopedTypes.document
  return values.filter(record => types.has(record.typeName)).sort((a,b)=>a.id.localeCompare(b.id))
}
function records(editor) {
  return documentRecords(editor, editor.store.allRecords())
}
// Bound retained receipts without silently expiring an idempotency key.
const MAX_JOBS = 128

function errorMessage(error) {
  // JavaScript can throw any value, including objects with throwing getters.
  try {
    const message = error?.message
    if (typeof message === 'string' && message) return message
  } catch (_) {}
  try {
    return String(error) || 'Unknown error'
  } catch (_) {
    return 'Unknown error (unprintable thrown value)'
  }
}

function runWithRollback(editor, label, callback) {
  const before = JSON.parse(JSON.stringify(editor.store.getStoreSnapshot('all').store))
  const mark = editor.markHistoryStoppingPoint(label)
  let failed = false
  let failure
  // Catch inside the SDK transaction. Letting it abort can restore reactive
  // records without undoing queued Store notifications sent to other Editors.
  editor.run(() => {
    try {
      callback()
    } catch (error) {
      failed = true
      failure = error
      try {
        // Remove failed history entries, then restore history-ignored records.
        // Forward and restoring changes commit in the same transaction.
        try { editor.bailToMark(mark) } finally {
          const current = Object.fromEntries(editor.store.allRecords().map(record => [record.id, record]))
          const diff = { added: {}, updated: {}, removed: {} }
          for (const [id, record] of Object.entries(before)) {
            if (!current[id]) diff.added[id] = record
            else if (JSON.stringify(current[id]) !== JSON.stringify(record)) diff.updated[id] = [current[id], record]
          }
          for (const [id, record] of Object.entries(current)) {
            if (!before[id]) diff.removed[id] = record
          }
          editor.run(() => editor.store.applyDiff(diff, { runCallbacks: false }), { history: 'ignore' })
        }
      } catch (rollbackError) {
        failure = new Error(`${errorMessage(error)}; record restoration failed: ${errorMessage(rollbackError)}`)
      }
    }
  })
  // Report failure only after the Store has committed its restoring changes.
  if (failed) throw failure
}

const jobs = new WeakMap()
let sequence = 0

function state(app, path) {
  const session = sessionFor(app, path)
  if (!session || session.editor.isDisposed) throw new Error('No CLI Editor session')
  const current = app.plugins.getPlugin('tldraw')?.currTldrawEditor
  return {
    path: session.path,
    revision: revision(session.editor),
    currentPageId: session.editor.getCurrentPageId(),
    pluginVersion: app.plugins.getPlugin('tldraw').manifest.version,
    bootstrap: session.bootstrap,
    vault: app.vault.getName(),
    dedicatedEditor: session.editor !== session.seed,
    separateStore: session.editor.store !== session.seed.store,
    guiEditorDisposed: session.seed.isDisposed,
    currentEditorIsLive: !!current && !current.isDisposed,
    activeFile: app.workspace.getActiveFile()?.path,
    guiViews: app.workspace.getLeavesOfType('tldraw-view')
      .filter(leaf => leaf.view.file?.path === session.path).length,
    records: records(session.editor),
  }
}

async function acquireSeed(app, plugin, file) {
  const previousLeaf = app.workspace.activeLeaf
  const candidate = plugin.currTldrawEditor
  if (candidate && !candidate.isDisposed) return { seed: candidate, bootstrap: 'live-existing-editor' }
  await plugin.openTldrFile(file, 'new-tab', 'tldraw-view')
  const deadline = Date.now() + 8000
  while (Date.now() < deadline) {
    const seed = plugin.currTldrawEditor
    if (seed && !seed.isDisposed && Object.keys(seed.shapeUtils).length) {
      if (previousLeaf) app.workspace.setActiveLeaf(previousLeaf, { focus: true })
      return { seed, bootstrap: 'opened-existing-view' }
    }
    await new Promise(resolve => setTimeout(resolve, 100))
  }
  throw new Error('Opened tldraw view, but no live Editor reference became available')
}

async function create(app, path) {
  if (typeof path !== 'string' || !path.endsWith('.md') || path.includes('\\') || /[\x00-\x1f]/.test(path)
    || path.split('/').some(part => !part || part === '.' || part === '..') || path.split('/').at(-1) === '.md') {
    throw new Error('Use a vault-relative Markdown path without traversal')
  }
  const plugin = app.plugins.getPlugin('tldraw')
  if (!['1.31.0', '1.32.0'].includes(plugin?.manifest.version)) throw new Error('Unsupported tldraw plugin version')
  if (app.vault.getAbstractFileByPath(path)) throw new Error(`File or folder already exists: ${path}`)
  if (sessionsFor(app).has(path)) throw new Error(`Close the existing session before creating: ${path}`)
  const parts = path.split('/')
  const filename = parts.pop()
  const file = await plugin.createTldrFile(filename, { foldername: parts.join('/'), inMarkdown: true })
  try {
    if (sessionsFor(app).has(file.path)) throw new Error('A session already exists for the created path')
    await plugin.openTldrFile(file, 'new-tab', 'tldraw-view')
    const result = await open(app, file.path)
    return { ...result, created: true, requestedPath: path, persistence: await saved(app, file.path) }
  } catch (error) {
    // Keep the created note: GUI edits or a delayed save may already exist.
    throw new Error(`Created ${file.path}, but initialization failed: ${errorMessage(error)}. Use open with this path to recover.`)
  }
}

async function open(app, path, currentPageId) {
  if (sessionsFor(app).has(path)) return state(app, path)
  const plugin = app.plugins.getPlugin('tldraw')
  if (!['1.31.0', '1.32.0'].includes(plugin?.manifest.version)) throw new Error('Unsupported tldraw plugin version')
  const file = app.vault.getAbstractFileByPath(path)
  if (!file || file.extension !== 'md') throw new Error('Markdown document required')
  const text = await app.vault.read(file)
  parseMarkdown(text)
  const { seed, bootstrap } = await acquireSeed(app, plugin, file)
  const session = { path, seed, file, bootstrap, editor: null }
  session.registration = plugin.tlDataDocumentStoreManager.register(
    file, () => text, data => { session.serialized = data }, true
  )
  session.container = seed.getContainer().ownerDocument.createElement('div')
  session.container.className = 'tl-container codex-cli-session-probe'
  session.container.style.cssText = 'position:fixed;left:-10000px;top:0;width:800px;height:600px;pointer-events:none;'
  session.container.ownerDocument.body.appendChild(session.container)
  sessionsFor(app).set(path, session)
  try {
    session.editor = new seed.constructor({
      store: session.registration.documentStore.store,
      shapeUtils: Object.values(seed.shapeUtils).filter(u => u && u.constructor.type !== 'group').map(u => u.constructor),
      bindingUtils: Object.values(seed.bindingUtils).filter(Boolean).map(u => u.constructor),
      assetUtils: Object.values(seed.assetUtils).filter(Boolean).map(u => u.constructor),
      tools: Object.values(seed.root.children).map(tool => tool.constructor),
      initialState: 'select',
      autoFocus: false,
      options: { text: seed.getTextOptions?.() ?? seed.options?.text },
      getContainer: () => session.container,
      fontAssetUrls: plugin.getFontOverrides(),
    })
    if (currentPageId) {
      if (!session.editor.getPage(currentPageId)) throw new Error(`Previous page no longer exists: ${currentPageId}`)
      session.editor.setCurrentPage(currentPageId)
    }
    return state(app, path)
  } catch (error) {
    close(app, path)
    throw error
  }
}

function close(app, path) {
  const session = sessionFor(app, path)
  if (!session) return { closed: true }
  session.registration.syncToMain(false)
  if (session.editor && !session.editor.isDisposed) session.editor.dispose()
  session.registration.unregister()
  session.container.remove()
  sessionsFor(app).delete(session.path)
  return { closed: true }
}

const methods = new Set(['createShapes', 'updateShapes', 'deleteShapes', 'createBindings',
  'deleteBindings', 'groupShapes', 'ungroupShapes', 'alignShapes', 'distributeShapes', 'rotateShapesBy', 'resizeShape', 'reparentShapes', 'createPage', 'updatePage', 'deletePage', 'setCurrentPage', 'undo', 'redo'])

function assertRevision(session, expected) {
  if (!expected || revision(session.editor) !== expected) throw new Error('Revision conflict: read state and re-plan before editing')
}
function editResult(app, path, before, full) {
  const result = state(app, path)
  const previous = new Map(before.map(record => [record.id, record]))
  const changes = { added: 0, updated: 0, removed: 0 }
  for (const record of result.records) {
    const old = previous.get(record.id)
    if (!old) changes.added++
    else if (JSON.stringify(old) !== JSON.stringify(record)) changes.updated++
    previous.delete(record.id)
  }
  changes.removed = previous.size
  if (full) return { ...result, changes }
  return { path: result.path, revision: result.revision, currentPageId: result.currentPageId, changes }
}

function batch(app, path, operations, expected, full = false) {
  const session = sessionFor(app, path)
  assertRevision(session, expected)
  if (!Array.isArray(operations) || !operations.length || operations.length > 1000) throw new Error('Batch must contain 1-1000 operations')
  for (const op of operations) {
    if (!op || !methods.has(op.method) || !Array.isArray(op.args) || typeof session.editor[op.method] !== 'function') throw new Error('Unsupported operation')
  }
  const editor = session.editor
  const before = JSON.parse(JSON.stringify(records(editor)))
  const history = operations.some(op => ['undo','redo'].includes(op.method))
  if (history && operations.length !== 1) throw new Error('Undo/redo must be a separate batch')
  const apply = () => { for (const op of operations) editor[op.method](...op.args) }
  if (history) editor.run(apply)
  else runWithRollback(editor, 'Obsidian tldraw bridge', apply)
  return editResult(app, path, before, full)
}
function script(app, path, code, expected, full = false) {
  const session = sessionFor(app, path)
  assertRevision(session, expected)
  if (typeof code !== 'string' || !code.trim()) throw new Error('Script is empty')
  const editor = session.editor
  // Trusted synchronous code, not a sandbox. A returned Promise is detected only
  // after execution: this check cannot cancel already scheduled work.
  const before = JSON.parse(JSON.stringify(records(editor)))
  const fn = new Function('editor', 'app', 'plugin', 'require', code)
  runWithRollback(editor, 'Obsidian tldraw bridge script', () => {
    const result = fn(editor, app, app.plugins.getPlugin('tldraw'), require)
    if (result && typeof result.then === 'function') {
      Promise.resolve(result).catch(() => {})
      throw new Error('Scripts must be synchronous; scheduled work cannot be cancelled')
    }
  })
  return editResult(app, path, before, full)
}

function parseMarkdown(text) {
  const start = text.indexOf('```json !!!_START_OF_TLDRAW_DATA__DO_NOT_CHANGE_THIS_PHRASE_!!!')
  if (start < 0) throw new Error('Not a tldraw Markdown document')
  const bodyStart = text.indexOf('\n', start) + 1
  const endMarker = text.indexOf('!!!_END_OF_TLDRAW_DATA__DO_NOT_CHANGE_THIS_PHRASE_!!!', bodyStart)
  if (endMarker < bodyStart) throw new Error('Missing tldraw end marker')
  const data = JSON.parse(text.slice(bodyStart, endMarker).trim())
  if (!Array.isArray(data.raw?.records)) throw new Error('Unsupported tldraw document format')
  return data
}

function flushPendingChanges(app, session) {
  // Store.listen flushes pending notifications before attaching the listener.
  // Drain both hops without waiting for animation frames in background windows.
  const flush = store => {
    const stop = store.listen(() => {}, { scope: 'document' })
    stop()
  }
  flush(session.editor.store)
  const main = app.plugins.getPlugin('tldraw')?.tlDataDocumentStoreManager
    ?.storesManager.storeGroupMap.get(session.file.path)?.main.store
  if (main && main !== session.editor.store) flush(main)
}

async function saved(app, path) {
  const session = sessionFor(app, path)
  if (!session) throw new Error('No session')
  const deadline = Date.now() + 10000
  while (Date.now() < deadline) {
    flushPendingChanges(app, session)
    const text = await app.vault.read(session.file)
    const document = parseMarkdown(text)
    const actual = JSON.stringify(documentRecords(session.editor, document.raw.records))
    const expected = JSON.stringify(records(session.editor))
    if (actual === expected) return { saved: true, path: session.path, bytes: Buffer.byteLength(text) }
    await new Promise(resolve => setTimeout(resolve, 100))
  }
  throw new Error('Timed out waiting for Markdown persistence')
}

async function execute(app, action, args) {
  if (action === 'doctor') {
    const plugin = app.plugins.getPlugin('tldraw')
    return {vault: app.vault.getName(), pluginVersion: plugin?.manifest.version ?? null,
      supported: ['1.31.0','1.32.0'].includes(plugin?.manifest.version),
      documents: [...sessionsFor(app).keys()]}
  }
  if (action === 'create') return create(app, args.path)
  if (action === 'open') return open(app, args.path, args.currentPageId)
  if (action === 'state') return state(app, args.path)
  if (action === 'batch' || action === 'script') {
    const result = action === 'batch' ? batch(app,args.path,args.operations,args.revision,args.full) : script(app,args.path,args.code,args.revision,args.full)
    return {...result, persistence: await saved(app,args.path)}
  }
  if (action === 'saved') return saved(app, args.path)
  if (action === 'close') {
    await saved(app, args.path)
    return close(app, args.path)
  }
  if (action === 'preview') {
    const session = sessionFor(app, args.path)
    if (args.revision) assertRevision(session,args.revision)
    const editor = session.editor
    const capturedRevision = revision(editor)
    const pageIds = [...editor.getCurrentPageShapeIds()]
    if ([args.ids, args.part, args.bounds].filter(value => value !== undefined).length > 1) throw new Error('Choose ids, part, or bounds, not more than one')
    if (args.part !== undefined && (typeof args.part !== 'string' || !args.part.trim())) throw new Error('Part must be a nonempty string')
    const ids = args.part !== undefined
      ? pageIds.filter(id => editor.getShape(id)?.meta?.bridgeFreehand?.part === args.part)
      : args.ids ?? pageIds
    if (!Array.isArray(ids) || !ids.length || ids.some(id => !pageIds.includes(id))) throw new Error('Preview selection must contain existing current-page shapes')
    const scale = args.scale ?? 1
    if (!Number.isFinite(scale) || scale <= 0 || scale > 4) throw new Error('Preview scale must be greater than 0 and at most 4')
    let bounds
    if (args.bounds !== undefined) {
      const b = args.bounds
      if (!b || !['x', 'y', 'w', 'h'].every(key => Number.isFinite(b[key])) || b.w <= 0 || b.h <= 0) {
        throw new Error('Preview bounds must be finite with positive width and height')
      }
      // Keep the SDK Box prototype required by toImage; never mutate cached geometry.
      const sample = ids.map(id => editor.getShapePageBounds(id)).find(Boolean)
      if (!sample) throw new Error('No shape bounds available for preview')
      bounds = Object.assign(sample.clone(), { x: b.x, y: b.y, w: b.w, h: b.h })
    }
    const { blob, width, height } = await editor.toImage(ids, {
      format: 'png', scale, background: true,
      ...(bounds ? { bounds, padding: 0 } : {}),
    })
    const bytes = Buffer.from(await blob.arrayBuffer())
    if (revision(editor) !== capturedRevision) throw new Error('Revision conflict during preview: read state and export again')
    require('node:fs').writeFileSync(args.output, bytes)
    return { path: args.output, width, height, revision: capturedRevision }
  }
  throw new Error('Unknown action')
}

module.exports = {
  // Return synchronously: older Obsidian CLI does not await eval's Promise output.
  dispatch(app, action, args = {}, requestedId) {
    let queue = jobs.get(app)
    if (!queue) jobs.set(app, queue = new Map())
    const id = requestedId || `job-${++sequence}`
    const request = JSON.stringify([action,args])
    if (queue.has(id)) {
      if (queue.get(id).request !== request) throw new Error('Job id already used for another request')
      return JSON.stringify(queue.get(id))
    }
    if ([...queue.values()].some(job => job.status === 'running')) throw new Error('CLI job still running')
    if (queue.size >= MAX_JOBS) throw new Error('Receipt capacity reached: use the CLI forget command to release completed request ids')
    const job = { id, request, status: 'running' }
    queue.set(id, job)
    Promise.resolve().then(() => execute(app, action, args)).then(
      result => { job.result = result; job.status = 'complete' },
      error => { job.status = 'failed'; job.error = errorMessage(error) }
    )
    return JSON.stringify(job)
  },
  poll(app, id) {
    const job = jobs.get(app)?.get(id)
    if (!job) throw new Error('Unknown CLI job')
    return JSON.stringify(job)
  },
  forget(app, id) {
    const job = jobs.get(app)?.get(id)
    if (job?.status === 'running') throw new Error('CLI job still running')
    return JSON.stringify({ forgotten: jobs.get(app)?.delete(id) ?? false })
  },
}
