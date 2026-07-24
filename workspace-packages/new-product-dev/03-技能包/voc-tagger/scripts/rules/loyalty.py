LOYALTY_RULES = {
    '高忠诚（5星+好评）': {
        'keywords': [
            '5 star', 'five star', '5 stars', '★★★★★',
            'love it', 'amazing', 'best ever', 'highly recommend',
            'would buy again', 'repurchase', 'buy another',
            'worth every penny', 'best purchase',
            '5星', '五星', '好评', '强烈推荐', '还会买', '回购', '物超所值'
        ],
        'context_patterns': [
            r'(5\s*star|five star|5/5|10/10|★★★★★)',
            r'(love (it|this|that))',
            r'(highly recommend|would (definitely|certainly) (buy|purchase|get) again)',
            r'(best (ever|purchase|toy|doll|one|thing i.ve bought))',
            r'(worth every (penny|cent|dollar))',
            r'(5星|五星|好评|强烈推荐|回购|还会买)'
        ]
    },
    '中忠诚（3-4星+中评）': {
        'keywords': [
            '4 star', 'four star', '3 star', 'three star',
            'decent', 'okay', 'not bad', 'pretty good',
            'not great but', 'mixed feelings',
            '4星', '四星', '3星', '三星', '还行', '一般', '还可以', '中规中矩'
        ],
        'context_patterns': [
            r'((4|3)\s*star|four star|three star|4/5|3/5|★★★★☆|★★★☆☆)',
            r'(decent|okay|not bad|pretty good|alright)',
            r'(it.s (okay|fine|alright|decent) but)',
            r'(mixed feelings|not (great|bad))',
            r'(还行|一般|还可以|中规中矩|马马虎虎)'
        ],
        'exclude_patterns': [
            r'(5 star|five star|love it|amazing|best ever|highly recommend)',
        ]
    },
    '低忠诚（1-2星+差评）': {
        'keywords': [
            '1 star', '2 star', 'one star', 'two star',
            'worst', 'terrible', 'awful', 'waste of money',
            'regret', 'disappointing', 'not worth',
            '1星', '2星', '一星', '二星', '差评', '后悔', '太差', '不值', '浪费钱'
        ],
        'context_patterns': [
            r'((1|2)\s*star|one star|two star|1/5|2/5|★☆☆☆☆|★★☆☆☆)',
            r'(worst (ever|purchase|thing))',
            r'(terrible|awful|horrible)',
            r'(waste of (money|time|money))',
            r'(regret (buying|getting|it|this))',
            r'(1星|2星|一星|二星|差评|后悔|太差|不值|浪费钱)'
        ]
    },
    '会推荐给他人': {
        'keywords': [
            'recommend', 'would recommend', 'highly recommend',
            'suggest', 'give it a try', 'check this out',
            '推荐', '建议买', '可以试试', '安利', '值得入手'
        ],
        'context_patterns': [
            r'(would (definitely|highly|certainly|surely) )?recommend',
            r'(i (suggest|recommend))',
            r'(give it a try|worth checking out)',
            r'(推荐|建议买|可以试试|安利|值得入手)'
        ],
        'exclude_patterns': [
            r'(would not recommend|don.t recommend|not recommended|cannot recommend)',
        ]
    },
    '价格敏感/犹豫': {
        'keywords': [
            'expensive', 'overpriced', 'too much',
            'not worth the price', 'pricy',
            'not sure if worth', 'hesitate', 'on the fence',
            '贵', '不值这个价', '犹豫', '纠结', '性价比不高'
        ],
        'context_patterns': [
            r'(too expensive|overpriced|too pricey)',
            r'(not worth (the price|the money))',
            r'(on the fence|hesitat(e|ing))',
            r'(not sure if (worth|it.s worth it))',
            r'(贵|不值这个价|犹豫|纠结|性价比不高)'
        ],
        'exclude_patterns': [
            r'(worth every penny|great value|affordable|worth it)',
        ]
    }
}
