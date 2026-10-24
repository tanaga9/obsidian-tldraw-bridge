#!/usr/bin/env node
'use strict'
// Repository-only, read-only review. The bundled runtime supplies the same logic
// used by language-status; no Obsidian connection or translation model is needed.
const fs = require('node:fs')
const path = require('node:path')
const {execFileSync} = require('node:child_process')
const {parseMarkdown, reviewLanguages} = require('../src/obsidian_tldraw_bridge/runtime/bridge.cjs')
const options = process.argv.slice(2)
if (options.includes('--help')) {
  process.stdout.write('Usage: node scripts/review_translations.cjs [--staged|--worktree] [--strict] [paths...]\nDefaults: inspect changed index and working-tree Markdown; report only. --strict exits 2 for review items.\n')
  process.exit(0)
}
const unknown = options.filter(a => a.startsWith('--') && !['--staged','--worktree','--strict'].includes(a))
if (unknown.length || (options.includes('--staged') && options.includes('--worktree'))) {
  process.stderr.write('Choose --staged or --worktree, or neither for both. Unknown options are rejected.\n'); process.exit(1)
}
const git = (...args) => execFileSync('git',args,{encoding:'utf8',maxBuffer:64*1024*1024,stdio:['ignore','pipe','pipe']})
const startMarker='```json !!!_START_OF_TLDRAW_DATA__DO_NOT_CHANGE_THIS_PHRASE_!!!'
function changedDiagrams(before, after) {
  const beforeDoc = before.find(r=>r.typeName==='document')?.meta?.multilingualDiagrams
  const afterDoc = after.find(r=>r.typeName==='document')?.meta?.multilingualDiagrams
  if (JSON.stringify(beforeDoc)!==JSON.stringify(afterDoc)) return null
  const left = new Map(before.map(r=>[r.id,r])), right = new Map(after.map(r=>[r.id,r]))
  const ids = new Set()
  function owner(map, record) {
    if (!record) return
    if (record.typeName==='asset') {
      for (const r of map.values()) if (r.typeName==='shape' && r.props?.assetId===record.id) owner(map,r)
      return
    }
    if (record.typeName==='binding') record=map.get(record.fromId)
    const visited=new Set()
    while(record && record.typeName!=='page' && !visited.has(record.id)) {visited.add(record.id);record=map.get(record.parentId)}
    if (record?.meta?.diagramId) ids.add(record.meta.diagramId)
  }
  for (const id of new Set([...left.keys(),...right.keys()])) {
    if (JSON.stringify(left.get(id))!==JSON.stringify(right.get(id))) {owner(left,left.get(id));owner(right,right.get(id))}
  }
  return ids
}
function baselineRecords(text) {
  if (!text || !text.includes(startMarker)) return []
  return parseMarkdown(text).raw.records
}
try {
  const root=git('rev-parse','--show-toplevel').trim()
  process.chdir(root)
  const paths=options.filter(a=>!a.startsWith('--'))
  for (const p of paths) if (path.isAbsolute(p)||p.split(/[\\/]/).includes('..')) throw new Error('Use repository-relative paths without traversal')
  const versions=options.includes('--staged')?['index']:options.includes('--worktree')?['worktree']:['index','worktree']
  const reports=[], errors=[]
  const indexPaths=new Set(git('ls-files','-z').split('\0').filter(Boolean))
  for (const version of versions) {
    const selection = paths.length ? paths : [...new Set([
      ...git('diff',...(version==='index'?['--cached']:[]),'--name-only','-z','--no-renames','--diff-filter=ACMR','--','*.md').split('\0').filter(Boolean),
      ...(version==='worktree'?git('ls-files','--others','--exclude-standard','-z','--','*.md').split('\0').filter(Boolean):[]),
    ])]
    for (const filename of selection.filter(p=>p.endsWith('.md'))) {
      if (version==='index' && !indexPaths.has(filename)) continue
      try {
        const text=version==='index'?git('show',':'+filename):fs.readFileSync(filename,'utf8')
        let prior=''
        try {prior=git('show',(version==='index'?'HEAD:':':')+filename)} catch (_) { /* New file; inspect every registered group. */ }
        if (!text.includes(startMarker)) {
          if (prior.includes(startMarker) || text.includes('!!!_END_OF_TLDRAW_DATA__DO_NOT_CHANGE_THIS_PHRASE_!!!')) {
            throw new Error('Missing tldraw start marker; inspect the damaged Note or intentional format removal')
          }
          continue
        }
        const values=parseMarkdown(text).raw.records
        let before, baselineWarning
        try {before=baselineRecords(prior)}
        catch (error) {
          // A repaired current Note must remain reviewable. Without a readable
          // prior blob, inspect every current group instead of narrowing scope.
          baselineWarning=`Previous Note could not be parsed (${error.message}); inspected all current diagrams`
        }
        const scope=before===undefined?null:changedDiagrams(before,values)
        if (scope && !scope.size) continue
        const checked=scope?[...scope].map(id=>reviewLanguages(values,id)):[reviewLanguages(values)]
        const diagrams=checked.flatMap(r=>r.diagrams), issues=checked.flatMap(r=>r.errors)
        if (!diagrams.length && !issues.length && !baselineWarning) continue
        reports.push({path:filename,version,diagrams,errors:issues,requiresReview:checked.some(r=>r.requiresReview),
          ...(baselineWarning?{baselineWarning}:{})})
      } catch (error) {errors.push({path:filename,version,message:error.message})}
    }
  }
  const requiresReview=errors.length>0||reports.some(r=>r.requiresReview)
  process.stdout.write(JSON.stringify({reports,errors,requiresReview,policy:'report-only; translate/apply only on explicit user request'},null,2)+'\n')
  process.exitCode=errors.length?1:options.includes('--strict')&&requiresReview?2:0
} catch (error) {process.stderr.write(JSON.stringify({error:error.message})+'\n');process.exitCode=1}
