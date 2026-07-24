import pandas as pd
import re
import time
import random
from collections import defaultdict


class PipelineEngine:
    def __init__(self, taggers):
        self.taggers = taggers
        self.dimensions = list(taggers.keys())

    def stage1_coarse_match(self, text):
        """阶段一：粗匹配（高召回、宁多勿漏）"""
        result = {}
        for dim_name, tagger in self.taggers.items():
            labels, hits = tagger.tag(text)
            result[f'{dim_name}_标签'] = labels
            result[f'{dim_name}_命中词'] = hits
        return result

    def stage2_fine_filter(self, text, stage1_result):
        """阶段二：精确筛选（上下文验证+排除规则）"""
        result = {}
        for dim_name in self.dimensions:
            labels = stage1_result.get(f'{dim_name}_标签', [])
            hits = stage1_result.get(f'{dim_name}_命中词', [])
            
            filtered_labels = []
            filtered_hits = []
            
            for label, hit in zip(labels, hits):
                if self._is_valid_label(text, dim_name, label, hit):
                    filtered_labels.append(label)
                    filtered_hits.append(hit)
            
            result[f'{dim_name}_标签'] = filtered_labels
            result[f'{dim_name}_命中词'] = filtered_hits
        return result

    def _is_valid_label(self, text, dim_name, label, hit):
        """验证标签是否有效（基于上下文和排除规则）"""
        text_lower = text.lower()
        
        exclusion_rules = self._get_exclusion_rules(dim_name, label)
        for pattern, reason in exclusion_rules:
            if re.search(pattern, text_lower):
                return False
        
        context_rules = self._get_context_rules(dim_name, label)
        if context_rules:
            for pattern in context_rules:
                if re.search(pattern, text_lower):
                    return True
            return False
        
        return True

    def _get_exclusion_rules(self, dim_name, label):
        """获取排除规则"""
        rules = {
            '用户画像': {
                '单身男性用户': [
                    (r'\bsolo (play|use|session|time)\b', 'solo指使用方式'),
                    (r'\balone (time|moment|just|only)\b', 'alone指独处而非单身'),
                ],
                '女性用户': [
                    (r'\bshe (is|was|has|does|looks)\b', 'she指产品拟人化'),
                ],
                '资深用户/收藏家': [
                    (r'\badd to collection\b', '营销话术'),
                    (r'\bcollection (page|item|store)\b', '电商集合页'),
                ],
            },
            '购买动机': {
                '送礼': [
                    (r'\bgift for myself\b', '给自己买'),
                ],
            },
            '购买目的': {
                '练习持久/技巧提升': [
                    (r'\bdurab', '产品耐用性'),
                    (r'\b(lasts? long)(?!.*(in bed|sex|ejaculatio))', '产品寿命'),
                ],
                '收藏/展示爱好': [
                    (r'\b(one of )?my favorites?\b', '最喜欢不等于收藏'),
                ],
            },
            '使用场景': {
                '卧室/床上使用': [
                    (r'\b(go to|come to|stay in|sleep in) bed\b', '指睡觉'),
                ],
            },
            '使用障碍': {
                '材质不真实/像橡胶': [
                    (r'\bsilicone (is|feels|material)\b', '正常材质描述'),
                ],
            },
        }
        return rules.get(dim_name, {}).get(label, [])

    def _get_context_rules(self, dim_name, label):
        """获取上下文验证规则"""
        rules = {
            '用户画像': {
                '单身男性用户': [
                    r'\b(i.?m|i am|as a) single\b',
                    r'\bno (girlfriend|wife|partner)\b',
                ],
                '已婚/有伴侣男性': [
                    r'\b(my wife|my girlfriend|my partner)\b',
                ],
            },
            '购买目的': {
                '练习持久/技巧提升': [
                    r'\b(last longer|endurance|stamina|premature)\b',
                ],
            },
        }
        return rules.get(dim_name, {}).get(label, [])

    def stage3_llm_validate(self, df, text_col, sample_ratio=0.1, max_iterations=3, target_accuracy=0.8):
        """阶段三：LLM抽样验证（多轮迭代）"""
        import subprocess
        import json
        
        results = []
        accuracy_history = []
        
        for iteration in range(max_iterations):
            print(f"\n=== 阶段三 - 第 {iteration+1} 轮 LLM 验证 ===")
            
            sample_size = int(len(df) * sample_ratio)
            sample = df.sample(n=sample_size, random_state=iteration)
            
            errors_found = 0
            corrections = []
            
            for _, row in sample.iterrows():
                text = str(row[text_col])
                current_labels = {}
                for dim in self.dimensions:
                    current_labels[dim] = row.get(f'{dim}_标签', '')
                
                llm_feedback = self._simulate_llm_validation(text, current_labels)
                
                if llm_feedback['errors']:
                    errors_found += 1
                    corrections.append({
                        'text': text,
                        'original': current_labels,
                        'corrected': llm_feedback['corrected'],
                    })
            
            accuracy = 1 - (errors_found / sample_size)
            accuracy_history.append(accuracy)
            print(f"  抽样 {sample_size} 条，发现错误 {errors_found} 条")
            print(f"  当前准确率: {accuracy*100:.1f}%")
            
            for correction in corrections:
                mask = df[text_col] == correction['text']
                for dim, labels in correction['corrected'].items():
                    df.loc[mask, f'{dim}_标签'] = labels
            
            if accuracy >= target_accuracy:
                print(f"  ✅ 达到目标准确率 {target_accuracy*100:.0f}%，停止迭代")
                break
        
        return df, accuracy_history

    def _simulate_llm_validation(self, text, current_labels):
        """模拟LLM验证（实际使用时替换为真实LLM调用）"""
        text_lower = text.lower()
        errors = []
        corrected = current_labels.copy()
        
        if '使用障碍' in current_labels:
            obstacles = current_labels['使用障碍']
            positive_words = ['love', 'great', 'amazing', 'awesome', 'perfect', 'excellent', 
                              'best', 'wonderful', 'fantastic', 'beautiful', 'good']
            
            has_positive = any(word in text_lower for word in positive_words)
            if has_positive and obstacles:
                errors.append("正面评价被误标为使用障碍")
                corrected['使用障碍'] = ''
        
        if '产品改进建议' in current_labels:
            suggestions = current_labels['产品改进建议']
            if '外观优化' in suggestions and ('beautiful' in text_lower or 'great looking' in text_lower):
                errors.append("正面外观评价被误标为改进建议")
                corrected['产品改进建议'] = suggestions.replace('外观优化', '').strip('、')
        
        return {'errors': errors, 'corrected': corrected}

    def stage4_scheduler_review(self, df, text_col):
        """阶段四：调度器检查（逐条审核）"""
        print("\n=== 阶段四 - 调度器逐条检查 ===")
        
        corrections = 0
        for i, row in df.iterrows():
            text = str(row[text_col])
            
            stage2_result = {}
            for dim in self.dimensions:
                stage2_result[f'{dim}_标签'] = row.get(f'{dim}_标签', [])
            
            review_result = self._review_single(text, stage2_result)
            
            has_changes = False
            for dim in self.dimensions:
                old_val = row.get(f'{dim}_标签', '')
                new_val = review_result.get(f'{dim}_标签', '')
                if old_val != new_val:
                    df.loc[i, f'{dim}_标签'] = new_val
                    has_changes = True
            
            if has_changes:
                corrections += 1
        
        print(f"  检查 {len(df)} 条，修正 {corrections} 条")
        return df

    def _review_single(self, text, current_result):
        """单条审核"""
        result = current_result.copy()
        
        text_lower = text.lower()
        text_len = len(text)
        
        for dim in self.dimensions:
            labels = result.get(f'{dim}_标签', [])
            
            if dim == '使用场景' and not labels and text_len > 20:
                if any(keyword in text_lower for keyword in ['bed', 'night', 'evening', 'before sleep']):
                    result[f'{dim}_标签'] = ['卧室/床上使用']
                elif any(keyword in text_lower for keyword in ['shower', 'bath', 'bathroom']):
                    result[f'{dim}_标签'] = ['浴室/洗澡时']
                elif any(keyword in text_lower for keyword in ['alone', 'myself', 'by myself']):
                    result[f'{dim}_标签'] = ['独处时/家中']
        
        return result

    def stage5_final_verify(self, df, text_col):
        """阶段五：二次验证（生成准确率报告）"""
        print("\n=== 阶段五 - 最终验证 ===")
        
        report = {
            'total_records': len(df),
            'dimension_stats': {},
            'accuracy_estimate': {},
        }
        
        for dim in self.dimensions:
            col = f'{dim}_标签'
            has_label = (df[col] != '').sum()
            coverage = has_label / len(df) * 100
            
            all_labels = df[col].str.split('、').explode()
            label_counts = all_labels.value_counts().to_dict()
            
            report['dimension_stats'][dim] = {
                'coverage': f'{coverage:.1f}%',
                'label_counts': label_counts,
            }
            
            report['accuracy_estimate'][dim] = self._estimate_accuracy(df, text_col, dim)
        
        return report

    def _estimate_accuracy(self, df, text_col, dimension):
        """估算各维度准确率"""
        sample_size = min(100, len(df))
        sample = df[df[f'{dimension}_标签'] != ''].sample(n=sample_size)
        
        correct = 0
        for _, row in sample.iterrows():
            text = str(row[text_col])
            labels = row[f'{dimension}_标签']
            
            if self._is_label_correct(text, dimension, labels):
                correct += 1
        
        return f'{correct/sample_size*100:.1f}%' if sample_size > 0 else 'N/A'

    def _is_label_correct(self, text, dimension, labels):
        """检查标签是否正确（简化版）"""
        text_lower = text.lower()
        
        if dimension == '使用障碍':
            if labels and any(word in text_lower for word in ['love', 'great', 'perfect', 'awesome']):
                return False
        
        if dimension == '产品改进建议':
            if labels and '外观优化' in labels and 'beautiful' in text_lower:
                return False
        
        return True

    def run_pipeline(self, df, text_col, use_llm=False):
        """运行完整五阶段流水线"""
        print("=" * 60)
        print("VOC 9维度五阶段打标流水线")
        print("=" * 60)
        
        start_time = time.time()
        
        print("\n--- 阶段一：粗匹配（高召回）---")
        stage1_results = []
        for _, row in df.iterrows():
            text = str(row[text_col])
            stage1_results.append(self.stage1_coarse_match(text))
        
        stage1_df = pd.DataFrame(stage1_results)
        df = pd.concat([df, stage1_df], axis=1)
        print(f"  完成，耗时 {time.time()-start_time:.1f}s")
        
        print("\n--- 阶段二：精确筛选（上下文验证）---")
        stage2_results = []
        for _, row in df.iterrows():
            text = str(row[text_col])
            stage1_result = {f'{d}_标签': row.get(f'{d}_标签', []) for d in self.dimensions}
            stage2_results.append(self.stage2_fine_filter(text, stage1_result))
        
        df.drop([f'{d}_标签' for d in self.dimensions], axis=1, inplace=True)
        stage2_df = pd.DataFrame(stage2_results)
        df = pd.concat([df, stage2_df], axis=1)
        print(f"  完成，耗时 {time.time()-start_time:.1f}s")
        
        if use_llm:
            print("\n--- 阶段三：LLM抽样验证（多轮迭代）---")
            df, accuracy_history = self.stage3_llm_validate(df, text_col)
            print(f"  完成，准确率历史: {accuracy_history}")
        
        print("\n--- 阶段四：调度器检查（逐条审核）---")
        df = self.stage4_scheduler_review(df, text_col)
        print(f"  完成，耗时 {time.time()-start_time:.1f}s")
        
        print("\n--- 阶段五：最终验证（生成报告）---")
        report = self.stage5_final_verify(df, text_col)
        print(f"  完成，总耗时 {time.time()-start_time:.1f}s")
        
        print("\n" + "=" * 60)
        print("打标完成！")
        print("=" * 60)
        
        return df, report
