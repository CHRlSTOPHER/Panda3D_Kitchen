a_scale = 6.06
b_scale = 5.29
c_scale = 4.14
BOSS_HAND = (0.95, 0.75, 0.75, 1.0)
LAW_HAND = (0.75, 0.75, 0.95, 1.0)
CASH_HAND = (0.65, 0.95, 0.85, 1.0)
SELL_HAND = (0.95, 0.75, 0.95, 1.0)
CC_COLOR = (0.25, 0.35, 1.0, 1.0)
AUTO_WALKER_SPEED = 14

PRESIDENT = 'ttr_{}_ene_bossbotClubPresident'
CLERK = 'ttr_{}_ene_lawbotClerk'
AUDITOR = 'ttr_{}_ene_cashbotAuditor'
FOREMAN = 'ttr_{}_ene_sellbotForeman'
CUSTOM_SUIT = {
    'cp': ('A', PRESIDENT.format("t"), PRESIDENT.format("m"),
           BOSS_HAND, None, 4.4/a_scale),
    'lc': ('B', CLERK.format("t"), CLERK.format("m"),
           (0.66, 0.706, 0.74, 1), None, 6.8/b_scale),
    'ma': ('C', AUDITOR.format("t"), AUDITOR.format("m"),
           CASH_HAND, None, 5.7/c_scale),
    'ff': ('B', FOREMAN.format("t"), FOREMAN.format("m"),
           (0.74, 0.62, 0.66, 1), None, 6.0/b_scale)
}

COG_CLOTHING = [
    ["blazer", "torso"],
    ["sleeve", "arms"],
    ["leg", "legs"]
]

HEADS = {
    'nd': 'name-dropper',
    'm': 'mingler',
    'rb': 'robber-baron',
    'bf': 'bottom-feeder',
    'b': 'blood-sucker',
    'dt': 'double-talker',
    'sd': 'spin-doctor',
    'cr': 'corporate-raider'
}
ALL_SEEING_HEADS = ['bigcheese', 'pennypincher']

SUIT_PATH = "phase_3.5/models/char/suit{}-mod"
HEAD_MODEL_PATH = "phase_4/models/char/suit{}-heads.bam"
ANIM_PATH = 'phase_{}/models/char/suit{}-{}.bam'

GLASSES = '**/glasses'
LEFT_EYE = "**/left_eye"
RIGHT_EYE = "**/right_eye"

# suit type, department, head type, hand color, head texture, scale.
SUITS = {
    # sellbots
    'cc': ('C', 's', 'coldcaller', (0.55, 0.65, 1.0, 1.0), None, 3.5/c_scale),
    'tm': ('B', 's', 'telemarketer', SELL_HAND, None, 3.75/b_scale),
    'nd': ('A', 's', 'numbercruncher', SELL_HAND, True, 4.35/a_scale),
    'gh': ('C', 's', 'gladhander', SELL_HAND, None, 4.75/c_scale),
    'ms': ('B', 's', 'movershaker', SELL_HAND, None, 4.75/b_scale),
    'tf': ('A', 's', 'twoface', SELL_HAND, None, 5.25/a_scale),
    'm': ('A', 's', 'twoface', SELL_HAND, True, 5.75/a_scale),
    'mh': ('A', 's', 'yesman', SELL_HAND, None, 7.0/a_scale),

    # cashbots
    'sc': ('C', 'm', 'coldcaller', CASH_HAND, None, 3.6/c_scale),
    'pp': ('A', 'm', 'pennypincher', (1.0, 0.5, 0.6, 1.0), None, 3.55/a_scale),
    'tw': ('C', 'm', 'tightwad', CASH_HAND, None, 4.5/c_scale),
    'bc': ('B', 'm', 'beancounter', CASH_HAND, None, 4.4/b_scale),
    'nc': ('A', 'm', 'numbercruncher', CASH_HAND, None, 5.25/a_scale),
    'mb': ('C', 'm', 'moneybags', CASH_HAND, None, 5.3/c_scale),
    'ls': ('B', 'm', 'loanshark', CASH_HAND, None, 6.5/b_scale),
    'rb': ('A', 'm', 'yesman', CASH_HAND, True, 7.0/a_scale),

    # lawbots
    'bf': ('C', 'l', 'tightwad', LAW_HAND, True, 4.0/c_scale),
    'b': ('B', 'l', 'movershaker', LAW_HAND, True, 4.375/b_scale),
    'dt': ('A', 'l', 'twoface', LAW_HAND, True, 4.25/a_scale),
    'ac': ('B', 'l', 'ambulancechaser', LAW_HAND, None, 4.35/b_scale),
    'bs': ('A', 'l', 'backstabber', LAW_HAND, None, 4.5/a_scale),
    'sd': ('B', 'l', 'telemarketer', LAW_HAND, True, 5.65/b_scale),
    'le': ('A', 'l', 'legaleagle', LAW_HAND, None, 7.125/a_scale),
    'bw': ('A', 'l', 'bigwig', LAW_HAND, None, 7.0/a_scale),

    # bossbots
    'f': ('C', 'c', 'flunky', BOSS_HAND, None, 4.0/c_scale),
    'p': ('B', 'c', 'pencilpusher', BOSS_HAND, None, 3.35/b_scale),
    'ym': ('A', 'c', 'yesman', BOSS_HAND, None, 4.125/a_scale),
    'mm': ('C', 'c', 'micromanager', BOSS_HAND, None, 2.5/c_scale),
    'ds': ('B', 'c', 'beancounter', BOSS_HAND, None, 4.5/b_scale),
    'hh': ('A', 'c', 'headhunter', BOSS_HAND, None, 6.5/a_scale),
    'cr': ('C', 'c', 'flunky', BOSS_HAND, True, 6.75/c_scale),
    'tbc': ('A', 'c', 'bigcheese', (0.75, 0.95, 0.75, 1.0), None, 7.0/a_scale),
}
SUIT_ANIMS = {
    'A': {
        "neutral": 4, "walk": 4,
    },
    'B': {
        "neutral": 4, "walk": 4,
    },
    'C': {
        "neutral": 3.5, "walk": 3.5,
    }
}