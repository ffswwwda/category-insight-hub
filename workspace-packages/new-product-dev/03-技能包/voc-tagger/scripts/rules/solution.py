SOLUTION_RULES = {
    '清洁/保养方法': {
        'keywords': [
            'wash with', 'clean with', 'soap and water',
            'toy cleaner', 'drying', 'air dry', 'powder',
            'cornstarch', 'maintain', 'care for',
            '清洗', '清洁', '保养', '擦干', '晾干', '爽身粉', '滑石粉'
        ],
        'context_patterns': [
            r'(wash (it|this|them) (with|using))',
            r'(clean (it|this|them) (with|using))',
            r'(toy cleaner|soap and water|mild soap)',
            r'(air dry|drying rack|let it dry|cornstarch|powder)',
            r'(清洗|清洁|保养|擦干|晾干|爽身粉)'
        ],
        'exclude_patterns': [
            r'(easy to clean|simple to clean|hard to clean|difficult to clean)',
        ]
    },
    '润滑液使用技巧': {
        'keywords': [
            'lube', 'lubricant', 'lube it up', 'use lube',
            'with lube', 'water based', 'silicone based',
            'add lube', 'plenty of lube',
            '润滑液', '润滑油', '润滑剂', '加润滑', '水溶', '硅基'
        ],
        'context_patterns': [
            r'use (lube|lubricant)',
            r'(with (plenty of|lots of) )?lube',
            r'(water.?based|silicone.?based) (lube|lubricant)',
            r'(润滑液|润滑油|润滑剂|加润滑|水溶|硅基)'
        ],
        'exclude_patterns': [
            r'(no lube needed|lube free|without lube)',
        ]
    },
    '购买建议/选购指南': {
        'keywords': [
            'should buy', 'recommend', 'go for', 'choose',
            'pick the', 'better option', 'best choice',
            'worth buying', 'buy this one', 'if you want',
            '建议买', '推荐', '选购', '选哪个', '值得买', '购买建议'
        ],
        'context_patterns': [
            r'(i (recommend|suggest|advise))',
            r'(you should (buy|choose|get|go for))',
            r'(go for (the |this |that ))',
            r'(worth (buying|getting|the money))',
            r'(best (choice|option|one to buy))',
            r'(建议买|推荐|选购|选哪个|值得买|购买建议)'
        ],
        'exclude_patterns': [
            r'(i wouldn.t recommend|not recommended|don.t buy|waste of money)',
        ]
    },
    '收纳/存放建议': {
        'keywords': [
            'store', 'storage', 'keep in', 'put away',
            'dust bag', 'storage bag', 'box', 'case',
            '收纳', '存放', '保存', '收纳袋', '收纳盒', '防尘'
        ],
        'context_patterns': [
            r'(store (it|them|this) (in|at|on))',
            r'(keep (it|them|this) (in|at|on))',
            r'(storage (bag|box|case|container))',
            r'(dust bag|original packaging)',
            r'(收纳|存放|保存|收纳袋|收纳盒|防尘)'
        ],
        'exclude_patterns': [
            r'(easy to store|compact storage|takes up space)',
        ]
    },
    '加热/降温技巧': {
        'keywords': [
            'warm', 'warm up', 'heated', 'heating',
            'warm water', 'blanket warmer',
            'cool', 'chill', 'cold', 'ice',
            '加热', '加温', '温水', '降温', '冷藏', '冰'
        ],
        'context_patterns': [
            r'(warm (it|this|them) (up|before use))',
            r'(heat (it|this|them) up)',
            r'(warm water (bath|soak))',
            r'(cool (it|this|them) down|chill (it|this|them))',
            r'(加热|加温|温水|降温|冷藏|冰冻)'
        ],
        'exclude_patterns': [
            r'(body temperature|room temperature)',
        ]
    },
    '使用姿势/技巧': {
        'keywords': [
            'position', 'best way', 'how to use',
            'technique', 'method', 'try this', 'tip',
            'angle', 'depth', 'speed',
            '姿势', '技巧', '怎么用', '使用方法', '角度', '速度'
        ],
        'context_patterns': [
            r'(best (position|way|angle|technique))',
            r'(how to (use|enjoy|get the most out of))',
            r'(try (this|that|a different) (position|angle|technique))',
            r'((tip|trick|hack) (for|to))',
            r'(姿势|技巧|怎么用|使用方法|角度)'
        ]
    },
    '爽身粉/保养粉使用': {
        'keywords': [
            'cornstarch', 'baby powder', 'talcum', 'powder',
            'renew powder', 'maintenance powder',
            '爽身粉', '保养粉', '玉米粉', '滑石粉', '去黏'
        ],
        'context_patterns': [
            r'(use (cornstarch|baby powder|(renew|maintenance) powder))',
            r'(powder (it|this|them|after washing))',
            r'(爽身粉|保养粉|玉米粉|滑石粉|去黏粉)'
        ]
    },
    '性价比方案': {
        'keywords': [
            'budget', 'cheap', 'affordable', 'value',
            'best value', 'under $', 'inexpensive',
            '性价比', '便宜', '划算', '平价', '低价'
        ],
        'context_patterns': [
            r'(best (budget|value|cheap|affordable))',
            r'(under \$\d+)',
            r'(great value for money|budget friendly)',
            r'(性价比|便宜|划算|平价|高性价比)'
        ],
        'exclude_patterns': [
            r'(cheap quality|cheaply made|poor quality)',
        ]
    },
    '修复/补救方法': {
        'keywords': [
            'fix', 'repair', 'patch', 'glue', 'restore',
            'how to fix', 'broken but', 'tear repair',
            '修复', '修补', '补救', '粘回去', '坏了怎么修'
        ],
        'context_patterns': [
            r'(fix (it|this|a tear|a hole))',
            r'(repair (it|this|the tear))',
            r'(patch (it|this|a hole))',
            r'(glue (it|this) back)',
            r'(修复|修补|补救|粘回去)'
        ]
    },
    '替代方案/其他选择': {
        'keywords': [
            'instead', 'alternative', 'better off with',
            'try instead', 'other options', 'another choice',
            '替代', '其他选择', '不如买', '换一个', '别的'
        ],
        'context_patterns': [
            r'(instead (of this|of it))',
            r'(better (off with|alternative|option))',
            r'(try (this|that|the) instead)',
            r'(other options|alternatives)',
            r'(替代|其他选择|不如买|换一个)'
        ]
    }
}
