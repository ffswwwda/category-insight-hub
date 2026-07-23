# 类目用户研究座 · 项目长期记忆

## 产品核心框架（用户定义，2026-07-16）

### 工作场景的两大细分（最大颗粒度）
1. **从分析用户出发 · 洞察创意为主**（用户洞察方向）
   - 从用户/数据出发，向外洞察：细分市场、机会识别（优化产品 / 开发产品 / 品牌营销等）。
2. **从运营出发 · 分析用户只是其中一环**（运营目的方向）
   - 从一个聚焦的问题/目的出发，反向看用户端口有什么信息、什么分析方法能解决该问题。

### 架构原则（已确认）
- "工作区"设计被用户认可，但**每个目的对应不同的工作区，调用的数据源也不同**。
- 用户将提供 **8 个原始数据源**，需通过工作区体系按目的路由调用（同一源可被多目的引用）。
- 目标部署平台：**GitHub Pages**（静态站点）。

### 当前实现状态
- `category-insight-hub.html`：左侧两工作区（用户洞察 / 运营目的）× 各 4 子板块（数据源/分析框架/AI看板/标签体系）。
- `de-dashboard.html`：德国站看板（248 条内联真实数据），经 iframe 接入"用户洞察→数据源→德国"。
- 数据一律**内联**进 HTML（无 fetch/外部 JSON），对 GitHub Pages 与本地 file:// 均零 CORS 问题 —— 部署友好，继续保持。

### 原理展厅（PRINCIPLE 板块，2026-07-17 起）
- 定位：把每个工具/skill 内部运作做成「小动画」演示（头脑特工隐喻），让用户在安装前看懂原理。默认「使用视角」简单、切「看背后工作」看动画。
- 画廊 `PR_TOOLS` 数组驱动，`ready:true` 的工具卡片 onclick 由 `t.fn+'()'` 动态映射。
- 已有两个可演示 demo（`viewPrDemo` 容器被各 demo 重写）：
  1. **VOC 智能打标** `openTagDemo()`：评论小人穿过「标签体系之墙」9 维度专员流水线（盖章/放行）。
  2. **产品需求打分** `openScoreDemo()`：需求小人「连续跳远」跳进 4 个维度沙坑（痛点匹配/技术可行/市场机会/竞争差异），落点弹分→右侧总分牌。评分引擎 `scoreProduct()` 为关键词词典规则（基础52 + 每命中+13，封顶98）。
- 动画复用模式：CSS transition + 时间轴（`_pt` VOC / `_spt` 打分），runner 用 translateX 水平移动 + WAAPI `jumpRunner()` 跳跃弧。
- 其余 7 个 PR_TOOLS 仍 `ready:false`（敬请期待）。

### 待办（用户定框架后）
- 扩展为 8 源注册表 + 工作区→源映射；每个源一个看板页（如 de-dashboard.html 模式）。
- 分析框架 / AI 看板 / 标签体系 板块补真实内容。

## 图标系统规范（用户确认，2026-07-17）

**模板文件**：`/Users/fsw/WorkBuddy/2026-07-15-15-11-41/radium-design-x/references/icon-system.html`
**原则：绝不使用 emoji，全部用白描 SVG。后续所有图标都按此样式做。**

### 技术形态
- **SVG sprite 方案**：在 `<body>` 开头放一段 `<svg style="position:absolute" width=0 height=0><defs>…<symbol></svg>`，每个图标一个 `<symbol id="i-xxx" viewBox="0 0 24 24">`，使用时 `<svg class="ic-svg"><use href="#i-xxx"/></svg>`。内联、零 CORS，GitHub Pages / file:// 均可用。
- 共享**三色渐变**：`#00d4ff → #a855f7 → #ff6b9d`（135°），gradient id 命名为 `uiGrad`（`<linearGradient x1=0 y1=0 x2=1 y2=1>`）。

### 两类图标
1. **渐变描边图标（UI 类：导航 / 卡片 / 按钮 / 数据源）** — `fill="none" stroke="url(#uiGrad)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"`，viewBox `0 0 24 24`。
   已有 30 个：`i-grid i-sliders i-globe i-gear i-doc i-layers i-compass i-build i-bot i-steps i-zap i-users i-link i-smile i-flame i-clock i-share i-tag i-bar i-plug i-target i-phone i-msg i-box i-trend i-star i-moon i-sun i-swap i-alert`
2. **白色图标（放在渐变底色方块上的品牌 / 流程 / 架构图标）** — `fill="currentColor" stroke="none"` 或 `stroke="currentColor"`，外层 `.box{background:var(--grad)}` 承载。
   已有 9 个：`w-fish w-layers w-chip w-wave w-doc w-chat w-phone w-plug w-bar`

### 已沉淀的可复用图标库（可直接复用，无需重绘）
| 语义 | 渐变描边 id | 白色 id |
|---|---|---|
| 网格/工作台 | `i-grid` | — |
| 滑块/参数 | `i-sliders` | — |
| 地球/全球/数字世界 | `i-globe` | — |
| 齿轮/设置/引擎 | `i-gear` | — |
| 文档/报告 | `i-doc` | `w-doc` |
| 分层/架构 | `i-layers` | `w-layers` |
| 罗盘/方向 | `i-compass` | — |
| 构建/产品 | `i-build` | — |
| 机器人/AI | `i-bot` | — |
| 步骤/流水线 | `i-steps` | — |
| 闪电/快速 | `i-zap` | — |
| 用户群 | `i-users` | — |
| 链接 | `i-link` | — |
| 微笑/情绪 | `i-smile` | — |
| 火焰/热度 | `i-flame` | — |
| 时钟/时间 | `i-clock` | — |
| 分享 | `i-share` | — |
| 标签 | `i-tag` | — |
| 柱状图/数据 | `i-bar` | `w-bar` |
| 插头/接入 | `i-plug` | `w-plug` |
| 靶心/目标 | `i-target` | — |
| 手机 | `i-phone` | `w-phone` |
| 消息 | `i-msg` | `w-chat` |
| 盒子/模块 | `i-box` | `w-chip` |
| 趋势 | `i-trend` | — |
| 星标 | `i-star` | — |
| 月亮/暗色 | `i-moon` | — |
| 太阳/亮色 | `i-sun` | — |
| 交换 | `i-swap` | — |
| 警告 | `i-alert` | — |
| 鱼（品类） | — | `w-fish` |
| 波浪/传播 | — | `w-wave` |

### 注意：category-insight-hub.html 现状偏差
- 站内未来实验室等处的 SVG 当前用紫描边（`stroke="#7c3aed"` / `currentColor`），**与上面三色渐变规范不一致**。
- 后续新增图标按渐变规范做；如需统一旧图标可再批量替换（用户未要求立即改）。
- 该站整体仍保持「干净亮色 + 克制」基底（用户 2026-07-10 偏好），图标渐变仅用于图标描边，不要外溢成大面积强风格背景。

## ai-office-3d 项目沉淀（2026-07-17）
- **位置**：`/Users/fsw/WorkBuddy/2026-07-15-08-51-27/ai-office-3d/`
- **技术栈**：PixiJS v8 + React 19 + Vite 8 + TypeScript（无 Spine 依赖）
- **启动**：`cd ai-office-3d && npm run dev`
- **场景**：3D 等轴测办公室，7 工位（中文同事：小灵/小分/小预/小创/小设/小测/小展）
- **复用建议**：用户研究/数据可视化的"全景项目"模板——PixiJS 程序绘制 2.5D 场景，零图片依赖，可作为独立子项目部署

## 方案包（Plan Package）规范 · 用户已确认（2026-07-22）
**目标**：每个"目的"工作区可下载一个**自包含方案包**，让从没见过项目的 AI 拿到包就能照着分析/产出/核对。
**已确认目录结构**（spec 用户复述认可）：
```
<目的id>/
├── manifest.json          # 机器索引：目的/版本/依赖/血缘
├── 00-README.md           # 人读总览 + 运行顺序
├── 01-提示词/ SYSTEM.md(自包含总提示词) + 数据源说明 + 分析框架说明 + 技能调用说明
├── 02-数据包/ <源>.csv     # 按源筛选过的真实数据
├── 03-技能包/ <skill>/      # SKILL.md + scripts/
├── 04-交付模板/ 输出模板.md + 校验清单.md
└── 05-标签字典/ taxonomy.md  # 可选：VOC九维/13维需求/四象限
```
**用户补充的 5 点（A-E，均已认可需落地）**：A.交付物模板+逐条校验清单；B.包索引 manifest+README；C.标签/维度字典（防打标漂移）；D.运行编排顺序(①manifest→②提示词→③数据→④技能→⑤套模板→⑥校验)；E.(可选)样例交付物+版本血缘。
**关键硬约束（必须写进 SYSTEM.md）**：自包含+强约束——禁止联网/禁外部知识补充；所有结论须引用 `02-数据包/` 具体行号 `[源文件#行号]`；数据不足处标注「数据不足」而非编造。这正是"核对准确"的落地。
**样例包已落地（本地）**：`workspace-packages/new-product-dev/`（31 文件，结构完全对齐 spec，含 9 源 CSV + voc-tagger 技能包 + 六段输出模板 + 校验清单 + taxonomy）。
**生成器已落地（2026-07-22，commit 949616f）**：右栏「导出方案包（.zip）」按钮已改为直接调用 `downloadPlanPackage()` 生成**真·多文件 zip**（零依赖 `makeZip`：store 模式 + CRC32 + UTF-8 文件名，内联无外部库，符合整站零 CORS 约定）。zip 严格按 spec 目录结构组装：`manifest.json`/`00-README.md`/`01-提示词/SYSTEM.md(+数据源/框架/技能说明)`/`02-数据包/<源id>-<源名>.csv`/`03-技能包/voc-tagger/SKILL.md`/`04-交付模板/(输出模板+校验清单)`/`05-标签字典/taxonomy.md`。SYSTEM.md 写死硬约束（禁联网/行级引用/数据不足标注/标签一致/框架不跳步）。
**待决点已拍板（用户 2026-07-22）**：数据包 = 用户在目的工作区**已选源的原始数据，原样导出，不二次加工、不重新跑 voc-tagger 打标**。生成器直接调 `filterSourceRows(sid)`（尊重用户在来源上的筛选）导出 CSV。目的工作区定位本就是"选源/选框架 → 导出给其他 AI 分析"，生成器只照单打包。
**注（macOS 解压）**：zip 字节标准合规（Python zipfile 验证 testzip=None、中文名/内容正确）；但 macOS 命令行 `unzip`(info-zip 旧版) 对 UTF-8 文件名有已知乱码 bug，建议用 Archive Utility / 7zip / Keka / Python 解压。

## Vite + PixiJS v8 常见坑（2026-07-17 实战踩坑）
- **PixiJS Container 的 `label` 字段是内置的**，子类不能重复声明 `private label`，会与 Container 自带的 string 类型冲突。改名 `bubbleLabel` 等
- **TypeScript 6.x `baseUrl` 弃用警告**：tsconfig.app.json 加 `"ignoreDeprecations": "6.0"`
- **ESM 下 vite.config.ts 不能用 `path` + `__dirname`**：改用 `fileURLToPath(new URL('./src', import.meta.url))`
- **PixiJS `Assets.load()` 在文件不存在时会无限挂起**（不抛异常）：必须用 `Promise.race([Assets.load(), new Promise(r => setTimeout(r, 3000))])` 包一层超时
- **store 订阅触发 React 重渲染**：PixiJS 场景里 `setOfficeAgents` 必须在 ticker 每一帧调用，否则 React 组件不更新
