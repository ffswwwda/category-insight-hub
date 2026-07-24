#!/usr/bin/env python3
"""
VOC 9维度规则打标工具 - CLI 主入口
支持两种模式：
1. 快速模式：纯规则引擎，本地运行，速度快
2. 流水线模式：五阶段打标流程（粗匹配→精确筛选→LLM验证→调度器检查→二次验证）
"""

import sys
import os
import argparse
import pandas as pd
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from core import create_tagger, Tagger
from rules.user_profile import USER_PROFILE_RULES
from rules.motivation import MOTIVATION_RULES
from rules.purpose import PURPOSE_RULES
from rules.scenario import SCENARIO_RULES
from rules.obstacle import OBSTACLE_RULES
from rules.solution import SOLUTION_RULES
from rules.loyalty import LOYALTY_RULES
from rules.improvement import IMPROVEMENT_RULES
from rules.thirteen_needs import THIRTEEN_NEEDS_RULES


ALL_DIMENSIONS = {
    '用户画像': USER_PROFILE_RULES,
    '购买动机': MOTIVATION_RULES,
    '购买目的': PURPOSE_RULES,
    '使用场景': SCENARIO_RULES,
    '使用障碍': OBSTACLE_RULES,
    '克服方式': SOLUTION_RULES,
    '用户忠诚度': LOYALTY_RULES,
    '产品改进建议': IMPROVEMENT_RULES,
    '十三种需求': THIRTEEN_NEEDS_RULES,
}


def detect_text_column(df):
    """自动检测文本列"""
    candidates = ['内容', '评论', '评价', '正文', '评论内容', 'review', 'content', 'text', 'comment']
    for col in candidates:
        if col in df.columns:
            return col
    for col in df.columns:
        if df[col].dtype == 'object':
            sample = df[col].dropna().head(20)
            avg_len = sample.str.len().mean()
            if avg_len > 20:
                return col
    return df.columns[0]


def load_taggers(dimensions=None):
    """加载指定维度的打标器"""
    if dimensions is None:
        dimensions = list(ALL_DIMENSIONS.keys())
    
    taggers = {}
    for dim_name in dimensions:
        if dim_name in ALL_DIMENSIONS:
            taggers[dim_name] = create_tagger(dim_name, ALL_DIMENSIONS[dim_name])
    return taggers


def tag_text(taggers, text):
    """对单条文本打所有维度的标签"""
    result = {}
    for dim_name, tagger in taggers.items():
        labels, hits = tagger.tag(text)
        result[f'{dim_name}_标签'] = '、'.join(labels) if labels else ''
        result[f'{dim_name}_命中词'] = '、'.join(hits[:5]) if hits else ''
    return result


def tag_csv(input_path, output_path=None, text_col=None, dimensions=None):
    """批量处理CSV文件（快速模式）"""
    print(f"读取文件: {input_path}")
    df = pd.read_csv(input_path)
    print(f"总条数: {len(df)}")
    
    if text_col is None:
        text_col = detect_text_column(df)
        print(f"自动检测文本列: {text_col}")
    else:
        print(f"使用文本列: {text_col}")
    
    taggers = load_taggers(dimensions)
    print(f"打标维度: {', '.join(taggers.keys())}")
    
    print("\n开始打标...")
    results = []
    total = len(df)
    
    for i, row in df.iterrows():
        text = str(row[text_col]) if pd.notna(row[text_col]) else ''
        tagged = tag_text(taggers, text)
        results.append(tagged)
        
        if (i + 1) % 5000 == 0 or (i + 1) == total:
            print(f"  进度: {i+1}/{total} ({(i+1)/total*100:.1f}%)")
    
    result_df = pd.DataFrame(results)
    df = pd.concat([df, result_df], axis=1)
    
    if output_path is None:
        input_path_obj = Path(input_path)
        output_path = str(input_path_obj.parent / f"{input_path_obj.stem}_已打标.csv")
    
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"\n✅ 完成！输出文件: {output_path}")
    
    print("\n📊 标签统计:")
    for dim_name in taggers.keys():
        col = f'{dim_name}_标签'
        non_empty = (df[col] != '').sum()
        print(f"  {dim_name}: {non_empty} 条有标签 ({non_empty/total*100:.1f}%)")
        if non_empty > 0:
            all_labels = df[col].str.split('、').explode()
            top_labels = all_labels.value_counts().head(5)
            for label, count in top_labels.items():
                if label:
                    print(f"    - {label}: {count} 条")
    
    return df


def tag_single_text(text, dimensions=None):
    """单条文本打标"""
    taggers = load_taggers(dimensions)
    result = tag_text(taggers, text)
    
    print("\n🏷️ 打标结果:")
    print("-" * 40)
    for dim_name in taggers.keys():
        labels = result.get(f'{dim_name}_标签', '')
        hits = result.get(f'{dim_name}_命中词', '')
        if labels:
            print(f"\n【{dim_name}】")
            print(f"  标签: {labels}")
            print(f"  命中词: {hits}")
        else:
            print(f"\n【{dim_name}】: 无匹配标签")


def run_pipeline(input_path, output_path=None, text_col=None, dimensions=None, use_llm=False):
    """运行五阶段打标流水线"""
    from pipeline import PipelineEngine
    
    print(f"读取文件: {input_path}")
    df = pd.read_csv(input_path)
    print(f"总条数: {len(df)}")
    
    if text_col is None:
        text_col = detect_text_column(df)
        print(f"自动检测文本列: {text_col}")
    else:
        print(f"使用文本列: {text_col}")
    
    taggers = load_taggers(dimensions)
    print(f"打标维度: {', '.join(taggers.keys())}")
    
    engine = PipelineEngine(taggers)
    df, report = engine.run_pipeline(df, text_col, use_llm=use_llm)
    
    if output_path is None:
        input_path_obj = Path(input_path)
        output_path = str(input_path_obj.parent / f"{input_path_obj.stem}_五阶段打标.csv")
    
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"\n✅ 流水线完成！输出文件: {output_path}")
    
    print("\n📊 准确率报告:")
    for dim, stats in report['dimension_stats'].items():
        print(f"\n【{dim}】")
        print(f"  覆盖率: {stats['coverage']}")
        print(f"  标签分布: {stats['label_counts']}")
    
    print("\n🎯 各维度准确率估算:")
    for dim, acc in report['accuracy_estimate'].items():
        print(f"  {dim}: {acc}")
    
    return df, report


def main():
    parser = argparse.ArgumentParser(description='VOC 9维度规则打标工具')
    parser.add_argument('input', nargs='?', help='输入CSV文件路径')
    parser.add_argument('--output', '-o', help='输出CSV文件路径')
    parser.add_argument('--text-column', '-c', help='文本内容所在列名')
    parser.add_argument('--dimensions', '-d', help='指定维度，逗号分隔（默认全部）')
    parser.add_argument('--text', '-t', help='单条文本测试')
    parser.add_argument('--list-dimensions', '-l', action='store_true', help='列出所有维度和标签')
    parser.add_argument('--pipeline', '-p', action='store_true', help='使用五阶段打标流水线（更高准确率）')
    parser.add_argument('--use-llm', action='store_true', help='在流水线中使用LLM验证（需配置API）')
    
    args = parser.parse_args()
    
    if args.list_dimensions:
        print("📋 支持的9个维度和标签:")
        for dim_name, rules in ALL_DIMENSIONS.items():
            labels = list(rules.keys())
            print(f"\n【{dim_name}】({len(labels)}个标签)")
            for label in labels:
                print(f"  - {label}")
        return
    
    dimensions = None
    if args.dimensions:
        dimensions = [d.strip() for d in args.dimensions.split(',')]
        for d in dimensions:
            if d not in ALL_DIMENSIONS:
                print(f"❌ 未知维度: {d}")
                print(f"可用维度: {', '.join(ALL_DIMENSIONS.keys())}")
                sys.exit(1)
    
    if args.text:
        tag_single_text(args.text, dimensions)
        return
    
    if args.input:
        if args.pipeline:
            run_pipeline(args.input, args.output, args.text_column, dimensions, use_llm=args.use_llm)
        else:
            tag_csv(args.input, args.output, args.text_column, dimensions)
        return
    
    parser.print_help()


if __name__ == '__main__':
    main()
