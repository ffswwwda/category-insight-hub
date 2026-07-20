# -*- coding: utf-8 -*-
"""生成美亚倒膜&名器商品评论看板 amz-review-dashboard.html（单文件内联，默认暗色，复用 reddit 看板视觉语言）"""
import openpyxl, json, re, collections

SRC = "/Users/fsw/Documents/美亚倒膜&名器商品评论（202512～20265月卖家精灵覆盖 ASIN）.xlsx"
OUT = "/Users/fsw/WorkBuddy/2026-07-15-08-51-27/amz-review-dashboard.html"

wb = openpyxl.load_workbook(SRC, read_only=True)
ws = wb['合并评论数据']
rows_iter = ws.iter_rows(values_only=True)
header = list(next(rows_iter))
idx = {h: i for i, h in enumerate(header)}

keep = ['ASIN', '标题', '内容', '星级', '赞同数', '图片数量', '是否有视频', 'VP评论', 'Vine Voice评论', '所属国家', '评论时间', '型号']
ki = [idx[k] for k in keep]

COLS = ['asin', 'title', 'content', 'star', 'votes', 'imgs', 'video', 'vp', 'vine', 'country', 'date', 'model']
arr = []
stars = []
for r in rows_iter:
    if r is None:
        continue
    asin = str(r[ki[0]] or '')
    title = str(r[ki[1]] or '')[:50]
    content = str(r[ki[2]] or '')[:120]
    st = r[ki[3]]
    try:
        star = int(float(st)) if st not in (None, '') else None
    except Exception:
        star = None
    votes = int(r[ki[4]]) if str(r[ki[4]]).isdigit() else 0
    imgs = int(r[ki[5]]) if str(r[ki[5]]).isdigit() else 0
    video = 'Y' if str(r[ki[6]]) not in ('None', 'nan', '', 'NoneType') and r[ki[6]] is not None else 'N'
    vp = 'Y' if str(r[ki[7]]) == 'Y' else 'N'
    vine = 'Y' if str(r[ki[8]]) == 'Y' else 'N'
    country = str(r[ki[9]] or 'Unknown')
    date = str(r[ki[10]] or '')[:10]
    model = str(r[ki[11]] or 'None')
    if model in ('None', 'nan', ''):
        model = '(未注明)'
    if star is not None:
        stars.append(star)
    arr.append([asin, title, content, star, votes, imgs, video, vp, vine, country, date, model])

total = len(arr)
asin_set = set(a[0] for a in arr if a[0])
avg_star = round(sum(stars) / len(stars), 2) if stars else 0
country_set = set(a[9] for a in arr)
dates = [a[10] for a in arr if a[10]]
date_min, date_max = (min(dates), max(dates)) if dates else ('', '')

# ---- 聚合 ----
def topn(field_idx, n=15, filt=None):
    c = collections.Counter()
    for a in arr:
        v = a[field_idx]
        if filt and not filt(a):
            continue
        c[v] += 1
    return [{'v': k, 'n': v} for k, v in c.most_common(n)]

star_mod = sorted([{'v': s, 'n': sum(1 for a in arr if a[3] == s)} for s in [5, 4, 3, 2, 1] if any(a[3] == s for a in arr)], key=lambda x: -x['v'])
country_mod = topn(9, 12)
model_mod = [x for x in topn(11, 15) if x['v'] != '(未注明)']
month_mod = sorted([{'v': a[10][:7], 'n': 1} for a in arr if a[10]], key=lambda x: x['v'])
# month count
mc = collections.Counter(a[10][:7] for a in arr if a[10])
month_mod = [{'v': k, 'n': v} for k, v in sorted(mc.items())]
media_mod = [
    {'v': '含图片', 'n': sum(1 for a in arr if a[5] > 0)},
    {'v': '无图片', 'n': sum(1 for a in arr if a[5] == 0)},
    {'v': '含视频', 'n': sum(1 for a in arr if a[6] == 'Y')},
    {'v': '无视频', 'n': sum(1 for a in arr if a[6] != 'Y')},
]
type_mod = [
    {'v': 'VP评论', 'n': sum(1 for a in arr if a[7] == 'Y')},
    {'v': 'Vine Voice', 'n': sum(1 for a in arr if a[8] == 'Y')},
    {'v': '普通评论', 'n': sum(1 for a in arr if a[7] == 'N' and a[8] == 'N')},
]

# ---- 关键词 ----
STOP = set('的 了 是 我 都 也 就 还 你 他 她 它 们 在 有 和 与 及 这 那 个 啊 吧 呢 吗 哦 嗯 把 被 让 给 对 从 到 上 下 里 后 前 中 不 没 很 太 真 好 要 会 能 可以 这个 那个 一个 我们 他们 自己 什么 怎么 这样 一样 已经 因为 所以 但是 如果 现在 the a an and or to of for in on is are was were be with you i it this that my your our their he she they we me him her them not no yes so but if at as by from all can will just like get got one two'.split())
def tokens(text):
    text = str(text).lower()
    out = []
    # 英文词
    for w in re.findall(r'[a-z]{3,}', text):
        if w not in STOP:
            out.append(w)
    # 中文 2-gram
    cjk = re.findall(r'[\u4e00-\u9fff]+', text)
    for seg in cjk:
        if len(seg) >= 2:
            for i in range(len(seg) - 1):
                bg = seg[i:i+2]
                if bg not in STOP:
                    out.append(bg)
    return out
kwc = collections.Counter()
for a in arr:
    for t in tokens(a[1] + ' ' + a[2]):
        kwc[t] += 1
kw_mod = [{'v': k, 'n': v} for k, v in kwc.most_common(40)]

modules = [
    {'key': 'star', 'name': '星级', 'type': 'pill', 'vals': star_mod},
    {'key': 'country', 'name': '所属国家', 'type': 'bar', 'vals': country_mod},
    {'key': 'model', 'name': '型号', 'type': 'bar', 'vals': model_mod},
    {'key': 'media', 'name': '媒体类型', 'type': 'pill', 'vals': media_mod},
    {'key': 'type', 'name': '评论类型', 'type': 'pill', 'vals': type_mod},
    {'key': 'month', 'name': '评论月份', 'type': 'bar', 'vals': month_mod},
    {'key': 'kw', 'name': '关键词', 'type': 'pill', 'vals': kw_mod},
]

# ---- 最新动态 feed（按日期倒序取前 8）----
feed = sorted([a for a in arr if a[10]], key=lambda x: x[10], reverse=True)[:8]

DATA = {
    'cols': COLS,
    'rows': arr,
    'modules': modules,
    'meta': {
        'total': total, 'asinCount': len(asin_set), 'avgStar': avg_star,
        'countryCount': len(country_set), 'dateMin': date_min, 'dateMax': date_max,
        'feed': [{'asin': a[0], 'title': a[1], 'content': a[2], 'star': a[3], 'country': a[9], 'date': a[10]} for a in feed],
    }
}

json_data = json.dumps(DATA, ensure_ascii=False, separators=(',', ':'))
print('rows:', total, '| json MB:', round(len(json_data.encode('utf-8'))/1024/1024, 2))

# ===================== HTML 模板 =====================
TPL = r'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>美亚倒膜&名器 · 商品评论看板</title>
<style>
:root{--bg:#0f1219;--panel:#161c2e;--panel2:#1d2340;--border:#2a3158;--text:#e8ecf8;--muted:#9aa3c4;--grad:linear-gradient(135deg,#00d4ff,#a855f7,#ff6b9d);}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;line-height:1.5;padding:0;min-height:100vh}
body.light{--bg:#f5f7fc;--panel:#ffffff;--panel2:#eef1f8;--border:#e2e6f0;--text:#1a2038;--muted:#6b7393}
a{color:#00d4ff}
.wrap{max-width:1180px;margin:0 auto;padding:22px 20px 60px}
.topbar{display:flex;align-items:center;justify-content:space-between;gap:14px;position:sticky;top:0;z-index:30;background:var(--bg);padding:14px 0 12px;border-bottom:1px solid var(--border);margin-bottom:18px}
.brand{display:flex;align-items:center;gap:11px}
.logo{width:34px;height:34px;border-radius:10px;background:var(--grad);display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;font-size:15px;flex:0 0 auto}
.brand h1{font-size:17px;font-weight:700;letter-spacing:.3px}
.brand p{font-size:12px;color:var(--muted)}
.topr{display:flex;align-items:center;gap:10px}
.btn{cursor:pointer;border:1px solid var(--border);background:var(--panel2);color:var(--text);padding:7px 13px;border-radius:9px;font-size:13px;transition:.18s;white-space:nowrap}
.btn:hover{border-color:#7c8cff}
.btn.pri{background:var(--grad);border:none;color:#fff;font-weight:600}
.kpis{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-bottom:20px}
.kpi{background:var(--panel);border:1px solid var(--border);border-radius:14px;padding:15px 16px}
.kpi .n{font-size:25px;font-weight:800;background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.kpi .l{font-size:12px;color:var(--muted);margin-top:3px}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:14px}
.card{background:var(--panel);border:1px solid var(--border);border-radius:14px;padding:15px 16px}
.card h3{font-size:13px;color:var(--muted);font-weight:600;margin-bottom:11px;display:flex;align-items:center;gap:7px}
.bar{display:flex;align-items:center;gap:9px;margin:6px 0;font-size:13px}
.bar .lab{width:78px;flex:0 0 auto;color:var(--muted);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.bar .track{flex:1;height:14px;background:var(--panel2);border-radius:7px;overflow:hidden}
.bar .fill{height:100%;background:var(--grad);border-radius:7px;transition:width .5s}
.bar .val{width:56px;flex:0 0 auto;text-align:right;color:var(--text);font-variant-numeric:tabular-nums}
.pill-cloud{display:flex;flex-wrap:wrap;gap:8px}
.pill{cursor:pointer;border:1px solid var(--border);background:var(--panel2);color:var(--text);padding:5px 11px;border-radius:20px;font-size:12.5px;transition:.15s}
.pill:hover{border-color:#7c8cff;transform:translateY(-1px)}
.pill.on{background:var(--grad);border:none;color:#fff;font-weight:600}
.pill .c{opacity:.7;margin-left:5px;font-size:11px}
.mini{display:grid;grid-template-columns:repeat(3,1fr);gap:9px;margin-top:11px}
.mini .m{background:var(--panel2);border-radius:10px;padding:9px 10px}
.mini .m .v{font-size:19px;font-weight:800}
.mini .m .t{font-size:11px;color:var(--muted)}
.feed{display:flex;flex-direction:column;gap:9px}
.fitem{border-left:3px solid transparent;background:var(--panel2);border-radius:0 10px 10px 0;padding:9px 12px}
.fitem .fh{display:flex;justify-content:space-between;gap:10px;font-size:12px;color:var(--muted);margin-bottom:3px}
.fitem .ft{font-weight:600;font-size:13.5px;margin-bottom:2px}
.fitem .fc{font-size:12.5px;color:var(--text);opacity:.92}
.star{color:#ffb020;font-weight:700}
.tree{background:var(--panel);border:1px solid var(--border);border-radius:14px;padding:14px 16px;margin-bottom:14px}
.tnode{border-bottom:1px solid var(--border);padding:9px 0}
.tnode:last-child{border-bottom:none}
.thead{display:flex;align-items:center;justify-content:space-between;cursor:pointer;font-size:14px;font-weight:600}
.thead .badge{font-size:11px;color:var(--muted);font-weight:400}
.tchildren{display:none;margin-top:10px}
.tchildren.open{display:block}
.val-list{display:block}
.bar .lab.clickable{cursor:pointer;border-bottom:1px dotted var(--muted)}
.bar .lab.clickable:hover{color:#7c8cff;border-color:#7c8cff}
.bar.on .fill{outline:2px solid #7c8cff;outline-offset:1px}
.section-title{font-size:15px;font-weight:700;margin:6px 0 13px;display:flex;align-items:center;gap:8px}
.empty{color:var(--muted);font-size:13px;padding:20px;text-align:center}
.cartbar{position:fixed;right:18px;bottom:18px;z-index:40}
.cartbtn{background:var(--grad);color:#fff;border:none;border-radius:30px;padding:11px 18px;font-size:14px;font-weight:600;cursor:pointer;box-shadow:0 8px 24px rgba(120,90,255,.4)}
.cart-added{background:#1f8a4c!important}
.hl{outline:2px solid #7c8cff}
.muted{color:var(--muted)}
</style></head>
<body>
<div class="wrap">
  <div class="topbar">
    <div class="brand"><div class="logo">美</div><div><h1>美亚倒膜 & 名器 · 商品评论看板</h1><p id="sub">加载中…</p></div></div>
    <div class="topr">
      <button class="btn" id="backBtn" onclick="goHub()">← 返回主站</button>
      <button class="btn" id="themeBtn" onclick="toggleTheme()">切换主题</button>
    </div>
  </div>
  <div id="app"></div>
</div>
<div class="cartbar"><button class="cartbtn" id="cartBtn" onclick="addCart()">+ 加入购物车</button></div>
<script>
const DATA = /*__DATA__*/null;
const COLS = DATA.cols;
const ROWS = DATA.rows;
const MODS = DATA.modules;
const META = DATA.meta;
const CIH = (function(){try{return JSON.parse(localStorage.getItem('cih_cart_v1')||'[]')}catch(e){return[]}})();
let cartAdded = CIH.some(function(x){return x.id==='amz-review'});
const state = {}; // moduleKey -> Set(values)
MODS.forEach(function(m){state[m.key]=new Set();});
let theme = (new URLSearchParams(location.search).get('theme')||(localStorage.getItem('cih_theme')||'dark'));
function applyTheme(){document.body.classList.toggle('light', theme==='light');localStorage.setItem('cih_theme',theme);try{parent&&parent.postMessage({type:'cih-theme',theme:theme},'*')}catch(e){}}
applyTheme();
function toggleTheme(){theme = theme==='dark'?'light':'dark';applyTheme();}
window.addEventListener('message',function(e){if(e.data&&e.data.type==='cih-theme'){theme=e.data.theme;applyTheme();render();}});
function goHub(){try{parent&&parent.postMessage({type:'cih-open',id:'home'},'*')}catch(e){} location.href='category-insight-hub.html';}

function filtered(){
  const active = MODS.filter(function(m){return state[m.key].size>0;});
  if(!active.length) return ROWS;
  return ROWS.filter(function(r){
    return active.every(function(m){
      const set = state[m.key];
      if(m.key==='star') return set.has(r[3]);
      if(m.key==='country') return set.has(r[9]);
      if(m.key==='model') return set.has(r[11]);
      if(m.key==='month') return set.has(r[10].slice(0,7));
      if(m.key==='kw'){const t=(r[1]+' '+r[2]).toLowerCase();let ok=false;set.forEach(function(v){if(t.indexOf(v.toLowerCase())>=0)ok=true;});return ok;}
      if(m.key==='media'){let ok=false;set.forEach(function(v){if(v==='含图片'&&r[5]>0)ok=true;if(v==='无图片'&&r[5]===0)ok=true;if(v==='含视频'&&r[6]==='Y')ok=true;if(v==='无视频'&&r[6]!=='Y')ok=true;});return ok;}
      if(m.key==='type'){let ok=false;set.forEach(function(v){if(v==='VP评论'&&r[7]==='Y')ok=true;if(v==='Vine Voice'&&r[8]==='Y')ok=true;if(v==='普通评论'&&r[7]==='N'&&r[8]==='N')ok=true;});return ok;}
      return true;
    });
  });
}
function maxN(vals){return Math.max(1,Math.max.apply(null,vals.map(function(v){return v.n;})));}
function distBar(vals,maxv,fmt,modKey){
  return '<div>'+vals.map(function(v){
    const pct=(v.n/maxv*100).toFixed(1);
    const lab = modKey ? '<span class="lab clickable" data-mod="'+modKey+'" data-v="'+esc(v.v)+'" title="'+esc(v.v)+'">'+esc(fmt?fmt(v.v):v.v)+'</span>' : '<span class="lab" title="'+esc(v.v)+'">'+esc(fmt?fmt(v.v):v.v)+'</span>';
    return '<div class="bar'+(modKey&&state[modKey].has(v.v)?' on':'')+'">'+lab+'<span class="track"><span class="fill" style="width:'+pct+'%"></span></span><span class="val">'+v.n.toLocaleString()+'</span></div>';
  }).join('')+'</div>';
}
function pillCloud(vals){
  return '<div class="pill-cloud">'+vals.map(function(v){
    return '<span class="pill '+(state[curMod]==null?'':(state[curMod].has(v.v)?'on':''))+'" data-mod="'+curMod+'" data-v="'+esc(v.v)+'">'+esc(v.v)+'<span class="c">'+v.n.toLocaleString()+'</span></span>';
  }).join('')+'</div>';
}
let curMod=null;
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}

function render(){
  const active = MODS.filter(function(m){return state[m.key].size>0;});
  const flt = filtered();
  const html = [];
  html.push('<p class="muted" style="margin-bottom:14px;font-size:13px">数据源：美亚（Amazon US）倒膜 & 名器类目商品评论 · 覆盖 ASIN '+META.asinCount.toLocaleString()+' 个 · 评论区间 '+META.dateMin+' ~ '+META.dateMax+(active.length?' · 当前筛选命中 <b style="color:var(--text)">'+flt.length.toLocaleString()+'</b> 条':' · 共 <b style="color:var(--text)">'+META.total.toLocaleString()+'</b> 条')+'</p>');
  if(!active.length){
    html.push(renderOverview());
  }
  html.push('<div class="section-title">🗂 维度筛选（点击展开 · 跨维度 AND 筛选）</div>');
  html.push(renderTree());
  if(active.length){
    html.push('<div class="section-title">🔍 筛选结果分布（'+flt.length.toLocaleString()+' 条）</div>');
    html.push(renderResult(flt));
  }
  document.getElementById('app').innerHTML = html.join('');
  document.getElementById('sub').textContent = '共 '+META.total.toLocaleString()+' 条评论 · '+META.asinCount.toLocaleString()+' 个 ASIN · 平均 '+META.avgStar+'★';
  bind();
  updateCartBtn();
}
function renderOverview(){
  const h=[];
  h.push('<div class="kpis">'
    +kpi(META.total.toLocaleString(),'总评论数')
    +kpi(META.asinCount.toLocaleString(),'覆盖 ASIN')
    +kpi(META.avgStar+'★','平均星级')
    +kpi(META.countryCount,'国家/地区')
    +kpi(MODS.reduce(function(s,m){return s+m.vals.length;},0),'可筛选维度值')
    +'</div>');
  // 星级分布
  const starMod = MODS.find(function(m){return m.key==='star';});
  const countryMod = MODS.find(function(m){return m.key==='country';});
  const modelMod = MODS.find(function(m){return m.key==='model';});
  const monthMod = MODS.find(function(m){return m.key==='month';});
  h.push('<div class="grid2">');
  h.push(card('⭐ 星级分布', distBar(starMod.vals, maxN(starMod.vals), function(v){return v+'★';})));
  h.push(card('🌍 所属国家 Top', distBar(countryMod.vals.slice(0,8), maxN(countryMod.vals), function(v){return v;})));
  h.push(card('📦 评论最多 ASIN Top10', distBar(modelMod.vals.slice(0,10), maxN(modelMod.vals))));
  h.push(card('⏱ 月度评论趋势', distBar(monthMod.vals, maxN(monthMod.vals))));
  h.push('</div>');
  // 关键词 + feed
  const kwMod = MODS.find(function(m){return m.key==='kw';});
  const mediaMod = MODS.find(function(m){return m.key==='media';});
  const typeMod = MODS.find(function(m){return m.key==='type';});
  h.push('<div class="grid2">');
  h.push(card('🔤 高频关键词 Top40', '<div class="pill-cloud">'+kwMod.vals.map(function(v){return '<span class="pill">'+esc(v.v)+'<span class="c">'+v.n.toLocaleString()+'</span></span>';}).join('')+'</div>'
    + '<div class="mini">'+mediaMod.vals.map(function(v){return '<div class="m"><div class="v">'+v.n.toLocaleString()+'</div><div class="t">'+esc(v.v)+'</div></div>';}).join('')+'</div>'
    + '<div class="mini">'+typeMod.vals.map(function(v){return '<div class="m"><div class="v">'+v.n.toLocaleString()+'</div><div class="t">'+esc(v.v)+'</div></div>';}).join('')+'</div>'));
  // feed
  const feed = META.feed.map(function(f){
    return '<div class="fitem"><div class="fh"><span>'+esc(f.asin)+' · '+(f.star?('<span class="star">'+f.star+'★</span>'):'—')+'</span><span>'+esc(f.country)+' · '+esc(f.date)+'</span></div>'
      + (f.title?'<div class="ft">'+esc(f.title)+'</div>':'')+'<div class="fc">'+esc(f.content)+'</div></div>';
  }).join('');
  h.push(card('📋 最新评论动态', '<div class="feed">'+feed+'</div>'));
  h.push('</div>');
  return h.join('');
}
function kpi(n,l){return '<div class="kpi"><div class="n">'+n+'</div><div class="l">'+l+'</div></div>';}
function card(t,body){return '<div class="card"><h3>'+t+'</h3>'+body+'</div>';}
function renderTree(){
  return '<div class="tree">'+MODS.map(function(m){
    return '<div class="tnode"><div class="thead" onclick="toggleNode(this)"><span>'+esc(m.name)+' <span class="badge">'+m.vals.length+' 个值</span></span><span class="badge">'+m.type+' ▾</span></div>'
      +'<div class="tchildren"><div class="val-list" data-mod="'+m.key+'">'+ (m.type==='bar'
        ? distBar(m.vals, maxN(m.vals), m.key==='star'?function(v){return v+'★';}:null, m.key)
        : '<div class="pill-cloud">'+m.vals.map(function(v){return '<span class="pill '+(state[m.key].has(v.v)?'on':'')+'" data-mod="'+m.key+'" data-v="'+esc(v.v)+'">'+esc(v.v)+'<span class="c">'+v.n.toLocaleString()+'</span></span>';}).join('')+'</div>')
      +'</div></div></div>';
  }).join('')+'</div>';
}
function renderResult(flt){
  const h=[];
  h.push('<div class="tree">'+MODS.map(function(m){
    const cnt = {};
    flt.forEach(function(r){
      let key=null;
      if(m.key==='star') key=r[3];
      else if(m.key==='country') key=r[9];
      else if(m.key==='model') key=r[11];
      else if(m.key==='month') key=r[10].slice(0,7);
      else if(m.key==='media'){if(r[5]>0)cnt['含图片']=(cnt['含图片']||0)+1;else cnt['无图片']=(cnt['无图片']||0)+1;if(r[6]==='Y')cnt['含视频']=(cnt['含视频']||0)+1;else cnt['无视频']=(cnt['无视频']||0)+1;}
      else if(m.key==='type'){if(r[7]==='Y')cnt['VP评论']=(cnt['VP评论']||0)+1;if(r[8]==='Y')cnt['Vine Voice']=(cnt['Vine Voice']||0)+1;if(r[7]==='N'&&r[8]==='N')cnt['普通评论']=(cnt['普通评论']||0)+1;}
      else if(m.key==='kw'){const t=(r[1]+' '+r[2]).toLowerCase();m.vals.forEach(function(v){if(t.indexOf(v.v.toLowerCase())>=0)cnt[v.v]=(cnt[v.v]||0)+1;});}
      if(key!=null) cnt[key]=(cnt[key]||0)+1;
    });
    const vals=Object.keys(cnt).map(function(k){return {v:k,n:cnt[k]};});
    const maxv=Math.max(1,Math.max.apply(null,vals.map(function(v){return v.n;})));
    return '<div class="tnode"><div class="thead"><span>'+esc(m.name)+' <span class="badge">筛选后命中分布</span></span><span class="badge">'+vals.length+' 值</span></div>'
      +'<div style="margin-top:9px">'+(m.type==='bar'?distBar(vals,maxv):'<div class="pill-cloud">'+vals.map(function(v){return '<span class="pill">'+esc(v.v)+'<span class="c">'+v.n.toLocaleString()+'</span></span>';}).join('')+'</div>')+'</div></div>';
  }).join('')+'</div>');
  // 抽样最新 6 条
  const sample = flt.filter(function(r){return r[10];}).sort(function(a,b){return a[10]<b[10]?1:-1;}).slice(0,6);
  h.push(card('📋 命中评论抽样（最新 6 条）', '<div class="feed">'+sample.map(function(r){
    return '<div class="fitem"><div class="fh"><span>'+esc(r[0])+' · '+(r[3]?('<span class="star">'+r[3]+'★</span>'):'—')+'</span><span>'+esc(r[9])+' · '+esc(r[10])+'</span></div>'
      +(r[1]?'<div class="ft">'+esc(r[1])+'</div>':'')+'<div class="fc">'+esc(r[2])+'</div></div>';
  }).join('')+'</div>'));
  return h.join('');
}
function toggleNode(el){const c=el.nextElementSibling.querySelector('.tchildren,.val-list');if(c) c.classList.toggle('open');}
function bind(){
  document.querySelectorAll('.pill[data-mod],.bar .lab.clickable').forEach(function(p){
    p.addEventListener('click',function(){
      const k=p.getAttribute('data-mod'), v=p.getAttribute('data-v');
      if(state[k].has(v)) state[k].delete(v); else state[k].add(v);
      render();
    });
  });
}
function addCart(){
  const item={id:'amz-review',name:'美亚倒膜&名器 · 商品评论看板',type:'amz',ts:Date.now()};
  let arr=[];try{arr=JSON.parse(localStorage.getItem('cih_cart_v1')||'[]')}catch(e){}
  if(!arr.some(function(x){return x.id==='amz-review'})){arr.push(item);localStorage.setItem('cih_cart_v1',JSON.stringify(arr));}
  try{parent&&parent.postMessage({type:'cih-cart-add',item:item},'*')}catch(e){}
  cartAdded=true;updateCartBtn();
}
function updateCartBtn(){const b=document.getElementById('cartBtn');if(cartAdded){b.textContent='✓ 已加入购物车';b.classList.add('cart-added');}else{b.textContent='+ 加入购物车';b.classList.remove('cart-added');}}
render();
</script>
</body></html>'''

html = TPL.replace('/*__DATA__*/null', json_data)
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(html)
import os
print('OUT:', OUT, '| size MB:', round(os.path.getsize(OUT)/1024/1024, 2))
