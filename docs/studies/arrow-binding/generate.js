// Trusted synchronous Obsidian Tldraw Bridge script.
// Run once on a fresh note; see README.md for the reproduction procedure.
// Each phase retains the originally inspected construction and layout edits.
const pages = editor.getPages();
if (pages.length !== 1 || pages[0].id !== 'page:page' ||
    editor.store.allRecords().some(r => r.typeName === 'shape' || r.typeName === 'binding')) {
  throw new Error('Use a fresh empty note with initial page ID page:page.');
}

function buildBaseline() {
  const rt=s=>({type:'doc',content:[{type:'paragraph',content:s?[{type:'text',text:s}]:[]}]});
  const cases=[];
  function page(id,name,w,h){if(id==='page:page')editor.updatePage({id,name});else editor.createPage({id,name});editor.setCurrentPage(id);const f='shape:f-'+id.slice(5);editor.createShapes([{id:f,type:'frame',x:0,y:0,props:{w,h,name}}]);return f;}
  function text(id,parent,x,y,s,w=450,size='s'){editor.createShapes([{id:'shape:'+id,type:'text',parentId:parent,x,y,props:{richText:rt(s),font:'sans',size,w,autoSize:false}}]);}
  function card(parent,id,x,y,title,kind,startProps,endProps,stage='initial',self=false){
   text(id+'-title',parent,x,y,title,465);
   const a='shape:'+id+'-a',b=self?a:'shape:'+id+'-b',ar='shape:'+id+'-arrow';
   editor.createShapes([{id:a,type:'geo',parentId:parent,x:x+20,y:y+70,props:{w:180,h:60,richText:rt('Source'),font:'sans',size:'s',dash:'solid',fill:'none'}}]);
   if(!self)editor.createShapes([{id:b,type:'geo',parentId:parent,x:x+255,y:y+170,props:{w:180,h:60,richText:rt('Target'),font:'sans',size:'s',dash:'solid',fill:'none'}}]);
   editor.createShapes([{id:ar,type:'arrow',parentId:parent,x:0,y:0,props:{kind,bend:self?-110:0,dash:'solid',size:'m',font:'mono',start:{x:x+110,y:y+100},end:{x:x+345,y:y+200}}}]);
   editor.createBindings([{id:'binding:'+id+'-s',type:'arrow',fromId:ar,toId:a,props:{terminal:'start',...startProps}},{id:'binding:'+id+'-e',type:'arrow',fromId:ar,toId:b,props:{terminal:'end',...endProps}}]);
   if(stage==='moved')editor.updateShapes([{id:b,type:'geo',x:x+255,y:y+45}]);
   if(stage==='resized')editor.updateShapes([{id:b,type:'geo',props:{w:235,h:110}}]);
   cases.push({id,arrow:ar,source:a,target:b,stage,kind});
  }
  const center={isPrecise:false,isExact:false,normalizedAnchor:{x:.5,y:.5},snap:'none'};
  const sideS={isPrecise:true,isExact:false,normalizedAnchor:{x:1,y:.5},snap:'none'},sideE={...sideS,normalizedAnchor:{x:0,y:.5}};
  let f=page('page:page','arc-center-vs-side',1500,1050);
  text('arc-head',f,25,15,'ARC: whole-node connection vs side midpoint',1400,'l');
  text('arc-sub',f,25,65,'Same 180 x 60 nodes. Columns: initial / moved / resized. Each variant is edited through the SDK.',1420);
  ['initial','moved','resized'].forEach((stage,i)=>{card(f,'arc-center-'+stage,20+i*495,130,'Center aim / '+stage,'arc',center,center,stage);card(f,'arc-side-'+stage,20+i*495,560,'Side midpoint / '+stage,'arc',sideS,sideE,stage);});
  f=page('page:exact','arc-precise-exact',1020,920);text('exact-head',f,25,15,'ARC: precise / exact combinations',960,'l');text('exact-sub',f,25,65,'Same off-center anchors: source (0.8, 0.25), target (0.2, 0.75).',960);
  for(let p=0;p<2;p++)for(let e=0;e<2;e++){let s={isPrecise:!!p,isExact:!!e,normalizedAnchor:{x:.8,y:.25},snap:'none'},t={...s,normalizedAnchor:{x:.2,y:.75}};card(f,`exact-${p}-${e}`,20+e*500,125+p*380,`precise=${!!p} / exact=${!!e}`,'arc',s,t);}
  f=page('page:elbow','elbow-patterns',1500,1620);text('elbow-head',f,25,15,'ELBOW: practical attachment patterns',1400,'l');text('elbow-sub',f,25,65,'Columns: initial / target moved above source / target resized. exact=false throughout.',1430);
  const pats=[['center',center,center],['edge-point',{...sideS,snap:'edge-point'},{...sideE,snap:'edge-point'}],['edge',{...sideS,snap:'edge',normalizedAnchor:{x:1,y:.8}},{...sideE,snap:'edge',normalizedAnchor:{x:0,y:.2}}],['none / interior',{...sideS,normalizedAnchor:{x:.8,y:.3}},{...sideE,normalizedAnchor:{x:.2,y:.7}}]];
  pats[0][1]={...center,snap:'center'};pats[0][2]={...center,snap:'center'};
  pats.forEach(([name,s,t],r)=>['initial','moved','resized'].forEach((stage,c)=>card(f,'elbow-'+r+'-'+stage,20+c*495,130+r*365,name+' / '+stage,'elbow',s,t,stage)));
  f=page('page:isolate','snap-isolation',1020,920);text('iso-head',f,25,15,'ELBOW: change only snap',960,'l');text('iso-sub',f,25,65,'precise=true, exact=false, same interior anchors in all four cases.',960);
  ['center','edge-point','edge','none'].forEach((snap,i)=>card(f,'isolate-'+snap,20+(i%2)*500,125+Math.floor(i/2)*380,'snap='+snap,'elbow',{...sideS,snap,normalizedAnchor:{x:.8,y:.3}},{...sideE,snap,normalizedAnchor:{x:.2,y:.7}}));
  f=page('page:loops','self-loop-patterns',1020,1250);text('loop-head',f,25,15,'SELF LOOPS: separate entry and exit',960,'l');text('loop-sub',f,25,65,'Each arrow binds both terminals to one 180 x 60 node.',960);
  const lp=[['arc / separate sides','arc',{...sideS,normalizedAnchor:{x:1,y:.5}},{...sideE,normalizedAnchor:{x:.5,y:0}}],['elbow / edge-point','elbow',{...sideS,snap:'edge-point'},{...sideE,snap:'edge-point',normalizedAnchor:{x:.5,y:0}}],['elbow / edge','elbow',{...sideS,snap:'edge',normalizedAnchor:{x:1,y:.75}},{...sideE,snap:'edge',normalizedAnchor:{x:.3,y:0}}],['elbow / center','elbow',{...center,snap:'center'},{...center,snap:'center'}],['elbow / none','elbow',sideS,{...sideE,normalizedAnchor:{x:.5,y:0}}],['elbow / exact interior','elbow',{...sideS,isExact:true,normalizedAnchor:{x:.8,y:.3}},{...sideE,isExact:true,normalizedAnchor:{x:.2,y:.7}}]];
  lp.forEach(([name,k,s,t],i)=>card(f,'loop-'+i,20+(i%2)*500,145+Math.floor(i/2)*350,name,k,s,t,'initial',true));
  editor.setCurrentPage('page:page');
  return {cases, pages:editor.getPages().map(p=>({id:p.id,name:p.name}))};
}

function addReversalAndUseCases() {
  const rt=s=>({type:'doc',content:[{type:'paragraph',content:s?[{type:'text',text:s}]:[]}]});
  editor.updateShapes([{id:'shape:f-page',type:'frame',props:{w:1560}},{id:'shape:f-elbow',type:'frame',props:{w:1560}}]);
  function page(id,name,w,h){editor.createPage({id,name});editor.setCurrentPage(id);let f='shape:f-'+id.slice(5);editor.createShapes([{id:f,type:'frame',props:{name,w,h}}]);return f;}
  function tx(id,f,x,y,s,w=460,size='s'){editor.createShapes([{id:'shape:'+id,type:'text',parentId:f,x,y,props:{richText:rt(s),font:'sans',size,w,autoSize:false}}]);}
  function node(id,f,x,y,label,w=180,h=60){editor.createShapes([{id:'shape:'+id,type:'geo',parentId:f,x,y,props:{w,h,richText:rt(label),font:'sans',size:'s',dash:'solid'}}]);}
  function arrow(id,f,a,b,sp,ep,kind='elbow'){let ar='shape:'+id;editor.createShapes([{id:ar,type:'arrow',parentId:f,props:{kind,dash:'solid',size:'m',start:{x:0,y:0},end:{x:100,y:100}}}]);editor.createBindings([{id:'binding:'+id+'-s',type:'arrow',fromId:ar,toId:'shape:'+a,props:{terminal:'start',...sp}},{id:'binding:'+id+'-e',type:'arrow',fromId:ar,toId:'shape:'+b,props:{terminal:'end',...ep}}]);}
  let f=page('page:reversal','elbow-reversal',1500,1620);tx('rev-head',f,25,15,'ELBOW: direction reversal and vertical placement',1420,'l');tx('rev-sub',f,25,65,'Columns: target moved to left / directly below / below and overlapping horizontally.',1420);
  const center={isPrecise:false,isExact:false,normalizedAnchor:{x:.5,y:.5},snap:'center'};
  const fixed={isPrecise:true,isExact:false,normalizedAnchor:{x:1,y:.5},snap:'edge-point'};
  const patterns=[['center',center,center],['edge-point',fixed,{...fixed,normalizedAnchor:{x:0,y:.5}}],['edge',{...fixed,snap:'edge',normalizedAnchor:{x:1,y:.8}},{...fixed,snap:'edge',normalizedAnchor:{x:0,y:.2}}],['none / interior',{...fixed,snap:'none',normalizedAnchor:{x:.8,y:.3}},{...fixed,snap:'none',normalizedAnchor:{x:.2,y:.7}}]];
  patterns.forEach(([name,s,t],r)=>{for(let c=0;c<3;c++){const id=`rev-${r}-${c}`,x=20+c*495,y=135+r*365;tx(id+'-title',f,x,y,name);node(id+'a',f,x+20,y+70,'Source');node(id+'b',f,x+255,y+170,'Target');arrow(id,f,id+'a',id+'b',s,t);if(c===0)editor.updateShapes([{id:'shape:'+id+'a',type:'geo',x:x+255},{id:'shape:'+id+'b',type:'geo',x:x+20,y:y+170}]);else editor.updateShapes([{id:'shape:'+id+'b',type:'geo',x:x+(c===1?20:100),y:y+200}]);}});
  f=page('page:usecases','recommended-use-cases',1100,1370);tx('use-head',f,25,15,'Intent-based combinations',1020,'l');
  tx('use-a',f,25,85,'A. Separate multiple connections on the same edge',1020);
  node('multi-target',f,650,180,'Service',280,260);
  [0,1,2].forEach(i=>{node('multi-source'+i,f,80,160+i*120,'Input '+(i+1));arrow('multi-arrow'+i,f,'multi-source'+i,'multi-target',fixed,{...fixed,snap:'edge',normalizedAnchor:{x:0,y:.2+i*.3}});});
  tx('use-b',f,25,565,'B. Return route: explicit top-to-top attachment',1020);
  node('return-a',f,100,725,'Earlier step',240);node('return-b',f,650,725,'Later step',240);
  const top={...fixed,normalizedAnchor:{x:.5,y:0}};arrow('return-arrow',f,'return-b','return-a',top,top);
  tx('use-c',f,25,890,'C. Point to an internal location: exact only at the target',1020);
  node('leader-source',f,80,1040,'Annotation',200);node('leader-target',f,650,1010,'Detail',300,160);
  arrow('leader-arrow',f,'leader-source','leader-target',{...center,snap:'none'},{...fixed,snap:'none',isExact:true,normalizedAnchor:{x:.25,y:.75}},'arc');
  // Mark the actual point with a small dot; it has no binding role.
  editor.createShapes([{id:'shape:leader-point',type:'geo',parentId:f,x:720,y:1125,props:{geo:'ellipse',w:10,h:10,fill:'fill',color:'black',dash:'solid'}}]);
  editor.setCurrentPage('page:page');
  return {arrowCount: editor.store.allRecords().filter(r => r.typeName === 'shape' && r.type === 'arrow').length};
}

function addPortCasesAndFinishLayout() {
  editor.setCurrentPage('page:reversal');
  editor.updateShapes([...editor.getCurrentPageShapes()].filter(s=>s.parentId==='shape:f-reversal').map(s=>({id:s.id,type:s.type,x:s.x+40})));
  editor.updateShapes([{id:'shape:f-reversal',type:'frame',props:{w:1580}}]);
  const rt=s=>({type:'doc',content:[{type:'paragraph',content:[{type:'text',text:s}]}]});
  editor.createPage({id:'page:ports',name:'exact-at-outline'});editor.setCurrentPage('page:ports');
  editor.createShapes([{id:'shape:f-ports',type:'frame',props:{w:1100,h:950,name:'exact-at-outline'}}]);
  const tx=(id,x,y,s,w=1020,size='s')=>editor.createShapes([{id:'shape:'+id,type:'text',parentId:'shape:f-ports',x,y,props:{richText:rt(s),font:'sans',w,autoSize:false,size}}]);
  tx('ports-head',25,15,'EXACT: deliberate contact at an outline port',1020,'l');tx('ports-sub',25,65,'Same side-midpoint anchors. Columns: exact=false / exact=true. precise=true throughout.');
  ['arc','elbow'].forEach((kind,r)=>[false,true].forEach((exact,c)=>{const id=`port-${r}-${c}`,x=25+c*535,y=150+r*350;tx(id+'label',x,y,kind+' / exact='+exact,490);editor.createShapes([{id:'shape:'+id+'a',type:'geo',parentId:'shape:f-ports',x:x+20,y:y+100,props:{w:180,h:60,richText:rt('Source'),font:'sans',dash:'solid',size:'s'}},{id:'shape:'+id+'b',type:'geo',parentId:'shape:f-ports',x:x+280,y:y+100,props:{w:180,h:60,richText:rt('Target'),font:'sans',dash:'solid',size:'s'}},{id:'shape:'+id,type:'arrow',parentId:'shape:f-ports',props:{kind,dash:'solid',start:{x:0,y:0},end:{x:100,y:100}}}]);editor.createBindings(['start','end'].map((terminal,i)=>({id:'binding:'+id+terminal,type:'arrow',fromId:'shape:'+id,toId:'shape:'+id+(i?'b':'a'),props:{terminal,isPrecise:true,isExact:exact,snap:kind==='arc'?'none':'edge-point',normalizedAnchor:{x:i?0:1,y:.5}}})));}));
  editor.setCurrentPage('page:page');
  return {arrowCount:editor.store.allRecords().filter(r=>r.typeName==='shape'&&r.type==='arrow').length};
}

buildBaseline();
addReversalAndUseCases();
addPortCasesAndFinishLayout();
return {
  arrowCount: editor.store.allRecords().filter(r => r.typeName === 'shape' && r.type === 'arrow').length,
  pageCount: editor.getPages().length,
};
