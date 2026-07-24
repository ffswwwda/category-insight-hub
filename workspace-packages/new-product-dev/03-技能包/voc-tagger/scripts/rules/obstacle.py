OBSTACLE_RULES = {
    '尺寸不合适（太大/太小）': {
        'keywords': [
            'too small', 'too big', 'too large', 'size issue',
            'wrong size', 'smaller than', 'bigger than',
            'not the right size', 'size problem', 'tiny',
            'huge', 'enormous', 'oversized', 'undersized',
            '尺寸', '太小', '太大', '大小', '不合适', '迷你', '超大'
        ],
        'context_patterns': [
            r'(too (small|big|large|tiny|huge|enormous))',
            r'(size (issue|problem|wrong|not right))',
            r'(smaller than expected|bigger than expected|not as big as|not as small as)',
            r'(太小|太大|尺寸不对|大小不合适|比想象中)'
        ],
        'exclude_patterns': [
            r'(perfect size|great size|good size|right size|ideal size|just the right size)',
            r'(not too (big|small|large))',
        ]
    },
    '使用体验差/没感觉': {
        'keywords': [
            'no feeling', 'no sensation', 'didn\'t feel',
            'doesn\'t feel good', 'not pleasurable',
            'boring', 'disappointing', 'not worth it',
            'overrated', 'not as expected', 'underwhelming',
            '没感觉', '没快感', '不舒服', '失望', '不好用', '鸡肋'
        ],
        'context_patterns': [
            r'(no (feeling|sensation|pleasure|stimulus))',
            r'(doesn.t feel (good|great|like real|right))',
            r'(not (pleasurable|stimulating|satisfying|worth it))',
            r'(boring|disappointing|overrated|underwhelming)',
            r'(没感觉|没快感|不舒服|失望|不好用|没用)'
        ],
        'exclude_patterns': [
            r'(great feeling|amazing feeling|pleasurable|satisfying|feels great|feels amazing|feels so good)',
        ]
    },
    '太松/没包裹感': {
        'keywords': [
            'loose', 'not tight', 'too loose', 'no suction',
            'no grip', 'no tightness', 'floppy',
            '松', '不紧', '没吸力', '没包裹感', '松垮'
        ],
        'context_patterns': [
            r'(too loose|very loose|so loose)',
            r'(not tight enough|no tightness)',
            r'(no (suction|grip|tightness))',
            r'(太松|不紧|没吸力|没包裹感)'
        ],
        'exclude_patterns': [
            r'(not too loose|perfect tightness|great suction|good grip|nice and tight)',
        ]
    },
    '太紧/疼痛': {
        'keywords': [
            'too tight', 'tight', 'hurts', 'painful',
            'can\'t get in', 'hard to insert', 'difficult to enter',
            'sore', 'pinching', 'chafing',
            '太紧', '痛', '疼', '插不进', '难进', '夹的疼'
        ],
        'context_patterns': [
            r'(too tight|so tight|very tight)',
            r'(hurt(s|ing)?|painful|sore|chafing|pinching)',
            r'(can.t get (in|inside|it in)|hard to insert|difficult to (enter|insert))',
            r'(太紧|太窄|痛|疼|插不进|难进)'
        ],
        'exclude_patterns': [
            r'(nice and tight|perfect tightness|good tight|just tight enough|tight but good)',
        ]
    },
    '材质不真实/像橡胶': {
        'keywords': [
            'feels like rubber', 'rubbery', 'plastic', 'not realistic',
            'cheap material', 'silicone feels', 'not soft',
            'hard material', 'stiff', 'rigid', 'unnatural',
            '像橡胶', '塑料感', '不真实', '材质差', '硬', '不软'
        ],
        'context_patterns': [
            r'(feels like (rubber|plastic))',
            r'(rubbery|plastic-y|cheap material|cheaply made)',
            r'(not (realistic|soft|natural|life like))',
            r'(stiff|rigid|hard (material|texture))',
            r'(像橡胶|塑料感|不真实|材质差|太硬|不软)'
        ],
        'exclude_patterns': [
            r'(realistic feel|lifelike|soft|natural feel|premium material|high quality silicone)',
        ]
    },
    '容易坏/不耐用': {
        'keywords': [
            'broke', 'broken', 'tear', 'torn', 'rip', 'ripped',
            'fell apart', 'disintegrated', 'low quality',
            'not durable', 'didn\'t last', 'fell apart',
            '坏了', '破了', '容易坏', '不耐用', '质量差', '用两次就坏'
        ],
        'context_patterns': [
            r'(broke|broken|tear|torn|rip|ripped)',
            r'(fell apart|disintegrated|came apart)',
            r'(didn.t last|only last|not durable|poor quality)',
            r'(坏了|破了|容易坏|不耐用|质量差|用几次就坏)'
        ],
        'exclude_patterns': [
            r'(still going strong|lasts long|durable|high quality|well made)',
        ]
    },
    '清洁麻烦/不易清洗': {
        'keywords': [
            'hard to clean', 'difficult to clean', 'hard to wash',
            'cleaning issue', 'takes forever to clean',
            'not easy to clean', 'cumbersome to clean',
            '清洁', '难洗', '不好洗', '清洗麻烦', '不容易干'
        ],
        'context_patterns': [
            r'(hard to (clean|wash|dry))',
            r'(difficult to (clean|wash|maintain))',
            r'(cleaning (issue|problem|nightmare))',
            r'(takes (too long|forever) to (clean|dry))',
            r'(难洗|不好洗|清洗麻烦|不容易干|清洁麻烦)'
        ],
        'exclude_patterns': [
            r'(easy to clean|simple to clean|quick clean|easy maintenance|easy to dry)',
        ]
    },
    '重量太重/搬运困难': {
        'keywords': [
            'too heavy', 'heavy', 'hard to carry', 'hard to hold',
            'weight issue', 'too much weight', 'cumbersome',
            'hard to maneuver', 'difficult to handle',
            '太重', '沉', '搬不动', '拿不动', '重量'
        ],
        'context_patterns': [
            r'(too heavy|very heavy|so heavy)',
            r'(hard to (carry|hold|handle|maneuver|lift))',
            r'(weight (issue|problem))',
            r'(cumbersome|bulky)',
            r'(太重|太沉|搬不动|拿不动|重量大)'
        ],
        'exclude_patterns': [
            r'(great weight|nice weight|good weight|hefty but good|weight adds to realism|substantial feel)',
        ]
    },
    '有异味/材质不安全': {
        'keywords': [
            'smell', 'odor', 'scent', 'bad smell', 'chemical smell',
            'stinky', 'smells bad', 'toxic', 'unsafe',
            'allergy', 'allergic', 'irritation', 'rash',
            '味道', '异味', '臭', '化学味', '过敏', '痒', '不安全'
        ],
        'context_patterns': [
            r'(bad (smell|odor|scent)|chemical (smell|odor))',
            r'(smells (bad|terrible|awful|like chemicals))',
            r'(allerg(ic|y)|irritation|rash|unsafe|toxic)',
            r'(有味道|异味|臭|化学味|过敏|痒|不安全)'
        ],
        'exclude_patterns': [
            r'(no smell|no odor|scent free|odorless|unscented|safe|body safe|non toxic)',
        ]
    },
    '内部纹理差/无刺激': {
        'keywords': [
            'no texture', 'smooth inside', 'boring inside',
            'no ribs', 'no bumps', 'inside is smooth',
            'not stimulating', 'no sensation inside',
            '内部', '纹理', '没纹路', '光滑', '没刺激', '内壁'
        ],
        'context_patterns': [
            r'(no (texture|ribs|bumps|ridges|stimulation))',
            r'(smooth (inside|interior))',
            r'(inside is (boring|smooth|flat|unstimulating))',
            r'(not (stimulating|textured))',
            r'(内部|纹理|没纹路|光滑|没刺激|内壁)'
        ],
        'exclude_patterns': [
            r'(great texture|amazing texture|lots of texture|ribbed inside|stimulating)',
        ]
    },
    '噪音大/不私密': {
        'keywords': [
            'noisy', 'loud', 'too loud', 'makes noise',
            'can hear it', 'privacy issue', 'not quiet',
            '噪音', '响', '吵', '不静音', '声音大', '没隐私'
        ],
        'context_patterns': [
            r'(too loud|very loud|so loud|noisy)',
            r'(makes (a lot of|too much) noise)',
            r'(can (hear|hear it) through walls)',
            r'(privacy (issue|problem))',
            r'(噪音|响|吵|不静音|声音大|没隐私)'
        ],
        'exclude_patterns': [
            r'(quiet|silent|no noise|not loud|discreet|privacy)',
        ]
    },
    '价格太贵/不值': {
        'keywords': [
            'too expensive', 'overpriced', 'not worth',
            'waste of money', 'too pricey', 'expensive',
            'not worth the price', 'overpriced',
            '太贵', '不值', '浪费钱', '价格高', '性价比低'
        ],
        'context_patterns': [
            r'(too expensive|too pricey|overpriced)',
            r'(not worth (it|the money|the price))',
            r'(waste of money|waste of cash)',
            r'(太贵|不值|浪费钱|价格高|性价比低)'
        ],
        'exclude_patterns': [
            r'(worth every penny|great value|good price|affordable|worth it|great deal)',
        ]
    }
}
