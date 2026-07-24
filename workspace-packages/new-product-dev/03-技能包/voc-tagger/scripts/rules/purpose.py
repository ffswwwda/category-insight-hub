PURPOSE_RULES = {
    '替代真人/满足性需求': {
        'keywords': [
            'instead of real', 'real woman', 'real person',
            'real girl', 'substitute', 'replacement',
            'sexual release', 'satisfy sexual', 'sexual needs',
            '替代真人', '满足性需求', '代替女朋友', '代替老婆'
        ],
        'context_patterns': [
            r'(instead of (a |real )?(woman|girl|person|partner))',
            r'(substitute for (real )?(sex|woman|girl|partner))',
            r'(for (sexual release|satisfaction|needs|desires))',
            r'(替代真人|满足性需求|代替.{1,5}(女朋友|老婆|真人))'
        ]
    },
    '日常自慰/性发泄': {
        'keywords': [
            'masturbat', 'jack off', 'jerk off', 'self pleasure',
            'daily use', 'regular use', 'every day', 'frequent use',
            '手淫', '自慰', '打飞机', '日常用', '经常用', '每天用'
        ],
        'context_patterns': [
            r'(for (masturbat|self pleasur|jack off|jerk off))',
            r'(use (it |this )?(every day|daily|regularly|frequently))',
            r'(日常自慰|每天用|经常用|打飞机|手淫|自慰)'
        ]
    },
    '伴侣一起使用/前戏': {
        'keywords': [
            'couples', 'couple play', 'partner use', 'with my wife',
            'with my husband', 'with my girlfriend', 'with my boyfriend',
            'foreplay', 'spice up', 'bedroom fun',
            '情侣', '夫妻', '一起用', '前戏', '增加情趣'
        ],
        'context_patterns': [
            r'(couple(s)? (play|use|toy|fun))',
            r'(with (my wife|my husband|my girlfriend|my boyfriend|partner))',
            r'(for (foreplay|spice up|bedroom))',
            r'(情侣|夫妻|一起用|前戏|增加情趣)'
        ],
        'exclude_patterns': [
            r'(a couple of (times|weeks|months|days|minutes|hours))',
        ]
    },
    '收藏/展示爱好': {
        'keywords': [
            'collector', 'collection', 'display', 'showcase',
            'figure', 'statue', 'hobby', 'collecting',
            '收藏', '展示', '爱好', '手办', '收集'
        ],
        'context_patterns': [
            r'(for my (collection|display|showcase))',
            r'(collect(or|ion|ing)|hobby)',
            r'(收藏|展示|爱好|手办|收集)'
        ]
    },
    '陪伴/情感慰藉': {
        'keywords': [
            'companion', 'company', 'not alone', 'less lonely',
            'emotional support', 'comfort', 'cuddle buddy',
            '陪伴', '安慰', '不孤单', '情感', '抱抱'
        ],
        'context_patterns': [
            r'(for (compan(y|ion)|comfort|emotional support|cuddl))',
            r'(feel (less lonely|not alone|better))',
            r'(陪伴|安慰|情感|不孤单)'
        ]
    },
    '缓解压力/放松': {
        'keywords': [
            'stress relief', 'relieve stress', 'relax', 'unwind',
            'after work', 'stress', 'tension relief',
            '减压', '放松', '缓解压力', '下班后'
        ],
        'context_patterns': [
            r'(for (stress relief|relaxation|unwind|tension relief))',
            r'(relieve (stress|tension))',
            r'(减压|放松|缓解压力)'
        ]
    },
    '练习/学习技巧': {
        'keywords': [
            'practice', 'learn', 'training', 'improve', 'skill',
            'technique', 'better at', 'endurance', 'premature',
            '练习', '学习', '训练', '提升', '技巧', '锻炼'
        ],
        'context_patterns': [
            r'(to (practice|learn|train|improve|master))',
            r'(for (practice|training|learning|improvement))',
            r'(练习|学习|训练|提升|技巧)'
        ]
    },
    '其他': {
        'keywords': [],
    }
}
