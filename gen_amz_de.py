# -*- coding: utf-8 -*-
"""生成美亚倒膜&名器 商品评论看板 —— 德国商品库(de-dashboard)同款结构。
数据：28727 条评论，按 ASIN 聚合为 386 款商品。
输出：amz-review-dashboard.html（数据内联，单文件，GitHub Pages 友好）。
"""
import openpyxl, json, sys

SRC = "/Users/fsw/Documents/美亚倒膜&名器商品评论（202512～20265月卖家精灵覆盖 ASIN）.xlsx"
OUT = "/Users/fsw/WorkBuddy/2026-07-15-08-51-27/vendor/amz-review-dashboard.html"

wb = openpyxl.load_workbook(SRC, read_only=True)
ws = wb['合并评论数据']
rows = ws.iter_rows(values_only=True)
header = list(next(rows))
idx = {h: i for i, h in enumerate(header)}

cols = ["asin", "title", "content", "star", "votes", "video", "image", "country", "model", "date"]
HEADER_MAP = {
    'asin': 'ASIN', 'title': '标题', 'content': '内容', 'star': '星级',
    'votes': '赞同数', 'video': '是否有视频', 'image': '图片数量',
    'country': '所属国家', 'model': '型号', 'date': '评论时间'
}
ci = {c: idx[HEADER_MAP[c]] for c in cols}

def clean(s, n):
    s = str(s or '').strip()
    return s[:n]

out_rows = []
for r in rows:
    if r is None:
        continue
    try:
        sv = int(float(r[ci['star']])) if r[ci['star']] not in (None, '') else None
    except Exception:
        sv = None
    try:
        vt = int(float(r[ci['votes']])) if str(r[ci['votes']]).isdigit() else 0
    except Exception:
        vt = 0
    vid = str(r[ci['video']]).strip() not in ('None', '', '无', '否')
    pic = False
    try:
        pic = int(float(r[ci['image']])) > 0
    except Exception:
        pic = False
    country = clean(r[ci['country']], 12) or '未知'
    model = clean(r[ci['model']], 40) or '未知'
    date = str(r[ci['date']] or '')[:10]
    asin = clean(r[ci['asin']], 20)
    if not asin:
        continue
    out_rows.append([
        asin,
        clean(r[ci['title']], 70),
        clean(r[ci['content']], 160),
        sv,
        vt,
        vid,
        pic,
        country,
        model,
        date,
    ])

TOTAL = len(out_rows)
print("评论条数:", TOTAL)

# ---- HTML 外壳（克隆 de-dashboard 的 CSS + 结构，改为评论数据逻辑）----
CSS = r'''  :root{
    --bg:#f6f7f9; --panel:rgba(255,255,255,.72); --panel-2:rgba(255,255,255,.5); --border:rgba(0,0,0,.08);
    --ink:#2b2f33; --ink-2:#5b6470; --muted:#8b94a3; --line:rgba(0,0,0,.05);
    --accent:#00C3F3; --accent-weak:#E6F7FC; --accent-2:#a855f7;
    --rad-grad:linear-gradient(135deg,#00d4ff 0%,#a855f7 50%,#ff6b9d 100%);
    --warn:#e8833a; --ok:#1f9d6b; --danger:#e05656; --star:#f5a623;
    --shadow:0 1px 3px rgba(0,0,0,.04),0 6px 20px rgba(0,0,0,.05);
    --glass-blur:blur(14px);
    --radius:14px; --radius-sm:10px;
    --font:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
    --mono:"SF Mono",ui-monospace,"JetBrains Mono",Menlo,Consolas,monospace;
  }
  body.dark{
    --bg:#0a0e1a; --panel:rgba(20,28,48,.6); --panel-2:rgba(30,40,66,.45); --border:rgba(255,255,255,.1);
    --ink:#e6ebf5; --ink-2:#aab4c8; --muted:#8893a8; --line:rgba(255,255,255,.08);
    --accent-weak:rgba(0,195,243,.14);
    --shadow:0 1px 3px rgba(0,0,0,.3),0 8px 28px rgba(0,0,0,.4);
    background-image:
      radial-gradient(circle at 18% 82%, rgba(0,195,243,.14) 0%, transparent 45%),
      radial-gradient(circle at 82% 18%, rgba(168,85,247,.12) 0%, transparent 45%),
      radial-gradient(circle at 55% 55%, rgba(219,179,96,.06) 0%, transparent 60%),
      linear-gradient(rgba(0,195,243,.06) 1px,transparent 1px),
      linear-gradient(90deg,rgba(0,195,243,.06) 1px,transparent 1px);
  }
  body.dark .src-card .tag{background:rgba(219,179,96,.18);}
  body.dark .chip:hover{border-color:rgba(255,255,255,.22);}
  body.dark .ls-item:hover{border-color:rgba(255,255,255,.22);}
  body.dark .pill.ok{background:rgba(31,157,107,.18);color:#5fd6a8;}
  body.dark .pill.no{background:rgba(224,86,86,.18);color:#ff8e8e;}
  body.dark .pill.cn{background:rgba(219,179,96,.18);color:#e6b563;}
  body.dark ::-webkit-scrollbar-thumb{background:#2a3550;}
  body.dark ::-webkit-scrollbar-thumb:hover{background:#3a4768;}
  body.dark .sidebar{background:rgba(20,28,48,.6);}
  body.dark .topbar{background:rgba(20,28,48,.6);}
  body.dark .filterbar{background:rgba(20,28,48,.7);}
  *{box-sizing:border-box}
  html{scroll-behavior:smooth}
  body{margin:0;background-color:var(--bg);color:var(--ink);font-family:var(--font);font-size:14px;line-height:1.55;-webkit-font-smoothing:antialiased;
    background-image:
      radial-gradient(circle at 18% 82%, rgba(0,195,243,.08) 0%, transparent 45%),
      radial-gradient(circle at 82% 18%, rgba(168,85,247,.07) 0%, transparent 45%),
      radial-gradient(circle at 55% 55%, rgba(219,179,96,.04) 0%, transparent 60%),
      linear-gradient(rgba(0,195,243,.04) 1px,transparent 1px),
      linear-gradient(90deg,rgba(0,195,243,.04) 1px,transparent 1px);
    background-size:auto,auto,auto,60px 60px,60px 60px;
    background-attachment:fixed}
  ::-webkit-scrollbar{width:10px;height:10px}
  ::-webkit-scrollbar-thumb{background:#d3d8e0;border-radius:8px;border:3px solid var(--bg)}
  ::-webkit-scrollbar-thumb:hover{background:#bcc3cf}
  .app{display:flex;min-height:100vh}
  .sidebar{width:264px;flex:0 0 264px;background:rgba(255,255,255,.74);backdrop-filter:var(--glass-blur);-webkit-backdrop-filter:var(--glass-blur);border-right:1px solid var(--border);
    display:flex;flex-direction:column;position:sticky;top:0;height:100vh}
  .brand{display:flex;gap:11px;align-items:center;padding:18px 18px 14px}
  .brand-mark{width:36px;height:36px;border-radius:10px;background:var(--rad-grad);
    color:#fff;display:grid;place-items:center;font-size:15px;font-weight:800;box-shadow:0 6px 18px rgba(0,195,243,.32)}
  .brand-name{font-weight:700;font-size:15px;letter-spacing:.2px}
  .brand-sub{font-size:11px;color:var(--muted);letter-spacing:.6px;margin-top:1px}
  .src-card{margin:10px 14px;background:var(--panel-2);backdrop-filter:var(--glass-blur);-webkit-backdrop-filter:var(--glass-blur);border:1px solid var(--border);border-radius:12px;padding:13px 14px;cursor:pointer;transition:border-color .15s,box-shadow .15s,background .15s}
  .src-card:hover{border-color:rgba(0,195,243,.35)}
  .src-card.active{border-color:var(--accent);background:var(--accent-weak);box-shadow:0 0 0 1px rgba(0,195,243,.15)}
  .src-card .tag{display:inline-block;background:#fff4e0;color:var(--warn);font-weight:600;border-radius:20px;padding:2px 9px;font-size:10.5px;margin-bottom:8px}
  .src-card h4{margin:0 0 4px;font-size:13.5px;font-weight:700;line-height:1.4}
  .src-card .meta{font-size:11.5px;color:var(--muted);line-height:1.6}
  .src-card .meta b{color:var(--ink-2);font-weight:600}
  .sidebar-foot{margin-top:auto;padding:13px 16px 16px;border-top:1px solid var(--border);font-size:11.5px;color:var(--muted);line-height:1.5}
  .main{flex:1;min-width:0;display:flex;flex-direction:column}
  .topbar{position:sticky;top:0;z-index:20;background:rgba(255,255,255,.72);backdrop-filter:var(--glass-blur);-webkit-backdrop-filter:var(--glass-blur);
    border-bottom:1px solid var(--border);padding:16px 26px;display:flex;align-items:center;gap:18px}
  .topbar-left{display:flex;flex-direction:column;min-width:0}
  .topbar-titlerow{display:flex;align-items:center;gap:13px}
  .back-btn{appearance:none;border:1px solid var(--border);background:var(--panel);color:var(--ink-2);
    font-family:var(--font);font-size:12.5px;font-weight:600;padding:7px 12px;border-radius:9px;cursor:pointer;
    transition:background .15s,border-color .15s,color .15s;white-space:nowrap}
  .back-btn:hover{background:var(--accent-weak);border-color:var(--accent);color:var(--accent)}
  .board-title{margin:0;font-size:18px;font-weight:700;letter-spacing:.2px}
  .board-sub{font-size:12px;color:var(--muted);margin-top:2px}
  .topbar-right{margin-left:auto;display:flex;align-items:center;gap:10px}
  .search-box{display:flex;align-items:center;gap:7px;background:var(--panel);border:1px solid var(--border);
    border-radius:10px;padding:8px 12px;width:340px}
  .search-box input{border:0;outline:0;background:transparent;font-size:13px;width:100%;color:var(--ink);font-family:var(--font)}
  .search-box .ico{color:var(--accent)}
  .fs-btn{appearance:none;display:inline-flex;align-items:center;gap:5px;border:1px solid var(--border);background:var(--panel);color:var(--ink-2);
    font-family:var(--font);font-size:12px;font-weight:600;padding:7px 11px;border-radius:9px;cursor:pointer;
    transition:background .15s,border-color .15s,color .15s;white-space:nowrap;flex-shrink:0}
  .fs-btn:hover{background:var(--accent-weak);border-color:var(--accent);color:var(--accent)}
  .fs-btn svg{width:14px;height:14px;flex-shrink:0}
  .board{flex:1;padding:22px 26px 60px;overflow:auto}
  .filterbar{background:var(--panel);backdrop-filter:var(--glass-blur);-webkit-backdrop-filter:var(--glass-blur);border:1px solid var(--border);border-radius:var(--radius);padding:14px 16px;margin-bottom:18px;box-shadow:var(--shadow);position:sticky;top:60px;z-index:19}
  .fb-hint{font-size:12px;color:var(--muted);margin-bottom:10px}
  .fb-hint code{background:var(--line);padding:1px 6px;border-radius:5px;font-family:var(--mono);font-size:11.5px}
  .chips{display:flex;flex-wrap:wrap;gap:7px}
  .chip{display:inline-flex;align-items:center;gap:5px;border:1px solid var(--border);background:var(--panel-2);
    border-radius:20px;padding:5px 12px;font-size:12.5px;cursor:pointer;color:var(--ink-2);transition:.15s;user-select:none}
  .chip:hover{border-color:#c4cad3}
  .chip.on{background:var(--rad-grad);border-color:transparent;color:#fff;box-shadow:0 4px 14px rgba(0,195,243,.3)}
  .fb-foot{display:flex;align-items:center;gap:12px;margin-top:12px;flex-wrap:wrap}
  .sortsel{display:flex;align-items:center;gap:7px;font-size:12.5px;color:var(--ink-2)}
  .sortsel select{border:1px solid var(--border);border-radius:8px;padding:5px 8px;font-size:12.5px;font-family:var(--font);background:var(--panel);color:var(--ink);outline:0}
  .clearbtn{margin-left:auto;font-size:12.5px;color:var(--muted);cursor:pointer;text-decoration:underline}
  .understood{font-size:12px;color:var(--accent);font-weight:600;margin-top:8px;min-height:16px}
  .view-layers{margin:10px 14px;border:1px solid var(--border);border-radius:12px;background:var(--panel-2);backdrop-filter:var(--glass-blur);-webkit-backdrop-filter:var(--glass-blur);overflow:hidden}
  .vl-head{display:flex;align-items:center;gap:7px;padding:10px 13px;font-size:11px;font-weight:800;color:var(--muted);letter-spacing:.4px;text-transform:uppercase;border-bottom:1px solid var(--line);user-select:none}
  .vl-head .vl-count{margin-left:auto;background:var(--rad-grad);color:#fff;font-size:9.5px;padding:1px 7px;border-radius:8px;font-weight:700}
  .vl-list{padding:6px;max-height:280px;overflow-y:auto;display:flex;flex-direction:column;gap:4px;pointer-events:auto}
  .vl-item{display:flex;align-items:center;gap:8px;padding:8px 10px;border-radius:9px;border:1px solid transparent;cursor:pointer;transition:all .15s;background:var(--panel);user-select:none;pointer-events:auto}
  .vl-item:hover{border-color:rgba(0,195,243,.3);background:rgba(0,195,243,.05)}
  .vl-item.active{border-color:var(--accent);background:var(--accent-weak);box-shadow:0 0 0 1px rgba(0,195,243,.15)}
  .vl-item .vl-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0;background:var(--rad-grad)}
  .vl-item .vl-name{flex:1;font-size:11.5px;font-weight:600;color:var(--ink);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .vl-item .vl-meta{font-size:9.5px;color:var(--muted);flex-shrink:0}
  .vl-item .vl-del{opacity:0;font-size:13px;color:var(--muted);cursor:pointer;flex-shrink:0;padding:2px 4px;border-radius:4px;transition:all .12s;pointer-events:auto}
  .vl-item:hover .vl-del{opacity:.6}
  .vl-item .vl-del:hover{opacity:1;color:var(--danger)}
  .vl-empty{color:var(--muted);font-size:11.5px;text-align:center;padding:18px 8px;line-height:1.6}
  .save-view-btn{display:inline-flex;align-items:center;gap:5px;font-size:11.5px;font-weight:700;padding:5px 13px;border:1px solid var(--accent);border-radius:9px;background:var(--accent-weak);color:var(--accent);cursor:pointer;transition:all .15s;user-select:none;white-space:nowrap}
  .save-view-btn:hover{background:var(--accent);color:#fff}
  #cartBtn.cart-added{border-color:#10b981;background:#ecfdf5;color:#059669;cursor:default;pointer-events:none;opacity:.8}
  .countline{font-size:13px;color:var(--ink-2);margin:0 2px 14px}
  .countline b{color:var(--accent);font-size:15px;font-weight:700}
  .grid{display:grid;gap:16px}
  .g-3{grid-template-columns:repeat(3,1fr)}
  .g-4{grid-template-columns:repeat(4,1fr)}
  .g-6{grid-template-columns:repeat(6,1fr)}
  @media(max-width:1280px){.g-6{grid-template-columns:repeat(3,1fr)}.g-4{grid-template-columns:repeat(2,1fr)}}
  @media(max-width:760px){.g-3,.g-4,.g-6{grid-template-columns:repeat(2,1fr)}.search-box{width:200px}}
  .stat{background:var(--panel);backdrop-filter:var(--glass-blur);-webkit-backdrop-filter:var(--glass-blur);border:1px solid var(--border);border-radius:var(--radius);padding:15px 17px;box-shadow:var(--shadow);transition:.18s;position:relative;overflow:hidden}
  .stat::before{content:'';position:absolute;left:0;top:14px;bottom:14px;width:3px;border-radius:3px;background:var(--rad-grad)}
  .stat:hover{border-color:rgba(0,195,243,.4);box-shadow:0 4px 10px rgba(20,30,50,.05),0 14px 34px rgba(0,195,243,.14)}
  .stat .n{font-size:25px;font-weight:700;letter-spacing:.3px;font-variant-numeric:tabular-nums}
  .stat .l{font-size:12px;color:var(--muted);margin-top:3px}
  .stat .s{font-size:11px;color:var(--accent);margin-top:6px;font-weight:600}
  .panel{background:var(--panel);backdrop-filter:var(--glass-blur);-webkit-backdrop-filter:var(--glass-blur);border:1px solid var(--border);border-radius:var(--radius);padding:18px 20px;box-shadow:var(--shadow);margin-bottom:16px;position:relative;overflow:hidden}
  .panel::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:var(--rad-grad);opacity:.85}
  .panel h3{margin:0 0 14px;font-size:15px;font-weight:700;display:flex;align-items:center;gap:8px}
  .panel h3 .sub{font-size:11.5px;color:var(--muted);font-weight:500;margin-left:auto}
  .dist-row{display:flex;align-items:center;gap:12px;padding:6px 0;font-size:13px}
  .dist-row .lab{width:170px;flex:0 0 170px;color:var(--ink-2);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .dist-row .track{flex:1;height:9px;background:var(--line);border-radius:6px;overflow:hidden}
  .dist-row .track .fill{display:block;height:100%;background:var(--rad-grad);border-radius:6px;transition:width .3s}
  .dist-row .num{width:64px;text-align:right;color:var(--muted);font-variant-numeric:tabular-nums}
  .dist-cols{display:grid;grid-template-columns:1fr 1fr;gap:24px}
  @media(max-width:900px){.dist-cols{grid-template-columns:1fr}}
  .ls-item{display:flex;gap:12px;padding:11px 12px;border:1px solid var(--border);border-radius:10px;margin-bottom:8px;background:var(--panel-2);transition:.15s}
  .ls-item:hover{border-color:#d4dae3}
  .ls-rank{width:24px;height:24px;flex:0 0 24px;border-radius:7px;background:var(--danger);color:#fff;display:grid;place-items:center;font-size:12px;font-weight:700;margin-top:1px}
  .ls-body{flex:1;min-width:0}
  .ls-title{font-size:13px;font-weight:600;color:var(--ink);line-height:1.45}
  .ls-meta{font-size:11.5px;color:var(--muted);margin-top:3px;display:flex;gap:12px;flex-wrap:wrap}
  .ls-meta b{color:var(--ink-2)}
  .ls-snip{font-size:12px;color:var(--ink-2);margin-top:5px;line-height:1.5;background:var(--panel);border-radius:8px;padding:6px 10px;border-left:2px solid var(--danger)}
  .pill{font-size:10.5px;border-radius:20px;padding:1px 8px;font-weight:600;display:inline-flex;align-items:center}
  .pill.ok{background:#eafaf3;color:var(--ok)}
  .pill.no{background:#fdeaea;color:var(--danger)}
  .pill.cn{background:#fff4e0;color:#c97a16}
  .table-wrap{border:1px solid var(--border);border-radius:12px;overflow:hidden}
  table{width:100%;border-collapse:collapse;font-size:12.5px}
  thead th{background:var(--panel-2);text-align:left;padding:10px 12px;font-weight:600;color:var(--ink-2);border-bottom:1px solid var(--border);position:sticky;top:0;white-space:nowrap}
  tbody td{padding:9px 12px;border-bottom:1px solid var(--line);color:var(--ink-2);vertical-align:top}
  tbody tr{cursor:pointer;transition:background .12s}
  tbody tr:hover{background:var(--panel-2)}
  tbody tr.open{background:var(--accent-weak)}
  .ttitle{color:var(--ink);font-weight:500;line-height:1.4;max-width:340px}
  .star{font-variant-numeric:tabular-nums;color:var(--star);font-weight:600}
  .detail-row td{background:var(--panel-2);padding:0}
  .detail-inner{padding:14px 18px;line-height:1.7;font-size:12.5px;color:var(--ink-2);white-space:pre-wrap}
  .kv{display:flex;gap:8px;font-size:12px}
  .kv .k{color:var(--muted);min-width:84px;flex:0 0 auto}
  .kv .v{color:var(--ink)}
  .empty{padding:50px 20px;text-align:center;color:var(--muted)}
  .section-gap{margin-bottom:16px}
'''

HTML_BODY = r'''<body>
<script>
/* 主题跟随主站：URL参数 > localStorage > 亮色；并监听主站 postMessage 实时切换 */
(function(){
  function applyTheme(t){
    t = (t==='dark') ? 'dark' : 'light';
    document.body.classList.toggle('dark', t==='dark');
    document.body.classList.toggle('light', t!=='dark');
    try{ localStorage.setItem('cih-theme', t); }catch(e){}
  }
  var q=new URLSearchParams(location.search).get('theme');
  var s=null; try{ s=localStorage.getItem('cih-theme'); }catch(e){}
  applyTheme(q||s||'light');
  window.addEventListener('message', function(e){ if(e.data&&e.data.type==='cih-theme') applyTheme(e.data.value); });
})();
</script>
<div class="app">
  <aside class="sidebar">
    <div class="brand">
      <div class="brand-mark">AMZ</div>
      <div>
        <div class="brand-name">美亚评论看板</div>
        <div class="brand-sub">REVIEW INSIGHT</div>
      </div>
    </div>
    <div class="src-card">
      <span class="tag">真实数据</span>
      <h4>美亚倒膜 &amp; 名器 · 商品评论</h4>
      <div class="meta">
        数据区间：<b>2025.12–2026.05</b><br>
        评论总数：<b>__TOTAL__ 条</b><br>
        覆盖商品：<b>386 款 ASIN</b><br>
        来源：<b>卖家精灵</b>
      </div>
    </div>
    <div class="view-layers" id="viewLayers">
      <div class="vl-head"><span>📑 视图图层</span><span class="vl-count" id="vlCount">0</span></div>
      <div class="vl-list" id="vlList"><div class="vl-empty">筛选后点「保存为新视图」<br>即可在此保存多组筛选条件</div></div>
    </div>
    <div class="sidebar-foot">
      点击视图卡片可切换筛选<br>对比不同条件下的评论分布
    </div>
  </aside>

  <main class="main">
    <header class="topbar">
      <div class="topbar-left">
        <div class="topbar-titlerow">
          <button class="back-btn" onclick="goBack()" title="返回类目洞察中枢">← 返回</button>
          <div>
            <h1 class="board-title">美亚倒膜 &amp; 名器 · 商品评论看板</h1>
            <div class="board-sub">__TOTAL__ 条真实评论 · 386 款商品 · 多维筛选 + 差评商品榜</div>
          </div>
        </div>
      </div>
      <div class="topbar-right">
        <button class="fs-btn" id="fsBtn" title="全屏查看看板（按 ESC 退出）"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3H5a2 2 0 0 0-2 2v3"/><path d="M21 8V5a2 2 0 0 0-2-2h-3"/><path d="M3 16v3a2 2 0 0 0 2 2h3"/><path d="M16 21h3a2 2 0 0 0 2-2v-3"/></svg>全屏</button>
        <div class="search-box">
          <span class="ico">⌕</span>
          <input id="nl-input" type="text" placeholder="自然语言筛选，如：1-3星差评 美国 有视频" autocomplete="off">
        </div>
      </div>
    </header>

    <div class="board">
      <div class="filterbar">
        <div class="fb-hint">快捷筛选（可叠加）：试试组合 <code>1-3星差评</code> · <code>4-5星好评</code> · <code>美国</code> · <code>加拿大</code> · <code>有视频</code> · <code>有图</code> · <code>近3月</code></div>
        <div class="chips" id="chips"></div>
        <div class="fb-foot">
          <div class="sortsel">
            <span>排序：</span>
            <select id="sort-sel">
              <option value="cnt_desc">评论数优先</option>
              <option value="star_desc">评分优先</option>
              <option value="star_asc">评分升序（差评优先）</option>
              <option value="bad_desc">差评数优先</option>
              <option value="date_desc">最新评论优先</option>
            </select>
          </div>
          <span class="clearbtn" id="clear-btn">清除全部筛选</span>
          <button class="save-view-btn" id="saveViewBtn" title="将当前筛选条件保存为一个新视图"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:15px;height:15px;vertical-align:-2px;margin-right:4px"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><path d="M17 21v-8H7v8M7 3v5h8"/></svg>保存为新视图</button>
          <button class="save-view-btn" id="cartBtn" title="把当前筛选结果加入购物车，跨数据源汇总后可统一下载"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:15px;height:15px;vertical-align:-2px;margin-right:4px"><circle cx="9" cy="20" r="1.3"/><circle cx="17" cy="20" r="1.3"/><path d="M2 3h2.4l2.1 12.3a1.6 1.6 0 0 0 1.6 1.3h9.1a1.6 1.6 0 0 0 1.6-1.3L21.5 7H5.4"/></svg>加入购物车</button>
        </div>
        <div class="understood" id="understood"></div>
      </div>

      <div class="countline">当前命中 <b id="hit-count">0</b> 条评论（共 __TOTAL__ 条，覆盖 <span id="asin-count">0</span> 款商品）</div>

      <div class="grid g-6 section-gap" id="kpis"></div>

      <div class="panel">
        <h3>评论结构分析 <span class="sub">按星级 / 国家 / 月份 / 型号</span></h3>
        <div class="dist-cols">
          <div>
            <div class="dist-row" style="color:var(--muted);font-size:12px;font-weight:600"><span class="lab">星级分布</span><span class="track"></span><span class="num">条数</span></div>
            <div id="dist-star"></div>
          </div>
          <div>
            <div class="dist-row" style="color:var(--muted);font-size:12px;font-weight:600"><span class="lab">国家分布</span><span class="track"></span><span class="num">条数</span></div>
            <div id="dist-country"></div>
          </div>
        </div>
        <div class="dist-cols" style="margin-top:14px">
          <div>
            <div class="dist-row" style="color:var(--muted);font-size:12px;font-weight:600"><span class="lab">月份分布</span><span class="track"></span><span class="num">条数</span></div>
            <div id="dist-month"></div>
          </div>
          <div>
            <div class="dist-row" style="color:var(--muted);font-size:12px;font-weight:600"><span class="lab">型号 Top</span><span class="track"></span><span class="num">条数</span></div>
            <div id="dist-model"></div>
          </div>
        </div>
      </div>

      <div class="panel">
        <h3>差评商品榜（≤3星占比最高）<span class="sub" id="ls-sub"></span></h3>
        <div id="lowstar"></div>
      </div>

      <div class="panel">
        <h3>原始评论数据 <span class="sub">点击任意行展开完整评论</span></h3>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>ASIN</th><th>星级</th><th>国家</th><th>型号</th><th>时间</th><th>评论摘要</th>
              </tr>
            </thead>
            <tbody id="raw-body"></tbody>
          </table>
        </div>
      </div>

      <div class="empty" id="empty-state" style="display:none">没有符合当前筛选条件的评论，试试放宽条件。</div>
    </div>
  </main>
</div>
'''

JS = r'''
var AMZ_COLS = ["asin","title","content","star","votes","video","image","country","model","date"];
var AMZ_ROWS = __ROWS__;
(function(){
  "use strict";
  var $ = function(s){ return document.querySelector(s); };
  var $$ = function(s){ return Array.from(document.querySelectorAll(s)); };

  // 预处理为对象
  var RECORDS = AMZ_ROWS.map(function(r){
    return {
      asin: r[0]||"", title: r[1]||"", content: r[2]||"", star: r[3],
      votes: r[4]||0, video: !!r[5], image: !!r[6],
      country: r[7]||"未知", model: r[8]||"未知", date: r[9]||""
    };
  });

  var TOTAL = RECORDS.length;
  var NULL_STAR = RECORDS.filter(function(r){return r.star==null;}).length;

  function blankFacets(){
    return {starMax:null, starMin:null, country:null, hasVideo:false, hasImage:false, recentOnly:false, oldOnly:false};
  }
  var state = { facets: blankFacets(), sort:"cnt_desc" };

  // 自然语言解析
  function parseQuery(q){
    var f = blankFacets();
    if(!q || !q.trim()) return f;
    var ql = q.toLowerCase();
    if(/差评|低分|不满意|吐槽|负面/.test(ql)) f.starMax = 3;
    if(/好评|高分|优质|满意|正面/.test(ql)) f.starMin = 4;
    var m = q.match(/([\d.]+)\s*星\s*(?:以下|以内|低于|小于|不高于|≤)/);
    if(m) f.starMax = parseFloat(m[1]);
    m = q.match(/([\d.]+)\s*星\s*(?:以上|高于|超过|大于|不低于|≥)/);
    if(m) f.starMin = parseFloat(m[1]);
    if(/美国|us\b|usa/.test(ql)) f.country = "US";
    if(/加拿大|canada|ca\b/.test(ql)) f.country = "CA";
    if(/视频|video/.test(ql)) f.hasVideo = true;
    if(/图|image|picture|有图/.test(ql)) f.hasImage = true;
    if(/近3月|近三月|最近三月|近期/.test(ql)) f.recentOnly = true;
    if(/老|早期|旧|早期评论/.test(ql)) f.oldOnly = true;
    if(/评论数|评论优先|数量优先/.test(ql)) state.sort = "cnt_desc";
    if(/评分优先|高分优先/.test(ql)) state.sort = "star_desc";
    if(/差评优先|差评数/.test(ql)) state.sort = "bad_desc";
    if(/最新|按时间/.test(ql)) state.sort = "date_desc";
    return f;
  }

  function facetsToText(f){
    var parts = [];
    if(f.starMax != null) parts.push("星级≤"+f.starMax);
    if(f.starMin != null) parts.push("星级≥"+f.starMin);
    if(f.country) parts.push(f.country+" 评论");
    if(f.hasVideo) parts.push("有视频");
    if(f.hasImage) parts.push("有图");
    if(f.recentOnly) parts.push("近3月");
    if(f.oldOnly) parts.push("早期评论");
    return parts;
  }

  function matches(r,f){
    if(f.starMax != null && (r.star==null || r.star>f.starMax)) return false;
    if(f.starMin != null && (r.star==null || r.star<f.starMin)) return false;
    if(f.country && r.country !== f.country) return false;
    if(f.hasVideo && !r.video) return false;
    if(f.hasImage && !r.image) return false;
    if(f.recentOnly && r.date < "2026-04") return false;
    if(f.oldOnly && r.date >= "2026-04") return false;
    return true;
  }

  function filtered(){
    var f = state.facets;
    var arr = RECORDS.filter(function(r){ return matches(r,f); });
    var s = state.sort;
    arr.sort(function(a,b){
      if(s==="star_desc") return (b.star||0)-(a.star||0);
      if(s==="star_asc") return (a.star||99)-(b.star||99);
      if(s==="bad_desc") return ((b.star!=null&&b.star<=3)?1:0)-((a.star!=null&&a.star<=3)?1:0) || (b.votes||0)-(a.votes||0);
      if(s==="date_desc") return (b.date||"")>(a.date||"")?1:-1;
      return (b.votes||0)-(a.votes||0);
    });
    return arr;
  }

  function pct(n,d){ return d? Math.round(n/d*100):0; }
  function uniqAsin(arr){ var s={}; arr.forEach(function(r){ if(r.asin) s[r.asin]=1; }); return Object.keys(s).length; }

  function renderKPIs(arr){
    var total = arr.length;
    var rated = arr.filter(function(r){return r.star!=null;});
    var avgStar = rated.length? (rated.reduce(function(a,b){return a+b.star;},0)/rated.length):null;
    var good = rated.filter(function(r){return r.star>=4;}).length;
    var img = arr.filter(function(r){return r.image;}).length;
    var vid = arr.filter(function(r){return r.video;}).length;
    var cards = [
      {n: total.toLocaleString(), l:"命中评论数", s:"共 "+TOTAL.toLocaleString()+" 条"},
      {n: uniqAsin(arr).toLocaleString(), l:"覆盖商品(ASIN)", s:"共 386 款"},
      {n: avgStar!=null? avgStar.toFixed(2)+"★":"—", l:"平均星级", s:rated.length+" 条有评分"},
      {n: rated.length? pct(good,rated.length)+"%":"—", l:"好评率(4-5★)", s:good+" / "+rated.length+" 条"},
      {n: pct(img,total)+"%", l:"含图率", s:img+" 条有图"},
      {n: pct(vid,total)+"%", l:"含视频率", s:vid+" 条有视频"}
    ];
    $("#kpis").innerHTML = cards.map(function(c){ return '<div class="stat"><div class="n">'+c.n+'</div><div class="l">'+c.l+'</div><div class="s">'+c.s+'</div></div>'; }).join("");
  }

  function distBars(id, pairs){
    var max = Math.max(1, Math.max.apply(null, pairs.map(function(p){return p.v;})));
    $(id).innerHTML = pairs.map(function(p){
      return '<div class="dist-row"><span class="lab" title="'+esc(p.k)+'">'+esc(p.k)+'</span><span class="track"><span class="fill" style="width:'+Math.round(p.v/max*100)+'%"></span></span><span class="num">'+p.v.toLocaleString()+'</span></div>';
    }).join("");
  }

  function renderDist(arr){
    // 星级
    var sb = [1,2,3,4,5].map(function(s){ return {k:s+"★", v: arr.filter(function(r){return r.star===s;}).length}; });
    distBars("#dist-star", sb);
    // 国家
    var cmap = {}; arr.forEach(function(r){ cmap[r.country]=(cmap[r.country]||0)+1; });
    var cp = Object.entries(cmap).sort(function(a,b){return b[1]-a[1];}).slice(0,8).map(function(e){return {k:e[0],v:e[1]};});
    distBars("#dist-country", cp);
    // 月份
    var mmap = {}; arr.forEach(function(r){ var m=r.date.slice(0,7); if(m) mmap[m]=(mmap[m]||0)+1; });
    var mp = Object.entries(mmap).sort().map(function(e){return {k:e[0],v:e[1]};});
    distBars("#dist-month", mp);
    // 型号
    var vmap = {}; arr.forEach(function(r){ if(r.model && r.model!=="未知") vmap[r.model]=(vmap[r.model]||0)+1; });
    var vp = Object.entries(vmap).sort(function(a,b){return b[1]-a[1];}).slice(0,8).map(function(e){return {k:e[0],v:e[1]};});
    distBars("#dist-model", vp);
  }

  // 差评商品榜：按 ASIN 聚合，差评率最高（≥5 条评论）
  function renderLowStar(arr){
    var map = {};
    arr.forEach(function(r){
      if(!r.asin) return;
      if(!map[r.asin]) map[r.asin] = {asin:r.asin, n:0, bad:0, sum:0, rated:0, snip:""};
      var o = map[r.asin]; o.n++;
      if(r.star!=null){ o.sum+=r.star; o.rated++; if(r.star<=3){ o.bad++; if(!o.snip && r.content) o.snip=r.content; } }
    });
    var list = Object.values(map).filter(function(o){return o.n>=5;});
    list.sort(function(a,b){ var ra=a.bad/a.n, rb=b.bad/b.n; if(rb!==ra) return rb-ra; return b.bad-a.bad; });
    list = list.slice(0,12);
    $("#ls-sub").textContent = list.length? ("共 "+list.length+" 款（差评率≥5条评论）") : "当前筛选无满足条件的商品";
    if(!list.length){ $("#lowstar").innerHTML = '<div style="color:var(--muted);font-size:13px;padding:6px 0">当前筛选条件下没有差评商品。</div>'; return; }
    $("#lowstar").innerHTML = list.map(function(o,i){
      var avg = o.rated? (o.sum/o.rated).toFixed(2):"—";
      return '<div class="ls-item"><div class="ls-rank">'+(i+1)+'</div><div class="ls-body">'+
        '<div class="ls-title">'+esc(o.asin)+'</div>'+
        '<div class="ls-meta"><span>评论 <b>'+o.n+'</b></span><span>均分 <b style="color:var(--danger)">'+avg+'</b></span><span>差评 <b>'+o.bad+'</b></span>'+
        '<span class="pill no">差评率 '+pct(o.bad,o.n)+'%</span></div>'+
        (o.snip? '<div class="ls-snip">“'+esc(o.snip)+'”</div>':'')+
        '</div></div>';
    }).join("");
  }

  function renderTable(arr){
    var body = $("#raw-body");
    var lim = arr.slice(0,200);
    body.innerHTML = lim.map(function(r,i){
      return '<tr data-i="'+i+'"><td class="ttitle">'+esc(r.asin)+'</td><td class="star">'+(r.star!=null?r.star+"★":"—")+'</td>'+
        '<td>'+esc(r.country)+'</td><td>'+esc(r.model)+'</td><td>'+(r.date||"—")+'</td>'+
        '<td>'+esc(r.content.slice(0,60))+(r.content.length>60?"…":"")+'</td></tr>'+
        '<tr class="detail-row" data-di="'+i+'" style="display:none"><td colspan="6"><div class="detail-inner">'+esc(r.content)+
        '\n\n— 评论标题：'+esc(r.title)+'　赞同数：'+r.votes+(r.video?'　有视频':'')+(r.image?'　有图':'')+'</div></td></tr>';
    }).join("");
    body.querySelectorAll("tr[data-i]").forEach(function(tr){
      tr.addEventListener("click", function(){
        var i = tr.getAttribute("data-i");
        var dr = body.querySelector('tr.detail-row[data-di="'+i+'"]');
        var open = dr.style.display==="none";
        dr.style.display = open?"table-row":"none";
        tr.classList.toggle("open", open);
      });
    });
    $("#empty-state").style.display = arr.length? "none":"block";
  }

  function esc(s){ return String(s==null?"":s).replace(/[&<>"']/g, function(c){ return ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]); }); }
  function kv(k,v){ return '<div class="kv"><span class="k">'+esc(k)+'</span><span class="v">'+esc(v)+'</span></div>'; }

  function render(){
    var arr = filtered();
    $("#hit-count").textContent = arr.length.toLocaleString();
    $("#asin-count").textContent = uniqAsin(arr).toLocaleString();
    renderKPIs(arr);
    renderDist(arr);
    renderLowStar(arr);
    renderTable(arr);
    $("#sort-sel").value = state.sort;
  }

  var CHIP_DEFS = [
    {key:"starLow", label:"1-3星差评", apply:function(f){f.starMax=3;}},
    {key:"starHigh", label:"4-5星好评", apply:function(f){f.starMin=4;}},
    {key:"us", label:"美国", apply:function(f){f.country="US";}},
    {key:"ca", label:"加拿大", apply:function(f){f.country="CA";}},
    {key:"video", label:"有视频", apply:function(f){f.hasVideo=true;}},
    {key:"image", label:"有图", apply:function(f){f.hasImage=true;}},
    {key:"recent", label:"近3月", apply:function(f){f.recentOnly=true;}},
    {key:"old", label:"早期评论", apply:function(f){f.oldOnly=true;}}
  ];
  var chipState = {};
  function renderChips(){
    $("#chips").innerHTML = CHIP_DEFS.map(function(c){ return '<span class="chip '+(chipState[c.key]?'on':'')+'" data-key="'+c.key+'">'+c.label+'</span>'; }).join("");
    $("#chips").querySelectorAll(".chip").forEach(function(el){
      el.addEventListener("click", function(){
        var key = el.dataset.key;
        chipState[key] = !chipState[key];
        var f = blankFacets();
        CHIP_DEFS.filter(function(c){return chipState[c.key];}).forEach(function(c){c.apply(f);});
        state.facets = f;
        ACTIVE_VIEW_ID = null; document.querySelector('.src-card') && document.querySelector('.src-card').classList.remove('active');
        document.querySelectorAll('.vl-item').forEach(function(el){el.classList.remove('active');});
        showUnderstood(); renderChips(); render();
      });
    });
  }
  function showUnderstood(){
    var parts = facetsToText(state.facets);
    $("#understood").textContent = parts.length? ("已应用筛选：" + parts.join(" · ")) : "";
  }

  $("#nl-input").addEventListener("input", function(e){
    var q = e.target.value;
    state.facets = parseQuery(q);
    Object.keys(chipState).forEach(function(k){chipState[k]=false;});
    ACTIVE_VIEW_ID = null; document.querySelector('.src-card') && document.querySelector('.src-card').classList.remove('active');
    document.querySelectorAll('.vl-item').forEach(function(el){el.classList.remove('active');});
    showUnderstood(); renderChips(); render();
  });
  $("#sort-sel").addEventListener("change", function(e){ state.sort=e.target.value; render(); });
  $("#clear-btn").addEventListener("click", function(){
    state.facets = blankFacets();
    Object.keys(chipState).forEach(function(k){chipState[k]=false;});
    $("#nl-input").value=""; $("#understood").textContent="";
    setActiveView('source'); renderChips(); render();
  });

  // 视图图层
  var SAVED_VIEWS = [];
  var ACTIVE_VIEW_ID = null;
  var _viewIdCounter = 0;
  function cloneFacets(f){ return JSON.parse(JSON.stringify(f)); }
  function cloneChipState(cs){ var o={}; Object.keys(cs).forEach(function(k){o[k]=cs[k];}); return o; }
  function generateViewName(){
    var parts = facetsToText(state.facets);
    if(!parts.length) return "全部评论（无筛选）";
    return parts.join(" + ");
  }
  function saveCurrentView(){
    var currentKey = JSON.stringify({f:state.facets,s:state.sort});
    var dup = SAVED_VIEWS.find(function(v){return v.key===currentKey;});
    if(dup){ toast("该筛选组合已存在："+dup.name); setActiveView(dup.id); return; }
    _viewIdCounter++;
    var view = {id:_viewIdCounter, name:generateViewName(), facets:cloneFacets(state.facets), sort:state.sort, chipState:cloneChipState(chipState), hitCount:filtered().length, key:currentKey, createdAt:new Date().toLocaleTimeString('zh-CN',{hour:'2-digit',minute:'2-digit'})};
    SAVED_VIEWS.push(view); setActiveView(view.id); renderViewLayers(); toast("已保存视图："+view.name);
  }
  function loadView(id){
    var view = SAVED_VIEWS.find(function(v){return v.id===id;});
    if(!view) return;
    state.facets = cloneFacets(view.facets);
    state.sort = view.sort || "cnt_desc";
    Object.keys(chipState).forEach(function(k){chipState[k]=false;});
    Object.keys(view.chipState).forEach(function(k){if(view.chipState[k])chipState[k]=true;});
    $("#nl-input").value = ""; showUnderstood(); renderChips(); render(); setActiveView(id);
  }
  function deleteView(id,e){
    if(e) e.stopPropagation();
    SAVED_VIEWS = SAVED_VIEWS.filter(function(v){return v.id!==id;});
    if(ACTIVE_VIEW_ID===id) ACTIVE_VIEW_ID=null;
    renderViewLayers();
  }
  function setActiveView(id){
    ACTIVE_VIEW_ID=id;
    var srcCard = document.querySelector('.src-card');
    if(srcCard) srcCard.classList.toggle('active', id==='source');
    document.querySelectorAll('.vl-item').forEach(function(el){ el.classList.toggle('active', el.dataset.vid===String(id)); });
  }
  function renderViewLayers(){
    var list = $("#vlList"); var countEl = $("#vlCount");
    countEl.textContent = String(SAVED_VIEWS.length);
    if(!SAVED_VIEWS.length){ list.innerHTML = '<div class="vl-empty">筛选后点「保存为新视图」<br>即可在此保存多组筛选条件</div>'; return; }
    list.innerHTML = SAVED_VIEWS.map(function(v){
      var isActive=(v.id===ACTIVE_VIEW_ID);
      return '<div class="vl-item'+(isActive?' active':'')+'" data-vid="'+v.id+'" role="button" tabindex="0"><span class="vl-dot"></span>'+
        '<span class="vl-name" title="'+esc(v.name)+'">'+esc(v.name)+'</span><span class="vl-meta">'+v.hitCount+'条</span>'+
        '<span class="vl-del" onclick="deleteView('+v.id+',event)" title="删除此视图">✕</span></div>';
    }).join("");
  }
  function toast(msg){
    var t=document.getElementById('toast');
    if(!t){ t=document.createElement('div'); t.id='toast'; t.style.cssText='position:fixed;top:18px;left:50%;transform:translateX(-50%);z-index:9999;padding:8px 18px;border-radius:10px;font-size:12.5px;font-weight:600;color:#fff;background:rgba(0,0,0,.76);backdrop-filter:blur(8px);pointer-events:none;opacity:0;transition:opacity .25s'; document.body.appendChild(t); }
    t.textContent=msg; t.style.opacity='1'; clearTimeout(toast._tm); toast._tm=setTimeout(function(){t.style.opacity='0';},2000);
  }
  $("#saveViewBtn").addEventListener("click", saveCurrentView);
  $("#vlList").addEventListener("click", function(e){
    if(e.target.closest('.vl-del')) return;
    var item = e.target.closest('.vl-item'); if(!item) return;
    var vid = Number(item.dataset.vid); if(vid>0) loadView(vid);
  });
  $("#vlList").addEventListener("keydown", function(e){
    if(e.key!=='Enter' && e.key!==' ') return;
    var item = e.target.closest('.vl-item'); if(!item) return;
    e.preventDefault(); var vid = Number(item.dataset.vid); if(vid>0) loadView(vid);
  });
  document.querySelector('.src-card').addEventListener('click', function(){
    state.facets = blankFacets();
    Object.keys(chipState).forEach(function(k){chipState[k]=false;});
    state.sort='cnt_desc'; $("#nl-input").value=""; $("#understood").textContent=""; showUnderstood(); renderChips(); render(); setActiveView('source');
  });
  setActiveView('source');

  // 购物车
  var CART_COLUMNS = [
    {key:'asin',label:'ASIN'},{key:'star',label:'星级'},{key:'country',label:'国家'},{key:'model',label:'型号'},
    {key:'date',label:'时间'},{key:'votes',label:'赞同数'},{key:'video',label:'视频'},{key:'image',label:'图片'},{key:'content',label:'评论'}
  ];
  var _cartAddedFilter = '';
  function updateCartButtonState(){
    var btn = document.getElementById('cartBtn');
    var curFp = generateViewName();
    if(_cartAddedFilter && _cartAddedFilter===curFp){
      btn.classList.add('cart-added');
      btn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="width:15px;height:15px;vertical-align:-2px;margin-right:4px"><path d="M20 6L9 17l-5-5"/></svg>已加入购物车';
    } else {
      btn.classList.remove('cart-added');
      btn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:15px;height:15px;vertical-align:-2px;margin-right:4px"><circle cx="9" cy="20" r="1.3"/><circle cx="17" cy="20" r="1.3"/><path d="M2 3h2.4l2.1 12.3a1.6 1.6 0 0 0 1.6 1.3h9.1a1.6 1.6 0 0 0 1.6-1.3L21.5 7H5.4"/></svg>加入购物车';
    }
  }
  var _lastRenderFp = '';
  var _origRender = render;
  render = function(){ _origRender(); var fp = generateViewName(); if(fp!==_lastRenderFp){ _lastRenderFp=fp; updateCartButtonState(); } };
  function addToCart(){
    var arr = filtered();
    if(!arr.length){ toast('当前筛选结果为空，无法加入购物车'); return; }
    var items = arr.map(function(r){ var o={}; CART_COLUMNS.forEach(function(c){ o[c.key]=r[c.key]; }); return o; });
    var item = {id:'cart_'+Date.now()+'_'+Math.floor(Math.random()*9999), source:'美亚评论 · 倒膜&名器', sourceKey:'amz', filter:generateViewName(), count:arr.length, addedAt:new Date().toISOString(), columns:CART_COLUMNS, items:items, _sel:true};
    try{ window.parent.postMessage({type:'cih-cart-add', item:item}, '*'); }catch(e){}
    _cartAddedFilter = generateViewName(); updateCartButtonState();
    if(window.parent===window){
      var key='cih_cart_v1'; var a=[];
      try{ a=JSON.parse(localStorage.getItem(key))||[]; }catch(e){}
      var dup=a.find(function(x){return x.source===item.source && x.filter===item.filter;});
      if(dup){ dup.items=item.items; dup.count=item.count; dup.addedAt=item.addedAt; }
      else a.push(item);
      try{ localStorage.setItem(key, JSON.stringify(a)); }catch(e){}
      toast('已加入购物车（'+arr.length+' 条）');
    } else { toast('已发送到购物车'); }
  }
  $("#cartBtn").addEventListener("click", addToCart);

  renderChips();
  render();
})();

function goBack(){
  if(window.self!==window.top){ try{parent.postMessage('hub:back','*');}catch(e){} }
  else { window.location.href='category-insight-hub.html'; }
}
(function(){
  var btn = document.getElementById('fsBtn'); if(!btn) return;
  var fsIcon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3H5a2 2 0 0 0-2 2v3"/><path d="M21 8V5a2 2 0 0 0-2-2h-3"/><path d="M3 16v3a2 2 0 0 0 2 2h3"/><path d="M16 21h3a2 2 0 0 0 2-2v-3"/></svg>';
  var exitIcon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 14h6v6"/><path d="M20 10h-6V4"/><path d="M14 10l7-7"/><path d="M3 21l7-7"/></svg>';
  function updateIcon(){
    var isFS = !!(document.fullscreenElement || document.webkitFullscreenElement || document.mozFullScreenElement);
    btn.innerHTML = (isFS ? exitIcon : fsIcon) + (isFS ? '退出全屏' : '全屏');
    btn.title = isFS ? '退出全屏（或按 ESC）' : '全屏查看看板';
  }
  btn.addEventListener('click', function(){
    if(!document.fullscreenElement && !document.webkitFullscreenElement && !document.mozFullScreenElement){
      var el = document.documentElement;
      (el.requestFullscreen || el.webkitRequestFullscreen || el.mozRequestFullScreen || function(){}).call(el);
    } else {
      (document.exitFullscreen || document.webkitExitFullscreen || document.mozCancelFullScreen || function(){}).call(document);
    }
  });
  document.addEventListener('fullscreenchange', updateIcon);
  document.addEventListener('webkitfullscreenchange', updateIcon);
})();
'''

rows_json = json.dumps(out_rows, ensure_ascii=False, separators=(',', ':'))
html = ('<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<title>美亚倒膜 & 名器 · 商品评论看板</title>\n<style>\n' + CSS + '\n</style>\n</head>\n'
        + HTML_BODY.replace('__TOTAL__', '{:,}'.format(TOTAL))
        + '<script>\n' + JS.replace('__ROWS__', rows_json) + '\n</script>\n</body>\n</html>\n')

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(html)
print("已写出:", OUT, "大小:", round(len(html.encode('utf-8'))/1024/1024, 2), "MB")
