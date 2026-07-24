const fs = require('fs');
const vm = require('vm');

const html = fs.readFileSync('/Users/fsw/WorkBuddy/2026-07-15-08-51-27/vendor/product-sales.html','utf8');
// extract all <script>...</script> blocks
const re = /<script>([\s\S]*?)<\/script>/g;
let m, scripts = [];
while((m = re.exec(html))) scripts.push(m[1]);
console.log('script blocks found:', scripts.length);

// ---- DOM shim ----
function makeEl(){
  const el = {
    _html:'', _text:'', value:'', style:{}, dataset:{},
    classList:{ _s:new Set(), toggle(c,f){ if(f===undefined){ this._s.has(c)?this._s.delete(c):this._s.add(c);} else { f?this._s.add(c):this._s.delete(c);} }, add(c){this._s.add(c);}, remove(c){this._s.delete(c);}, contains(c){return this._s.has(c);} },
    addEventListener(){}, removeEventListener(){},
    querySelector(){ return makeEl(); },
    querySelectorAll(){ return []; },
    appendChild(){}, setAttribute(){}, getAttribute(){return null;},
    requestFullscreen(){}, focus(){}
  };
  Object.defineProperty(el,'innerHTML',{get(){return el._html;},set(v){el._html=String(v);}});
  Object.defineProperty(el,'textContent',{get(){return el._text;},set(v){el._text=String(v);}});
  return el;
}
const cache = new Map();
function qs(sel){ if(!cache.has(sel)) cache.set(sel, makeEl()); return cache.get(sel); }

const document = {
  readyState:'complete',
  body: makeEl(),
  documentElement: makeEl(),
  querySelector: qs,
  querySelectorAll: ()=>[],
  addEventListener(){}, removeEventListener(){},
  getElementById(id){ return qs('#'+id); },
  exitFullscreen(){}, fullscreenElement:null
};
const localStorageData = {};
const localStorage = { getItem(k){return k in localStorageData?localStorageData[k]:null;}, setItem(k,v){localStorageData[k]=String(v);}, removeItem(k){delete localStorageData[k];} };
const windowObj = { parent:null, addEventListener(){}, postMessage(){}, requestFullscreen(){} };
windowObj.parent = windowObj;
const location = { search:'' };
function prompt(){ return 'test-view'; }
function alert(){}

const sandbox = {
  document, window:windowObj, localStorage, location, prompt, alert,
  URLSearchParams, JSON, Math, Date, console, setTimeout:()=>{}, RegExp, parseInt, parseFloat, isNaN,
  requestAnimationFrame:()=>{}
};
sandbox.window = windowObj;
sandbox.globalThis = sandbox;

try {
  for(const code of scripts){ vm.runInNewContext(code, sandbox, {filename:'block.js'}); }
  // inspect rendered output
  const kpis = qs('#kpis')._html;
  const raw = qs('#raw-body')._html;
  const board = qs('#boardList')._html;
  const rel = qs('#relNote')._html;
  console.log('KPI html len:', kpis.length, '| has stat:', kpis.includes('stat'));
  console.log('boardList len:', board.length, '| has src-card:', board.includes('src-card'));
  console.log('raw-body len:', raw.length, '| data-row count:', (raw.match(/data-row/g)||[]).length, '| d-tag present:', raw.includes('d-tag'));
  console.log('relNote:', rel.slice(0,60));
  console.log('SMOKE TEST PASS');
} catch(e){
  console.error('SMOKE TEST FAIL:', e && e.stack ? e.stack : e);
  process.exit(1);
}
