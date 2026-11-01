'use strict'
const { test } = require('node:test')
const assert = require('node:assert/strict')
const fs = require('node:fs')
const vm = require('node:vm')
const path = require('node:path')
const source = fs.readFileSync(path.join(__dirname, '../src/obsidian_tldraw_bridge/runtime/bridge.cjs'), 'utf8')
const context = { require, module: {exports: {}}, Buffer, setTimeout }
vm.runInNewContext(source + '\nmodule.exports.test = {formatText,setTextList,separateArrowLabel,namedOperations};', context)
const api = context.module.exports.test
const copy = value => JSON.parse(JSON.stringify(value))
const text = (value, marks = []) => ({type:'text',text:value,...(marks.length ? {marks} : {})})
const paragraph = (...content) => ({type:'paragraph',content})
function editorFor(content) {
  const shape = {id:'shape:a',type:'geo',props:{richText:{type:'doc',content},color:'blue'}}
  return {shape,getShape:id=>id===shape.id?shape:undefined,updateShapes:updates=>{
    for(const update of updates) Object.assign(shape.props,update.props)
  }}
}
function format(editor, text, marks, extra = {}) {
  const op = {op:'formatText',id:'shape:a',text,marks,...extra}
  api.namedOperations([op])
  api.formatText(editor,op)
}
test('partial formatting spans existing marks and preserves other text, attributes, and emoji', () => {
  const link = {type:'link',attrs:{href:'https://example.com',target:'_blank'}}
  const e=editorFor([paragraph(text('前😀 '),text('rea',[link]),text('dy!',[{type:'italic'}]))])
  format(e,'ready',{bold:true,highlight:true})
  assert.deepEqual(copy(e.shape.props.richText.content[0].content),[
    text('前😀 '),text('rea',[link,{type:'bold'},{type:'highlight'}]),
    text('dy',[{type:'italic'},{type:'bold'},{type:'highlight'}]),text('!',[{type:'italic'}])])
  assert.equal(e.shape.props.color,'blue')
  format(e,'rea',{bold:false})
  assert.deepEqual(copy(e.shape.props.richText.content[0].content[1].marks),[link,{type:'highlight'}])
})
test('ambiguous or absent matches reject without modifying records; occurrence is explicit', () => {
  const e=editorFor([paragraph(text('same same'))]), before=copy(e.shape)
  for(const phrase of ['same','missing']) assert.throws(()=>format(e,phrase,{bold:true}),error=>error.code==='TEXT_MATCH_FAILED')
  assert.deepEqual(e.shape,before)
  format(e,'same',{code:true},{occurrence:2})
  assert.deepEqual(copy(e.shape.props.richText.content[0].content),[text('same '),text('same',[{type:'code'}])])
})
test('matches cross paragraphs and list items without removing structure', () => {
  const e=editorFor([paragraph(text('one')), {type:'bulletList',content:[{type:'listItem',content:[paragraph(text('two'))]}]}])
  format(e,'one\ntwo',{italic:true})
  assert.equal(e.shape.props.richText.content[1].type,'bulletList')
  assert.equal(e.shape.props.richText.content[1].content[0].content[0].content[0].marks[0].type,'italic')
})
test('list conversion preserves inline content and rejects nested/unsupported blocks', () => {
  const original=[paragraph(text('One',[{type:'bold'}])),paragraph(text('Two'))]
  const e=editorFor(copy(original))
  api.setTextList(e,{id:'shape:a',list:'bullet'})
  assert.equal(e.shape.props.richText.content[0].content.length,2)
  api.setTextList(e,{id:'shape:a',list:'none'})
  assert.deepEqual(copy(e.shape.props.richText.content),original)
  const nested=editorFor([{type:'bulletList',content:[{type:'listItem',content:[paragraph(text('one')),{type:'bulletList',content:[]}]}]}])
  const before=copy(nested.shape)
  assert.throws(()=>api.setTextList(nested,{id:'shape:a',list:'none'}))
  assert.deepEqual(nested.shape,before)
})
test('operation schema rejects invalid marks, ids, occurrence and extra fields', () => {
  const base={op:'formatText',id:'shape:a',text:'a',marks:{bold:true}}
  for(const extra of [{marks:{}},{marks:{link:true}},{marks:{bold:'yes'}},{occurrence:0},{occurrence:1.5},{id:'a'},{ignored:true}]) {
    assert.throws(()=>api.namedOperations([{...base,...extra}]),error=>error.code==='INVALID_INPUT')
  }
  const separate={op:'separateArrowLabel',id:'shape:a',labelId:'shape:label',x:0,y:0,width:100}
  for(const extra of [{x:NaN},{y:'1'},{width:0},{width:-1},{width:Infinity}]) {
    assert.throws(()=>api.namedOperations([{...separate,...extra}]),error=>error.code==='INVALID_INPUT')
  }
  const e=editorFor([paragraph(text('a'))]);e.shape.isLocked=true
  assert.throws(()=>format(e,'a',{bold:true}))
})
test('separate arrow label uses explicit placement and preserves effective font size and source props', () => {
  const arrow={id:'shape:a',type:'arrow',parentId:'shape:frame',x:100,y:200,rotation:Math.PI/2,opacity:.8,
    props:{richText:{type:'doc',content:[paragraph(text('label',[{type:'bold'}]))]},start:{x:0,y:0},end:{x:300,y:0},font:'mono',size:'m',labelColor:'blue',scale:2}}
  const before=copy(arrow), values=new Map([[arrow.id,arrow]])
  const e={getShape:id=>values.get(id),createShapes:shapes=>shapes.forEach(s=>values.set(s.id,copy(s))),
    getCurrentTheme:()=>({}),getColorMode:()=> 'light',
    getShapeUtil:shape=>({options:{getDefaultDisplayValues:()=>shape.type==='arrow'?{labelFontSize:20}:{fontSize:24},getCustomDisplayValues:()=>({})}}),
    updateShapes:updates=>updates.forEach(u=>{const s=values.get(u.id); if(u.props)Object.assign(s.props,u.props);for(const k of ['x','y'])if(k in u)s[k]=u[k]}),
  }
  const op={id:arrow.id,labelId:'shape:label',x:192,y:300,width:100}
  api.separateArrowLabel(e,op)
  const label=values.get('shape:label')
  assert.deepEqual(label.props.richText,before.props.richText)
  assert.equal(label.parentId,arrow.parentId)
  assert.equal(label.rotation,arrow.rotation)
  assert.equal(label.props.scale,2*20/24)
  assert.equal(label.props.w*label.props.scale,100)
  assert.equal(label.props.scale*24,2*20)
  assert.equal(label.props.textAlign,'start')
  assert.equal(label.x,192)
  assert.equal(label.y,300)
  assert.deepEqual(copy(arrow.props),{...before.props,richText:{type:'doc',content:[{type:'paragraph'}]}})
  assert.throws(()=>api.separateArrowLabel(e,op))
})
