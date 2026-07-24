import re
from typing import Dict, List, Tuple, Optional


class Rule:
    def __init__(self, label: str, keywords: List[str],
                 context_patterns: List[str] = None,
                 exclude_patterns: List[str] = None,
                 min_chars: int = 2):
        self.label = label
        self.keywords = [k.lower() for k in keywords]
        self.context_patterns = [re.compile(p, re.IGNORECASE) for p in (context_patterns or [])]
        self.exclude_patterns = [re.compile(p, re.IGNORECASE) for p in (exclude_patterns or [])]
        self.min_chars = min_chars

    def match(self, text: str) -> Tuple[bool, List[str]]:
        text_lower = text.lower()
        matched_keywords = []

        for kw in self.keywords:
            if len(kw) < self.min_chars:
                pattern = r'\b' + re.escape(kw) + r'\b'
                if re.search(pattern, text_lower):
                    matched_keywords.append(kw)
            else:
                if kw in text_lower:
                    matched_keywords.append(kw)

        if not matched_keywords:
            return False, []

        for excl in self.exclude_patterns:
            if excl.search(text):
                return False, []

        if self.context_patterns:
            for pat in self.context_patterns:
                if pat.search(text):
                    return True, matched_keywords
            return False, []

        return True, matched_keywords


class Tagger:
    def __init__(self, rules: Dict[str, List[Rule]], dimension_name: str):
        self.rules = rules
        self.dimension_name = dimension_name

    def tag(self, text: str) -> Tuple[List[str], List[str]]:
        if not text or not isinstance(text, str):
            return [], []
        labels = []
        hits = []
        for label, rule in self.rules.items():
            matched, keywords = rule.match(text)
            if matched:
                labels.append(label)
                hits.extend(keywords)
        return labels, hits


def create_tagger(dimension_name: str, rules_config: dict) -> Tagger:
    rules = {}
    for label, config in rules_config.items():
        rule = Rule(
            label=label,
            keywords=config.get('keywords', []),
            context_patterns=config.get('context_patterns', []),
            exclude_patterns=config.get('exclude_patterns', []),
            min_chars=config.get('min_chars', 2)
        )
        rules[label] = rule
    return Tagger(rules, dimension_name)
