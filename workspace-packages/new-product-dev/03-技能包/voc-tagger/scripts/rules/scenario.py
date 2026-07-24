SCENARIO_RULES = {
    '独处时/家中': {
        'keywords': [
            'alone', 'by myself', 'home alone', 'at home',
            'in my room', 'my place', 'private time',
            '一个人', '在家', '独处', '私人时间', '自己一个人'
        ],
        'context_patterns': [
            r'(when (i.?m |i am )?(alone|by myself|home alone))',
            r'(at (home|my place|my apartment|my room))',
            r'(private time|me time)',
            r'(一个人|在家|独处|私人时间)'
        ]
    },
    '卧室/床上使用': {
        'keywords': [
            'in bed', 'bedroom', 'on the bed', 'bed time',
            'before bed', 'nightstand', 'under pillow',
            '床上', '卧室', '睡觉前', '床头', '枕边'
        ],
        'context_patterns': [
            r'(in (the |my )?bed)',
            r'(in (the |my )?bedroom)',
            r'(before (bed|sleep))',
            r'(bed(time|side|stand))',
            r'(床上|卧室|睡觉前|床头)'
        ],
        'exclude_patterns': [
            r'(keep (it )?in bed (for storage|stored|to store))',
            r'(store (it )?in the bedroom)',
        ]
    },
    '夜晚使用': {
        'keywords': [
            'at night', 'night time', 'evening', 'late night',
            'before sleep', 'bedtime', 'overnight',
            '晚上', '夜里', '深夜', '睡前', '夜晚'
        ],
        'context_patterns': [
            r'(at night|night time|late night|overnight)',
            r'(in the evening)',
            r'(before (bed|sleep|going to bed))',
            r'(晚上|夜里|深夜|睡前|夜晚)'
        ]
    },
    '浴室/洗澡时': {
        'keywords': [
            'shower', 'bath', 'bathtub', 'in the shower',
            'while bathing', 'wet use', 'waterproof',
            '浴室', '洗澡', '淋浴', '泡澡', '防水'
        ],
        'context_patterns': [
            r'(in the (shower|bath|bathtub))',
            r'(while (bathing|showering))',
            r'(shower use|bath time|wet use)',
            r'(浴室|洗澡|淋浴|泡澡)'
        ],
        'exclude_patterns': [
            r'(wash (it )?in (the )?shower)',
            r'(clean (it )?in (the )?bath)',
            r'(防水设计|easy to clean)',
        ]
    },
    '释放压力时': {
        'keywords': [
            'stress', 'stressed', 'after work', 'long day',
            'tired', 'frustrated', 'need release', 'tension',
            '压力大', '下班后', '累了', '压力', '疲惫'
        ],
        'context_patterns': [
            r'(after (work|a long day|a hard day))',
            r'(when (stressed|tired|frustrated|tense))',
            r'(to (relieve|release|reduce) (stress|tension))',
            r'(下班后|压力大|累了|压力|疲惫)'
        ]
    },
    '伴侣前戏/互动': {
        'keywords': [
            'with partner', 'with my wife', 'with my husband',
            'foreplay', 'couples play', 'in bed with',
            'intimacy', 'during sex', 'spice up',
            '和伴侣', '和老婆', '和老公', '前戏', '亲热'
        ],
        'context_patterns': [
            r'(with (my wife|my husband|my girlfriend|my boyfriend|partner))',
            r'(during (foreplay|sex|intimacy))',
            r'(couple(s)? (play|fun|time))',
            r'(spice up (our sex life|things))',
            r'(和.{1,5}(老婆|老公|伴侣|对象)|前戏|亲热)'
        ],
        'exclude_patterns': [
            r'(a couple of (times|weeks|months|days|minutes|hours))',
        ]
    },
    '出差/旅行携带': {
        'keywords': [
            'travel', 'business trip', 'on the road', 'portable',
            'easy to carry', 'travel size', 'vacation', 'holiday',
            '出差', '旅行', '旅游', '便携', '假期'
        ],
        'context_patterns': [
            r'(for (travel|business trip|vacation|trips))',
            r'(when (traveling|on a trip|on the road))',
            r'(easy to (carry|transport|take with you))',
            r'(出差|旅行|旅游|便携|假期)'
        ]
    },
    '单身独居': {
        'keywords': [
            'live alone', 'single', 'live by myself', 'solo',
            'apartment alone', 'my own place',
            '单身', '独居', '一个人住', '自己住'
        ],
        'context_patterns': [
            r'(live (alone|by myself))',
            r'(single and living alone)',
            r'(in my (own )?(apartment|place) alone)',
            r'(单身|独居|一个人住|自己住)'
        ]
    },
    '办公室/工作间隙': {
        'keywords': [
            'office', 'at work', 'work from home', 'break time',
            'during work', 'desk', 'work break',
            '办公室', '上班', '工作时', '摸鱼', '休息时间'
        ],
        'context_patterns': [
            r'(at the office|at work|during work hours)',
            r'(on (my )?break|break time|lunch break)',
            r'(work from home|wfh)',
            r'(办公室|上班|工作时|摸鱼)'
        ],
        'exclude_patterns': [
            r'(it works (great|well|good|fine))',
            r'(work from home 指在家办公)',
        ]
    }
}
