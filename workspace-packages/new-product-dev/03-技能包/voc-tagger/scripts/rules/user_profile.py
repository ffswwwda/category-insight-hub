USER_PROFILE_RULES = {
    '已婚/有伴侣男性': {
        'keywords': [
            'my wife', 'my husband', 'wife and i', 'husband and i',
            'married', 'my partner', 'my girlfriend', 'my boyfriend',
            'my spouse', 'for my wife', 'for my husband',
            '老婆', '老公', '已婚', '伴侣', '我妻子', '我丈夫', '女朋友', '男朋友'
        ],
        'exclude_patterns': [
            r'(gift|present|idea|recommend|for a friend)',
        ],
        'context_patterns': [
            r'(my wife|my husband|married|my partner|my girlfriend|my boyfriend)',
            r'(老婆|老公|已婚|伴侣|我妻子|我丈夫)'
        ]
    },
    '单身男性用户': {
        'keywords': [
            'single', 'alone', 'no girlfriend', 'no wife',
            '单身', '一个人', '没女朋友', '没老婆'
        ],
        'context_patterns': [
            r'(i.?m single|i am single|single guy|single male)',
            r'(我是单身|单身男性|单身狗)'
        ]
    },
    '女性用户': {
        'keywords': [
            'as a woman', 'as a girl', 'female user', 'woman here',
            'girl here', 'my boyfriend', 'my husband bought',
            '女生', '女性', '我是女生', '作为女性'
        ],
        'context_patterns': [
            r'(as a woman|as a girl|female|woman here|girl here)',
            r'(女生|女性|我是女生|作为女性)'
        ]
    },
    '初学者/第一次购买': {
        'keywords': [
            'first time', 'first toy', 'first purchase', 'first one',
            'beginner', 'new to this', 'my first', 'never tried',
            '第一次', '新手', '初学者', '第一次买', '入门'
        ],
        'exclude_patterns': [
            r'(first (time|one) [a-z]+ (great|good|amazing|awesome|love))',
        ]
    },
    '资深用户/收藏家': {
        'keywords': [
            'collector', 'collection', 'dozens', 'many toys',
            'veteran', 'experienced', 'had many', 'owned several',
            '收藏家', '收集', '资深', '老玩家', '几十个', '好几十个'
        ],
        'context_patterns': [
            r'(collect(or|ion)|many toys|experienced|dozens of|veteran)',
            r'(收藏家|收集|资深|老玩家|几十个)'
        ]
    },
    '送礼者': {
        'keywords': [
            'gift for', 'as a gift', 'bought for', 'present for',
            'gave him', 'gave her', 'gift idea', 'for my boyfriend',
            'for my girlfriend', 'for my husband', 'for my wife',
            'for my partner', 'valentine', 'birthday gift',
            '送礼', '礼物', '买给', '送给', '给男朋友', '给女朋友',
            '给老公', '给老婆', '情人节', '生日礼物'
        ],
        'context_patterns': [
            r'(bought (this|it) (for|as a gift)|gift for|as a gift|gave (him|her))',
            r'(买给|送给|礼物|送礼|给.{1,10}(男朋友|女朋友|老公|老婆))'
        ]
    },
    '情侣/夫妻共用': {
        'keywords': [
            'couples', 'couple use', 'for couples', 'partner play',
            'we use', 'my wife and i', 'my husband and i',
            '情侣', '夫妻', '一起用', '共用', '两个人'
        ],
        'context_patterns': [
            r'(couple(s)? (use|play|toy)|we (use|play|enjoy) (this|it|together))',
            r'(情侣|夫妻|一起用|共用)'
        ]
    },
    '其他': {
        'keywords': [],
    }
}
