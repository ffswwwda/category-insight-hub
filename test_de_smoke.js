// DOM-shim smoke test for de-dashboard.html
const fs = require('fs');
const vm = require('vm');

const html = fs.readFileSync('de-dashboard.html', 'utf8');
// extract all <script> blocks
const scripts = [];
const re = /<script>([\s\S]*?)<\/script>/g; let m;
while ((m = re.exec(html))) scripts.push(m[1]);

// minimal DOM shim
function makeEl() {
  const el = {
    _html: '', textContent: '', value: '', title: '',
    style: {}, dataset: {}, classList: { add(){}, remove(){}, toggle(){}, contains(){return false;} },
    children: [],
    set innerHTML(v){ this._html = String(v); }, get innerHTML(){ return this._html; },
    addEventListener(){}, removeEventListener(){},
    querySelector(){ return makeEl(); },
    querySelectorAll(){ return []; },
    closest(){ return null; },
    getAttribute(){ return null; }, setAttribute(){},
    appendChild(){}, focus(){}, click(){},
  };
  return el;
}
const elements = {};
const document = {
  body: { classList: { add(){}, remove(){}, toggle(){} } },
  getElementById(id){ return elements[id] || (elements[id] = makeEl()); },
  querySelector(){ return makeEl(); },
  querySelectorAll(){ return []; },
  addEventListener(){}, removeEventListener(){},
  createElement(){ return makeEl(); },
  documentElement: { requestFullscreen(){}, webkitRequestFullscreen(){}, mozRequestFullScreen(){} },
  fullscreenElement: null, webkitFullscreenElement: null, mozFullScreenElement: null,
};
const storage = {};
const localStorage = { getItem(k){ return k in storage ? storage[k] : null; }, setItem(k,v){ storage[k]=String(v); }, removeItem(k){ delete storage[k]; } };
const window = {
  parent: { postMessage(){}, },
  addEventListener(){}, removeEventListener(){},
  location: { href: '', search: '?theme=dark' },
  postMessage(){},
};
const sandbox = {
  document, window, localStorage,
  location: { search: '?theme=dark' },
  URLSearchParams: URLSearchParams,
  console, setTimeout, clearTimeout, setInterval, clearInterval,
  JSON, Math, Date, Array, Object, String, Number, RegExp,
};
sandbox.window = window; sandbox.self = window; sandbox.globalThis = sandbox;
vm.createContext(sandbox);

let ok = true;
scripts.forEach((s, i) => {
  try { vm.runInContext(s, sandbox, { filename: 'de-script-' + i + '.js' }); }
  catch (e) { ok = false; console.log('RUNTIME ERROR in script #' + i + ':', e.message); }
});

// exercise language switch + re-render
try {
  if (sandbox.setLang) { sandbox.setLang('zh'); sandbox.setLang('en'); console.log('setLang OK'); }
  else console.log('setLang not found on global (may be inside IIFE — fine)');
} catch (e) { ok = false; console.log('setLang call error:', e.message); }

console.log('DE SMOKE:', ok ? 'PASS' : 'FAIL');
process.exit(ok ? 0 : 1);
