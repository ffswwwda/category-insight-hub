# -*- coding: utf-8 -*-
import csv, json, os

BASE = "/Users/fsw/WorkBuddy/2026-07-15-08-51-27/workspace-packages/new-product-dev"
DATA = os.path.join(BASE, "02-数据包")
os.makedirs(DATA, exist_ok=True)

# 真实样本来自 category-insight-hub.html 的 SOURCE_POOL（项目内联真实 VOC）
# 字段：source_id, source_label, market, text, 数据性质
SOURCES = {
    "s1": {
        "label": "亚马逊评论", "market": "DE/US/JP/UK/EU", "file": "亚马逊评论.csv",
        "rows": [
            ("s1", "亚马逊评论", "DE/US/JP/UK/EU", "我自己加了静音棉，效果还行，但希望出厂就做好，还能调震频。", "真实样本"),
            ("s1", "亚马逊评论", "DE/US/JP/UK/EU", "机器噪音太大，我拆开加了减震垫，建议出厂就考虑静音。", "真实样本"),
            ("s1", "亚马逊评论", "DE/US/JP/UK/EU", "能不能出个可调震频的版本，自己改固件太麻烦。", "真实样本"),
            ("s1", "亚马逊评论", "DE/US/JP/UK/EU", "柜子深度只有30cm，市面上没有合适的，只能将就。", "真实样本"),
            ("s1", "亚马逊评论", "DE/US/JP/UK/EU", "租房党空间小，希望有可伸缩结构适配非标空间。", "真实样本"),
            ("s1", "亚马逊评论", "DE/US/JP/UK/EU", "家里有宠物，怕咬到电线，希望出宠物安全材质的。", "真实样本"),
            ("s1", "亚马逊评论", "DE/US/JP/UK/EU", "能不能做成装饰性外观，能当摆件而非躲起来。", "真实样本"),
            ("s1", "亚马逊评论", "DE/US/JP/UK/EU", "做工粗糙，缝隙不均，工艺细节能再精致点。", "真实样本"),
        ],
    },
    "s13": {
        "label": "美亚倒膜&名器评论", "market": "US", "file": "美亚评论.csv",
        "rows": [
            ("s13", "美亚倒膜&名器评论", "US", "养猫家庭最在意噪音和安全性，市面上几乎没有同时满足这两个的。", "真实样本"),
            ("s13", "美亚倒膜&名器评论", "US", "养宠家庭需要低噪+无毒材质双满足。", "真实样本"),
            ("s13", "美亚倒膜&名器评论", "US", "颜值即正义，现在这款太工业风了。", "真实样本"),
            ("s13", "美亚倒膜&名器评论", "US", "经常出差，希望有便携版本。", "真实样本"),
            ("s13", "美亚倒膜&名器评论", "US", "希望APP能稳定连接，智能联动。", "真实样本"),
        ],
    },
    "s15": {
        "label": "用户反馈情报汇总", "market": "全球", "file": "反馈情报.csv",
        "rows": [
            ("s15", "用户反馈情报汇总", "全球", "安装对租房党不友好，搬了三次家每次拆装。", "真实样本"),
            ("s15", "用户反馈情报汇总", "全球", "安装太复杂，老人不会，需要快装结构。", "真实样本"),
        ],
    },
    "s8": {
        "label": "德国商品库", "market": "DE", "file": "德国商品库.csv",
        "rows": [
            ("s8", "德国商品库", "DE", "我家是老房子，尺寸都不标准，希望能出非标尺寸定制。", "真实样本"),
        ],
    },
    "s3": {
        "label": "竞品分析", "market": "DE/US", "file": "竞品分析.csv",
        "rows": [
            ("s3", "竞品分析", "DE/US", "放客厅不好看，像工业品不像家电，朋友来都觉得尴尬。", "真实样本"),
        ],
    },
    "s12": {
        "label": "Reddit社媒标签", "market": "全球", "file": "Reddit标签.csv",
        "rows": [
            ("s12", "Reddit社媒标签", "全球", "竞品的APP联动做得好，你们蓝牙配对不稳定。", "真实样本"),
            ("s12", "Reddit社媒标签", "全球", "智能家居联动太弱，希望加强。", "真实样本"),
            ("s12", "Reddit社媒标签", "全球", "希望能出免打孔版本，打孔太麻烦。", "真实样本"),
        ],
    },
    "s14": {
        "label": "亚马逊关键词搜索量", "market": "全球", "file": "搜索量.csv",
        "rows": [
            ("s14", "亚马逊关键词搜索量", "全球", "长尾词「静音 可伸缩 家电」月搜索量同比 +38%，蓝海长尾。", "结构示例"),
            ("s14", "亚马逊关键词搜索量", "全球", "「宠物安全 材质 家电」搜索量高位稳定，在售供给少。", "结构示例"),
        ],
    },
    "s20": {
        "label": "核心竞品KOL合作", "market": "全球", "file": "KOL合作.csv",
        "rows": [
            ("s20", "核心竞品KOL合作", "全球", "KOL测评强调「低噪+颜值」卖点，互动率高于类目均值。", "结构示例"),
            ("s20", "核心竞品KOL合作", "全球", "竞品KOL内容主打「APP智能联动」，评论区高频追问稳定性。", "结构示例"),
        ],
    },
    "s9": {
        "label": "类目趋势", "market": "EU/US", "file": "类目趋势.csv",
        "rows": [
            ("s9", "类目趋势", "EU/US", "家居装饰化小型家电类目年增 22%，审美权重上升。", "结构示例"),
            ("s9", "类目趋势", "EU/US", "便携迷你款在差旅人群渗透率上升，供给尚未饱和。", "结构示例"),
        ],
    },
}

HEAD = ["source_id", "source_label", "market", "text", "数据性质"]
for sid, meta in SOURCES.items():
    path = os.path.join(DATA, meta["file"])
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(HEAD)
        for r in meta["rows"]:
            w.writerow(r)
    print("write", meta["file"], len(meta["rows"]), "rows")

# manifest.json
manifest = {
    "package_id": "new-product-dev",
    "purpose": "新品开发 / 创新孵化",
    "core_question": "用户还有哪些未被满足的需求？我该造什么新产品 / 新概念？",
    "version": "1.0.0",
    "generated": "2026-07-22",
    "data_lineage": "样本切片来自 category-insight-hub.html 内联真实 VOC（SOURCE_POOL）与看板；s14/s20/s9 为结构示例，生成器将替换为完整筛选集。",
    "run_order": ["00-README.md", "01-提示词/SYSTEM.md", "02-数据包/*.csv", "03-技能包/voc-tagger/SKILL.md", "04-交付模板/输出模板.md", "04-交付模板/校验清单.md"],
    "sources": [
        {"id": sid, "label": m["label"], "market": m["market"], "file": "02-数据包/" + m["file"], "status": "ready",
         "nature": "真实样本" if any(r[4] == "真实样本" for r in m["rows"]) and not any(r[4] == "结构示例" for r in m["rows"]) else "含结构示例"}
        for sid, m in SOURCES.items()
    ],
    "frameworks": ["quad", "compass", "triz", "extreme", "jtbd", "needs"],
    "skill_dependencies": [
        {"id": "voc-tagger", "path": "03-技能包/voc-tagger/SKILL.md", "required": True, "used_for": "对 02-数据包 中 VOC 评论做九维打标"}
    ],
    "output_template": "04-交付模板/输出模板.md",
    "verify_checklist": "04-交付模板/校验清单.md"
}
with open(os.path.join(BASE, "manifest.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)
print("write manifest.json")
print("total sources:", len(SOURCES))
