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
const INITIALIZATION_TIMEOUT_MS = 8000

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
        failure = fault('ROLLBACK_FAILED', `${errorMessage(error)}; record restoration failed: ${errorMessage(rollbackError)}`, 'unknown')
      }
    }
  })
  // Report failure only after the Store has committed its restoring changes.
  if (failed) throw failure
}

const jobs = new WeakMap()
let sequence = 0

// The AI-facing contract is independent of CLI parsing and transport.
const operationFields = {
  createShapes: { shapes: 'array' }, updateShapes: { shapes: 'array' }, deleteShapes: { ids: 'array' },
  createBindings: { bindings: 'array' }, deleteBindings: { ids: 'array' },
  alignShapes: { ids: 'array', alignment: ['left', 'center-horizontal', 'right', 'top', 'center-vertical', 'bottom'] },
  distributeShapes: { ids: 'array', axis: ['horizontal', 'vertical'] },
  setCurrentPage: { pageId: 'string' }, undo: {}, redo: {},
}
function fault(code, message, outcome = 'not_applied', details) {
  return Object.assign(new Error(message), { code, outcome, details })
}
function failureInfo(error, fallback = 'not_applied') {
  try {
    return { code: typeof error?.code === 'string' ? error.code : 'OPERATION_FAILED',
      message: errorMessage(error), outcome: error?.outcome || fallback,
      ...(error?.details ? { details: error.details } : {}) }
  } catch (_) { return { code: 'OPERATION_FAILED', message: errorMessage(error), outcome: 'unknown' } }
}
const testedPluginVersions = ['1.31.0', '1.32.0']
const pluginFunctions = ['getFontOverrides', 'tlDataDocumentStoreManager.register',
  'tlDataDocumentStoreManager.storesManager.storeGroupMap.get']
function missingFunctions(object, paths, prefix) {
  return paths.filter(path => typeof path.split('.').reduce((value, key) => value?.[key], object) !== 'function')
    .map(path => `${prefix}.${path}`)
}
function requireFunctions(object, paths, prefix) {
  const missingCapabilities = missingFunctions(object, paths, prefix)
  if (missingCapabilities.length) throw fault('TLDRAW_UNSUPPORTED',
    `Required tldraw APIs are unavailable: ${missingCapabilities.join(', ')}`, 'not_applied', { missingCapabilities })
}
function pluginSupport(plugin) {
  const pluginVersion = plugin?.manifest?.version ?? null
  const missingCapabilities = missingFunctions(plugin, pluginFunctions, 'plugin')
  return { pluginVersion, supported: !!plugin && missingCapabilities.length === 0,
    testedPluginVersions, versionTested: testedPluginVersions.includes(pluginVersion), missingCapabilities }
}
function requirePlugin(app) {
  const plugin = app.plugins.getPlugin('tldraw')
  if (!plugin) throw fault('TLDRAW_UNAVAILABLE', 'Install and enable the tldraw community plugin')
  requireFunctions(plugin, pluginFunctions, 'plugin')
  return plugin
}
function requireEditor(editor) {
  requireFunctions(editor, ['getCurrentPageId', 'dispose',
    'store.allRecords', 'store.listen', 'store.scopedTypes.document.has'], 'editor')
}
function requireEditing(editor) {
  requireFunctions(editor, ['run', 'markHistoryStoppingPoint', 'bailToMark',
    'store.getStoreSnapshot', 'store.applyDiff'], 'editor')
}
function capabilities(app) {
  const plugin = app.plugins.getPlugin('tldraw')
  return { apiVersion: 1, ...pluginSupport(plugin),
    actions: ['doctor','capabilities','create','open','observe','state','apply','batch','script','saved','preview','close'],
    operations: operationFields, coordinates: { observeBounds: 'page', shapePosition: 'parent-local' }, observation: 'dedicated-editor-current-page',
    limits: { operations: 1000, observeShapes: 500, observeBindings: 500, retainedRequests: 128, previewScale: 4 },
    guarantees: { revisionRequiredForEdits: true, persistenceChecked: true, synchronousStoreRollback: true,
      humanEditLock: false, arbitraryScriptCancellation: false, receiptsSurviveRestart: false },
    shapeTypes: [...sessionsFor(app).values()][0]?.editor.shapeUtils
      ? Object.keys([...sessionsFor(app).values()][0].editor.shapeUtils).sort() : null,
    shapeTypesNote: 'Open a document to discover registered types; shape props follow its installed SDK.',
  }
}
function namedOperations(operations) {
  if (!Array.isArray(operations) || !operations.length || operations.length > 1000) {
    throw fault('INVALID_INPUT', 'Apply must contain 1-1000 operations')
  }
  return operations.map((op, index) => {
    const fields = op && typeof op.op === 'string' && Object.hasOwn(operationFields, op.op) ? operationFields[op.op] : null
    if (!fields || Object.keys(op).some(key => key !== 'op' && !Object.hasOwn(fields, key))) {
      throw fault('INVALID_INPUT', 'Unknown operation or argument', 'not_applied', { operationIndex: index })
    }
    const args = Object.entries(fields).map(([key, type]) => {
      const value = op[key]
      const valid = Array.isArray(type) ? type.includes(value) : type === 'array'
        ? Array.isArray(value) && value.length > 0 : typeof value === 'string' && value.length > 0
      if (!valid) throw fault('INVALID_INPUT', `Invalid ${key} for ${op.op}`, 'not_applied', { operationIndex: index })
      return value
    })
    const prefix = op.op === 'deleteBindings' ? 'binding:' : 'shape:'
    if (op.ids && op.ids.some(id => typeof id !== 'string' || !id.startsWith(prefix))) {
      throw fault('INVALID_INPUT', `Expected ${prefix} IDs`, 'not_applied', { operationIndex: index })
    }
    return { method: op.op, args }
  })
}
function observe(app, args) {
  const session = sessionFor(app, args.path), editor = session.editor
  flushPendingChanges(app, session)
  if (args.revision) assertRevision(app, session, args.revision)
  const limit = args.limit ?? 100, offset = args.offset ?? 0
  if (!Number.isInteger(limit) || limit < 1 || limit > 500 || !Number.isInteger(offset) || offset < 0 || (offset && (!args.revision || !args.pageId))) {
    throw fault('INVALID_INPUT', 'Observe requires limit 1-500, offset >= 0, and revision/pageId for subsequent pages')
  }
  if (args.ids !== undefined && args.bounds !== undefined) throw fault('INVALID_INPUT', 'Choose ids or bounds')
  if (args.pageId !== undefined && args.pageId !== editor.getCurrentPageId()) {
    throw fault('PAGE_CONFLICT', 'Current page changed; observe again before continuing')
  }
  const pageIds = [...editor.getCurrentPageShapeIds()].sort()
  if (args.ids !== undefined && (!Array.isArray(args.ids) || !args.ids.length || args.ids.some(id => !pageIds.includes(id)))) {
    throw fault('INVALID_INPUT', 'Observe IDs must exist on the current page')
  }
  const b = args.bounds
  if (b !== undefined && (!b || !['x','y','w','h'].every(k => Number.isFinite(b[k])) || b.w <= 0 || b.h <= 0)) {
    throw fault('INVALID_INPUT', 'Bounds must be finite with positive width and height')
  }
  const shapeBounds = id => {
    const box = editor.getShapePageBounds(id)
    return box ? { x: box.x, y: box.y, w: box.w, h: box.h } : null
  }
  let ids = args.ids ?? pageIds
  if (b) ids = ids.filter(id => {
    const box = shapeBounds(id)
    return box && box.x <= b.x+b.w && box.x+box.w >= b.x && box.y <= b.y+b.h && box.y+box.h >= b.y
  })
  const total = ids.length, selected = ids.slice(offset, offset + limit), selectedSet = new Set(selected)
  const all = records(editor)
  const bindings = all.filter(r => r.typeName === 'binding' && (selectedSet.has(r.fromId) || selectedSet.has(r.toId)))
  return { path: session.path, revision: revision(editor), currentPageId: editor.getCurrentPageId(),
    coordinateSpace: 'page', source: 'dedicated-editor',
    pages: all.filter(r => r.typeName === 'page').map(r => ({ id: r.id, name: r.name })),
    shapes: selected.map(id => {
      const shape = editor.getShape(id)
      const text = editor.getShapeUtil(shape).getText?.(shape)
      return { id, type: shape.type, parentId: shape.parentId, bounds: shapeBounds(id),
        localPosition: { x: shape.x, y: shape.y },
        localRotation: shape.rotation, opacity: shape.opacity, index: shape.index, isLocked: shape.isLocked,
        props: Object.fromEntries(['geo','color','fill','dash','size','font','align','verticalAlign'].filter(k => shape.props?.[k] !== undefined).map(k => [k,shape.props[k]])), ...(typeof text === 'string' ? { text: text.slice(0,2000), textTruncated: text.length > 2000 } : {}) }
    }),
    bindings: bindings.slice(0,500).map(r => ({ id: r.id, type: r.type, fromId: r.fromId, toId: r.toId, props: r.props })),
    total, offset, nextOffset: offset + selected.length < total ? offset + selected.length : null,
    bindingsTruncated: bindings.length > 500,
  }
}

function state(app, path, reconcile = true) {
  const session = sessionFor(app, path)
  if (!session || session.editor.isDisposed) throw new Error('No CLI Editor session')
  if (reconcile) flushPendingChanges(app, session)
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

function captureSeed(app, seed, bootstrap) {
  // Capture SDK construction data synchronously. The user may close the seed
  // tab during the next await; construction must not depend on its mutable data afterward.
  requireFunctions(seed, ['getContainer'], 'editor')
  return { seed, bootstrap, Editor: seed.constructor,
    ownerDocument: app.workspace.containerEl?.ownerDocument ?? seed.getContainer()?.ownerDocument,
    shapeUtils: Object.values(seed.shapeUtils).filter(u => u && u.constructor.type !== 'group').map(u => u.constructor),
    bindingUtils: Object.values(seed.bindingUtils).filter(Boolean).map(u => u.constructor),
    assetUtils: Object.values(seed.assetUtils).filter(Boolean).map(u => u.constructor),
    tools: Object.values(seed.root.children).map(tool => tool.constructor),
    text: seed.getTextOptions?.() ?? seed.options?.text,
  }
}

async function acquireSeed(app, plugin, file) {
  const candidate = plugin.currTldrawEditor
  if (candidate && !candidate.isDisposed) return captureSeed(app, candidate, 'live-existing-editor')
  requireFunctions(plugin, ['openTldrFile'], 'plugin')
  const leaf = await plugin.openTldrFile(file, 'new-tab', 'tldraw-view')
  const deadline = Date.now() + INITIALIZATION_TIMEOUT_MS
  while (Date.now() < deadline) {
    const seed = plugin.currTldrawEditor
    if (seed && !seed.isDisposed && Object.keys(seed.shapeUtils ?? {}).length) {
      return captureSeed(app, seed, 'opened-existing-view')
    }
    if (leaf && !app.workspace.getLeavesOfType('tldraw-view').includes(leaf)) {
      throw fault('EDITOR_UNAVAILABLE', 'The initialization tab was closed before its Editor became available; retry open when ready')
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
  const plugin = requirePlugin(app)
  requireFunctions(plugin, ['createTldrFile'], 'plugin')
  if (app.vault.getAbstractFileByPath(path)) throw new Error(`File or folder already exists: ${path}`)
  if (sessionsFor(app).has(path)) throw new Error(`Close the existing session before creating: ${path}`)
  const parts = path.split('/')
  const filename = parts.pop()
  const file = await plugin.createTldrFile(filename, { foldername: parts.join('/'), inMarkdown: true })
  try {
    // The plugin's store manager identifies Markdown through Obsidian's
    // metadata cache, which can lag behind vault.create without a GUI tab.
    const deadline = Date.now() + INITIALIZATION_TIMEOUT_MS
    while (typeof plugin.isTldrawFile === 'function' && !plugin.isTldrawFile(file)) {
      if (Date.now() >= deadline) throw new Error('Timed out waiting for Obsidian to recognize the new tldraw note')
      await new Promise(resolve => setTimeout(resolve, 100))
    }
    if (sessionsFor(app).has(file.path)) throw new Error('A session already exists for the created path')
    const result = await open(app, file.path)
    return { ...result, created: true, requestedPath: path, persistence: await saved(app, file.path) }
  } catch (error) {
    // Keep the created note: GUI edits or a delayed save may already exist.
    throw new Error(`Created ${file.path}, but initialization failed: ${errorMessage(error)}. Use open with this path to recover.`)
  }
}

async function open(app, path, currentPageId) {
  if (sessionsFor(app).has(path)) return state(app, path)
  const plugin = requirePlugin(app)
  const file = app.vault.getAbstractFileByPath(path)
  if (!file || file.extension !== 'md') throw new Error('Markdown document required')
  let text = await app.vault.read(file)
  parseMarkdown(text)
  const captured = await acquireSeed(app, plugin, file)
  const { seed, bootstrap, ownerDocument, Editor } = captured
  // A GUI opened for initialization may have edited and saved this note while
  // we waited. Register from fresh Markdown if its GUI store was then closed.
  text = await app.vault.read(file)
  parseMarkdown(text)
  if (ownerDocument?.defaultView?.closed) throw fault('EDITOR_UNAVAILABLE', 'The initialization window was closed; retry open when ready')
  requireFunctions(ownerDocument, ['createElement', 'body.appendChild'], 'editor.container.ownerDocument')
  const session = { path, seed, file, bootstrap, editor: null, registration: null }
  session.container = ownerDocument.createElement('div')
  session.container.className = 'tl-container codex-cli-session-probe'
  session.container.style.cssText = 'position:fixed;left:-10000px;top:0;width:800px;height:600px;pointer-events:none;'
  session.container.ownerDocument.body.appendChild(session.container)
  sessionsFor(app).set(path, session)
  try {
    session.registration = plugin.tlDataDocumentStoreManager.register(
      file, () => text, data => { session.serialized = data }, true
    )
    requireFunctions(session.registration, ['syncToMain', 'unregister'], 'registration')
    session.editor = new Editor({
      store: session.registration.documentStore.store,
      shapeUtils: captured.shapeUtils,
      bindingUtils: captured.bindingUtils,
      assetUtils: captured.assetUtils,
      tools: captured.tools,
      initialState: 'select',
      autoFocus: false,
      options: { text: captured.text },
      getContainer: () => session.container,
      fontAssetUrls: plugin.getFontOverrides(),
    })
    requireEditor(session.editor)
    if (currentPageId) {
      requireFunctions(session.editor, ['getPage', 'setCurrentPage'], 'editor')
      if (!session.editor.getPage(currentPageId)) throw new Error(`Previous page no longer exists: ${currentPageId}`)
      session.editor.setCurrentPage(currentPageId)
    }
    return state(app, path)
  } catch (error) {
    // Initialization can fail because a new plugin lacks a cleanup API too.
    // Still release every resource whose API is available.
    const cleanupErrors = []
    for (const [target, method, args] of [[session.registration, 'syncToMain', [false]],
      [session.editor, 'dispose', []], [session.registration, 'unregister', []], [session.container, 'remove', []]]) {
      try { if (typeof target?.[method] === 'function') target[method](...args) }
      catch (cleanupError) { cleanupErrors.push(errorMessage(cleanupError)) }
    }
    sessionsFor(app).delete(path)
    if (cleanupErrors.length) throw fault(error?.code || 'OPERATION_FAILED', errorMessage(error), 'unknown',
      { ...error?.details, cleanupErrors })
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

function assertRevision(app, session, expected) {
  flushPendingChanges(app, session)
  if (!expected || revision(session.editor) !== expected) throw fault('REVISION_CONFLICT', 'Revision conflict: read state and re-plan before editing', 'not_applied', { expectedRevision: expected ?? null, actualRevision: revision(session.editor) })
}
function editResult(app, path, before, full) {
  const result = state(app, path, false)
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
  assertRevision(app, session, expected)
  if (!Array.isArray(operations) || !operations.length || operations.length > 1000) throw new Error('Batch must contain 1-1000 operations')
  for (const op of operations) {
    if (!op || !methods.has(op.method) || !Array.isArray(op.args)) throw new Error('Unsupported operation')
    requireFunctions(session.editor, [op.method], 'editor')
  }
  const editor = session.editor
  requireEditing(editor)
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
  assertRevision(app, session, expected)
  if (typeof code !== 'string' || !code.trim()) throw new Error('Script is empty')
  const editor = session.editor
  requireEditing(editor)
  // Trusted synchronous code, not a sandbox. A returned Promise is detected only
  // after execution: this check cannot cancel already scheduled work.
  const before = JSON.parse(JSON.stringify(records(editor)))
  const fn = new Function('editor', 'app', 'plugin', 'require', code)
  try { runWithRollback(editor, 'Obsidian tldraw bridge script', () => {
    const result = fn(editor, app, app.plugins.getPlugin('tldraw'), require)
    if (result && typeof result.then === 'function') {
      Promise.resolve(result).catch(() => {})
      throw new Error('Scripts must be synchronous; scheduled work cannot be cancelled')
    }
  })
  } catch (error) {
    throw fault('SCRIPT_FAILED', errorMessage(error), 'unknown', { storeRevision: revision(editor),
      recovery: 'Inspect state; script side effects outside the Store cannot be restored.' })
  }
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
  const group = app.plugins.getPlugin('tldraw')?.tlDataDocumentStoreManager
    ?.storesManager.storeGroupMap.get(session.file.path)
  // A GUI source can have user changes queued until the next animation frame.
  // Publish those before inspecting the dedicated Editor or sending its changes.
  // Read-only/unsynchronized instances must not publish their private state.
  for (const instance of group?.instances ?? []) {
    if (instance.store !== session.editor.store && instance.isSynchronizingToMain()) flush(instance.store)
  }
  flush(session.editor.store)
  if (group?.main.store && group.main.store !== session.editor.store) flush(group.main.store)
}

async function saved(app, path, expectedRevision) {
  const session = sessionFor(app, path)
  if (!session) throw new Error('No session')
  const assertSavedRevision = () => {
    if (expectedRevision && revision(session.editor) !== expectedRevision) {
      throw fault('SAVE_CONFLICT', 'Document changed while saving; inspect the current state before continuing', 'applied',
        { path: session.path, revision: expectedRevision, actualRevision: revision(session.editor),
          recovery: 'Observe current state and check saved; do not reapply this edit.' })
    }
  }
  const deadline = Date.now() + 10000
  while (Date.now() < deadline) {
    flushPendingChanges(app, session)
    assertSavedRevision()
    const text = await app.vault.read(session.file)
    flushPendingChanges(app, session)
    assertSavedRevision()
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
    return {vault: app.vault.getName(), ...pluginSupport(plugin),
      documents: [...sessionsFor(app).keys()]}
  }
  if (action === 'capabilities') return capabilities(app)
  if (action === 'observe') return observe(app, args)
  if (action === 'create') return create(app, args.path)
  if (action === 'open') return open(app, args.path, args.currentPageId)
  if (action === 'state') return state(app, args.path)
  if (action === 'apply') {
    if (args.pageId !== undefined && args.pageId !== sessionFor(app,args.path).editor.getCurrentPageId()) {
      throw fault('PAGE_CONFLICT', 'Current page changed; observe again before editing')
    }
    args = { ...args, operations: namedOperations(args.operations) }
    action = 'batch'
  }
  if (action === 'batch' || action === 'script') {
    let result
    try {
      result = action === 'batch' ? batch(app,args.path,args.operations,args.revision,args.full) : script(app,args.path,args.code,args.revision,args.full)
    } catch (error) {
      if (error?.code) throw error
      const unchanged = revision(sessionFor(app,args.path).editor) === args.revision
      throw fault('OPERATION_FAILED', errorMessage(error), unchanged ? 'not_applied' : 'unknown')
    }
    try {
      return {...result, persistence: await saved(app,args.path,result.revision)}
    } catch (error) {
      if (error?.code === 'SAVE_CONFLICT') throw error
      throw fault('SAVE_UNCONFIRMED', errorMessage(error), 'applied', { path: args.path, revision: result.revision,
        currentPageId: result.currentPageId, changes: result.changes, recovery: 'Inspect state and saved; do not reapply the edit.' })
    }
  }
  if (action === 'saved') return saved(app, args.path)
  if (action === 'close') {
    await saved(app, args.path)
    return close(app, args.path)
  }
  if (action === 'preview') {
    const session = sessionFor(app, args.path)
    flushPendingChanges(app, session)
    if (args.revision) assertRevision(app, session,args.revision)
    const editor = session.editor
    requireFunctions(editor, ['toImage'], 'editor')
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
    flushPendingChanges(app, session)
    if (revision(editor) !== capturedRevision) throw fault('REVISION_CONFLICT', 'Revision conflict during preview: read state and export again')
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
      if (queue.get(id).request !== request) throw fault('REQUEST_ID_REUSED', 'Job id already used for another request')
      return JSON.stringify(queue.get(id))
    }
    if ([...queue.values()].some(job => job.status === 'running')) throw fault('RUNTIME_BUSY', 'CLI job still running')
    if (queue.size >= MAX_JOBS) throw fault('RECEIPT_CAPACITY', 'Receipt capacity reached: use the CLI forget command to release completed request ids')
    const job = { id, request, status: 'running' }
    queue.set(id, job)
    Promise.resolve().then(() => execute(app, action, args)).then(
      result => { job.result = result; job.status = 'complete' },
      error => { job.status = 'failed'; job.error = errorMessage(error); job.failure = failureInfo(error, action === 'create' ? 'unknown' : 'not_applied') }
    )
    return JSON.stringify(job)
  },
  poll(app, id) {
    const job = jobs.get(app)?.get(id)
    if (!job) throw fault('REQUEST_NOT_FOUND', 'Unknown CLI job', 'unknown')
    return JSON.stringify(job)
  },
  forget(app, id) {
    const job = jobs.get(app)?.get(id)
    if (job?.status === 'running') throw fault('RUNTIME_BUSY', 'CLI job still running')
    return JSON.stringify({ forgotten: jobs.get(app)?.delete(id) ?? false })
  },
}
