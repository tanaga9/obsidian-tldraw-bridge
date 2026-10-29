const arrows=editor.store.allRecords().filter(r=>r.typeName==='shape'&&r.type==='arrow');
const issues=[];
for(const a of arrows){const bs=editor.getBindingsFromShape(a,'arrow');if(bs.length!==2)issues.push(a.id+': binding count '+bs.length);for(const b of bs)if(!editor.getShape(b.toId))issues.push(a.id+': missing target');const parent=editor.getShape(a.parentId);if(!parent||parent.type!=='frame')issues.push(a.id+': not in frame');}
const iso=['center','edge-point','edge','none'].map(snap=>{const a=editor.getShape('shape:isolate-'+snap+'-arrow');const v=editor.getShapeUtil(a).getGeometry(a).vertices;const base=v[0];return {snap,relativeVertices:v.map(p=>({x:p.x-base.x,y:p.y-base.y}))};});
return {arrowCount:arrows.length,bindingCount:arrows.reduce((n,a)=>n+editor.getBindingsFromShape(a,'arrow').length,0),pageCount:editor.getPages().length,issues,isolation:iso,allIsolationPathsEqual:iso.every(x=>JSON.stringify(x.relativeVertices)===JSON.stringify(iso[0].relativeVertices))};
