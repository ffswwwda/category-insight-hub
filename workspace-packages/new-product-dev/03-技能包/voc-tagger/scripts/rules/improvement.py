IMPROVEMENT_RULES = {
    '尺寸调整': {
        'keywords': [
            'too big', 'too small', 'size issue', 'wrong size',
            '尺寸问题', '太大', '太小', '尺寸不合适', '尺寸不对'
        ],
        'context_patterns': [
            r'(too big|too small|size (issue|problem|too|wrong)|尺寸问题|太大|太小)'
        ]
    },
    '材质升级': {
        'keywords': [
            'material', 'silicone', 'soft', 'hard', 'texture',
            '材质', '硅胶', '软', '硬', '质感', '材质问题'
        ],
        'context_patterns': [
            r'(material (too|issue|problem|needs)|材质(问题|升级|改进))'
        ]
    },
    '结构优化': {
        'keywords': [
            'design', 'structure', 'shape', 'ergonomic',
            '设计', '结构', '形状', '人体工学', '设计改进'
        ],
        'context_patterns': [
            r'(design (needs|could|should)|结构(问题|优化)|设计(改进|优化))'
        ]
    },
    '功能增加': {
        'keywords': [
            'wish it had', 'need more', 'add feature', 'function',
            '希望有', '增加功能', '缺少功能', '功能不足'
        ],
        'context_patterns': [
            r'(wish (it|this) (had|had a)|add (feature|function)|增加(功能|特性))'
        ]
    },
    '噪音降低': {
        'keywords': [
            'noise', 'loud', 'quiet', 'sound', 'too loud',
            '噪音', '声音', '太吵', '静音', '声音太大'
        ],
        'context_patterns': [
            r'(noise( issue)?|too loud|噪音(问题)?|太吵)'
        ]
    },
    '续航提升': {
        'keywords': [
            'battery', 'charge', 'last longer', 'battery life',
            '电池', '续航', '充电', '续航时间', '电池寿命'
        ],
        'context_patterns': [
            r'(battery (life|issue|too short)|续航(问题|提升)|电池(寿命|问题))'
        ]
    },
    '清洁方便': {
        'keywords': [
            'clean', 'easy to clean', 'cleaning', 'hard to clean',
            '清洁', '清洗', '难清洁', '容易清洁', '清洁方便'
        ],
        'context_patterns': [
            r'(clean(ing)? (too|issue|hard)|清洁(方便|困难|问题))'
        ]
    },
    '外观优化': {
        'keywords': [
            'looks', 'appearance', 'design', 'aesthetic',
            '外观', '颜值', '好看', '设计', '外观改进'
        ],
        'context_patterns': [
            r'(look(s)? (better|different)|外观(优化|改进)|颜值(提升))'
        ]
    },
    '包装改进': {
        'keywords': [
            'packaging', 'discreet', 'package', 'privacy',
            '包装', '隐私', '保密', '包装改进', '包装设计'
        ],
        'context_patterns': [
            r'(packag(ing|e) (issue|needs)|包装(改进|设计)|隐私(包装))'
        ]
    },
    '价格调整': {
        'keywords': [
            'price', 'expensive', 'cheap', 'affordable', 'worth',
            '价格', '贵', '便宜', '性价比', '价格高', '价格低'
        ],
        'context_patterns': [
            r'(price (too|issue|high|low)|价格(太高|太低|调整)|性价比)'
        ]
    },
    '图文不符': {
        'keywords': [
            'misleading', 'not as described', 'different from picture',
            '图文不符', '描述不符', '和图片不一样', '和描述不符'
        ],
        'context_patterns': [
            r'(misleading|not as (described|shown)|图文不符|描述不符)'
        ]
    },
    '预期管理': {
        'keywords': [
            'expectation', 'expected', 'disappointed', 'not what I expected',
            '预期', '失望', '和想象的不一样', '不如预期'
        ],
        'context_patterns': [
            r'(expect(ation|ed)|disappointed|不如预期|和想象的不一样)'
        ]
    },
    '产品改进建议·未分类': {
        'keywords': [],
    }
}
