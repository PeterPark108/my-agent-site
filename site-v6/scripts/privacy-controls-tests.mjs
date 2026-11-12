import assert from 'node:assert/strict';import fs from 'node:fs';import vm from 'node:vm';
const source=fs.readFileSync('public/js/config.js','utf8');
const bridge=source.slice(source.indexOf('/* Restore production privacy controls'));
const events={},changes=[];let button,state;
function fresh(){button={hidden:true,dataset:{},listeners:[],addEventListener(t,fn){this.listeners.push(fn)}};state={textContent:'Đo lường đang tắt trong phiên bản preview.'};}
fresh();const w={MYAGENT_GA:{blocked:false,optedOut:false,set:v=>changes.push(v)},addEventListener:(t,f)=>events[t]=f};const d={querySelector:s=>s==='[data-ga-toggle]'?button:state};
vm.runInNewContext(bridge,{window:w,document:d});assert.equal(button.hidden,false);
button.hidden=true;state.textContent='preview';events['myagent:tools-ready']();assert.equal(button.hidden,false);assert.match(state.textContent,/Đang bật/);
assert.equal(button.listeners.length,1);button.listeners[0]();assert.equal(w.MYAGENT_GA.optedOut,true);assert.deepEqual(changes,[true]);assert.match(state.textContent,/Đang tắt/);
fresh();events['myagent:tools-ready']();assert.equal(button.hidden,false);assert.match(button.textContent,/Bật lại/);button.listeners[0]();assert.deepEqual(changes,[true,false]);
w.MYAGENT_GA.blocked=true;events['myagent:tools-ready']();assert.equal(button.hidden,true);assert.match(state.textContent,/riêng tư/);
vm.runInNewContext(bridge,{window:w,document:d});assert.equal(button.listeners.length,1);assert.equal(fs.readFileSync('../js/config.js','utf8'),source);
console.log('PASS: tools-ready restores production toggle after preview override; SPA rebinding, opt-out/in, DNT and singleton handlers.');
