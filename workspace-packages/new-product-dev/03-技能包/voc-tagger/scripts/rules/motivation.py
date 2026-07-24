MOTIVATION_RULES = {
    '追求真实感/模拟真人': {
        'keywords': [
            'realistic', 'feels real', 'like real', 'lifelike',
            'real feel', 'authentic', 'realistic feel',
            'realistic texture', 'just like real',
            '真实感', '逼真', '像真的', '真人', '真实', '仿真'
        ],
        'context_patterns': [
            r'(i (bought|got|chose|wanted|needed) .{0,30}(realistic|real feel|lifelike|authentic))',
            r'(because .{0,20}(realistic|real feel|lifelike|authentic))',
            r'(look(ing)? for .{0,20}(realistic|real|lifelike))',
            r'(买.{0,10}因为.{0,20}(真实|逼真|真人|仿真))',
            r'(为了.{0,20}(真实|逼真|真人|仿真))',
            r'(追求.{0,10}(真实|逼真))'
        ],
        'exclude_patterns': [
            r'(this (product|toy|doll) is (very|quite|super|so) realistic)',
            r'(it feels real\.)\s*(great|amazing|love|awesome|best)',
        ]
    },
    '性需求满足/发泄': {
        'keywords': [
            'masturbat', 'jack off', 'jerk off', 'cum',
            'sexual need', 'sex drive', 'horny', 'release',
            'satisfy', 'pleasure myself', 'self pleasure',
            '手淫', '自慰', '打飞机', '发泄', '生理需求', '性需求'
        ],
        'context_patterns': [
            r'(i (use|bought|need|want) .{0,30}(masturbat|jack off|jerk off|release|pleasure))',
            r'(for (masturbat|release|pleasure|self pleasur))',
            r'(to (masturbat|jerk off|cum|release|satisfy))',
            r'(用来.{0,10}(手淫|自慰|发泄|解决))',
            r'(为了.{0,10}(发泄|生理需求|性需求))'
        ]
    },
    '好奇/尝鲜体验': {
        'keywords': [
            'curious', 'curiosity', 'try out', 'give it a try',
            'wanted to try', 'first time', 'never tried',
            'wonder', 'what it like', 'how it feels',
            '好奇', '试试', '尝鲜', '第一次', '想试试', '玩玩'
        ],
        'context_patterns': [
            r'(curious (about|to try))',
            r'(wanted to (try|see|experience))',
            r'(out of curiosity)',
            r'(give it a try|just to try)',
            r'(好奇|想试试|出于好奇|尝鲜)'
        ]
    },
    '送礼': {
        'keywords': [
            'gift for', 'as a gift', 'birthday gift', 'valentine gift',
            'christmas gift', 'bought for him', 'bought for her',
            'present for', 'surprise for',
            '送礼', '礼物', '买给', '送给', '生日礼物', '情人节礼物'
        ],
        'context_patterns': [
            r'(bought (this|it) (for|as a gift))',
            r'(gift (for|idea|for him|for her))',
            r'(present for)',
            r'(买给.{1,10}|送给.{1,10}|礼物|送礼)'
        ],
        'exclude_patterns': [
            r'(makes a great gift|would make a good gift|gift idea)',
        ]
    },
    '新鲜感/刺激感': {
        'keywords': [
            'new experience', 'something new', 'spice things up',
            'variety', 'change', 'different', 'novelty',
            'exciting', 'thrill', 'adventure',
            '新鲜', '刺激', '新鲜感', '换换口味', '新体验'
        ],
        'context_patterns': [
            r'(something new|new experience|spice things up)',
            r'(for (variety|change|novelty|excitement))',
            r'(新鲜|刺激|新鲜感|换换口味|新体验)'
        ]
    },
    '陪伴/情感需求': {
        'keywords': [
            'lonely', 'companion', 'company', 'comfort',
            'not alone', 'feel less lonely', 'emotional',
            'cuddle', 'hug', 'love doll',
            '孤独', '寂寞', '陪伴', '安慰', '情感', '抱抱'
        ],
        'context_patterns': [
            r'(feel (lonely|alone|isolated))',
            r'(for (compan(y|ion)|comfort|emotional support))',
            r'(lonel(iness|y))',
            r'(孤独|寂寞|陪伴|安慰)'
        ]
    },
    '收藏/爱好': {
        'keywords': [
            'collector', 'collection', 'collecting', 'hobby',
            'display', 'showcase', 'figure collection',
            '收藏', '收集', '爱好', '展示', '手办'
        ],
        'context_patterns': [
            r'(collect(or|ion|ing))',
            r'(for my (collection|display))',
            r'(收藏|收集|爱好|展示)'
        ]
    },
    '特定审美/偏好': {
        'keywords': [
            'anime', 'hentai', 'cosplay', 'fantasy',
            'character', 'specific look', 'big butt',
            'big boobs', 'thighs', 'legs', 'ass',
            '动漫', '二次元', 'cos', '角色', '审美'
        ],
        'context_patterns': [
            r'(i (like|love|prefer|want) .{0,30}(anime|hentai|cosplay|fantasy|big butt|big boobs|thighs))',
            r'(for the (anime|hentai|cosplay|character|fantasy))',
            r'(动漫|二次元|cos|角色)'
        ]
    },
    '性价比/价格因素': {
        'keywords': [
            'cheap', 'affordable', 'budget', 'value for money',
            'good price', 'great value', 'inexpensive',
            '性价比', '便宜', '划算', '实惠', '不贵'
        ],
        'context_patterns': [
            r'(good (price|value|deal|budget))',
            r'(affordable|inexpensive|cheap)',
            r'(value for money|great value)',
            r'(性价比|便宜|划算|实惠)'
        ]
    },
    '替代真人/远距离关系': {
        'keywords': [
            'long distance', 'far away', 'girlfriend away',
            'wife away', 'partner away', 'when she not around',
            '异地', '远距离', '女朋友不在', '老婆不在'
        ],
        'context_patterns': [
            r'(long (distance|distance relationship))',
            r'(when .{0,10}(girlfriend|wife|partner) .{0,10}(away|not here|out of town))',
            r'(异地|远距离|女朋友不在|老婆不在)'
        ]
    },
    '单身/无伴侣': {
        'keywords': [
            'single', 'no girlfriend', 'no wife', 'no partner',
            'alone', 'without a partner', '单身', '没女朋友', '没老婆'
        ],
        'context_patterns': [
            r'(single|no girlfriend|no wife|no partner)',
            r'(because (i.?m single|no girlfriend))',
            r'(单身|没女朋友|没老婆)'
        ]
    },
    '其他': {
        'keywords': [],
    }
}
