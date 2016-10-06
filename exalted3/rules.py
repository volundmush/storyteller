from __future__ import unicode_literals
from evennia.utils.ansi import ANSIString

# And finally, the Stats for Exalted 3rd Edition.

STAT_TAGS = (
    {
        'id': 1,
        'key': 'Dot',
    },{
        'id': 2,
        'key': 'Roll',
    },{
        'id': 3,
        'key': 'Favored',
    },{
        'id': 4,
        'key': 'Supernal',
    },{
        'id': 5,
        'key': 'Caste',
    },{
        'id': 6,
        'key': 'Specialty',
    },
)

STAT_DATA = (
    {
        'id': 1,
        'key': 'Attribute',
        'list_order': 1,
        'parent': None,
        'kind': None,
        'start_rating': 1,
        'features_add': (1, 2, 3,)
    },{
        'id': 2,
        'key': 'Physical',
        'list_order': 1,
        'parent': None,
        'kind': None,
        'start_rating': 1,
        'features_add': ()
    },{
        'id': 3,
        'key': 'Social',
        'list_order': 2,
        'parent': None,
        'kind': None,
        'start_rating': 1,
        'features_add': ()
    },{
        'id': 4,
        'key': 'Mental',
        'list_order': 3,
        'parent': None,
        'kind': None,
        'start_rating': 1,
        'features_add': ()
    },{
        'id': 5,
        'key': 'Ability',
        'list_order': 2,
        'parent': None,
        'kind': None,
        'start_rating': 1,
        'features_add': (1, 2, 3, 4, 5, 6)
    },{
        'id': 6,
        'key': 'Advantage',
        'list_order': 3,
        'parent': None,
        'kind': None,
        'start_rating': 1,
        'features_add': (1, 2, )
    },{
        'id': 7,
        'key': 'Style',
        'list_order': 4,
        'parent': None,
        'kind': None,
        'start_rating': 1,
        'features_add': (1, 2)
    },{
        'id': 8,
        'key': 'Specialty',
        'list_order': 4,
        'parent': None,
        'kind': None,
        'start_rating': 1,
        'features_add': (1, 2)
    },

    # Attributes
    {
        'id': 100,
        'key': 'Strength',
        'parent': 1,
        'kind': 2,
        'start_rating': 1,
        'list_order': 1,
    },{
        'id': 101,
        'key': 'Dexterity',
        'parent': 1,
        'kind': 2,
        'start_rating': 1,
        'list_order': 2,
    },{
        'id': 102,
        'key': 'Stamina',
        'parent': 1,
        'kind': 2,
        'start_rating': 1,
        'list_order': 3,
    },{
        'id': 103,
        'key': 'Charisma',
        'parent': 1,
        'kind': 3,
        'start_rating': 1,
        'list_order': 4,
    },{
        'id': 104,
        'key': 'Manipulation',
        'parent': 1,
        'kind': 3,
        'start_rating': 1,
        'list_order': 5,
    },{
        'id': 105,
        'key': 'Appearance',
        'parent': 1,
        'kind': 3,
        'start_rating': 1,
        'list_order': 6,
    },{
        'id': 106,
        'key': 'Perception',
        'parent': 1,
        'kind': 4,
        'start_rating': 1,
        'list_order': 7,
    },{
        'id': 107,
        'key': 'Intelligence',
        'parent': 1,
        'kind': 4,
        'start_rating': 1,
        'list_order': 8,
    },{
        'id': 108,
        'key': 'Wits',
        'parent': 1,
        'kind': 4,
        'start_rating': 1,
        'list_order': 9,
    },

    # Abilities
    {
        'id': 200,
        'key': 'Archery',
        'parent': 5,
        'kind': None,
        'start_rating': 0,
        'list_order': 10,
    },{
        'id': 201,
        'key': 'Brawl',
        'parent': 5,
        'kind': None,
        'start_rating': 0,
        'list_order': 15,
    },{
        'id': 202,
        'key': 'Melee',
        'parent': 5,
        'kind': None,
        'start_rating': 0,
        'list_order': 20,
    },{
        'id': 203,
        'key': 'War',
        'parent': 5,
        'kind': None,
        'start_rating': 0,
        'list_order': 25,
    },{
        'id': 204,
        'key': 'Thrown',
        'parent': 5,
        'kind': None,
        'start_rating': 0,
        'list_order': 30,
    },{
        'id': 205,
        'key': 'Bureaucracy',
        'parent': 5,
        'kind': None,
        'start_rating': 0,
        'list_order': 35,
    },{
        'id': 206,
        'key': 'Linguistics',
        'parent': 5,
        'kind': None,
        'start_rating': 0,
        'list_order': 40,
    },{
        'id': 207,
        'key': 'Ride',
        'parent': 5,
        'kind': None,
        'start_rating': 0,
        'list_order': 45,
    },{
        'id': 208,
        'key': 'Sail',
        'parent': 5,
        'kind': None,
        'start_rating': 0,
        'list_order': 50,
    },{
        'id': 209,
        'key': 'Socialize',
        'parent': 5,
        'kind': None,
        'start_rating': 0,
        'list_order': 55,
    },{
        'id': 210,
        'key': 'Athletics',
        'parent': 5,
        'kind': None,
        'start_rating': 0,
        'list_order': 60,
    },{
        'id': 211,
        'key': 'Awareness',
        'parent': 5,
        'kind': None,
        'start_rating': 0,
        'list_order': 65,
    },{
        'id': 212,
        'key': 'Dodge',
        'parent': 5,
        'kind': None,
        'start_rating': 0,
        'list_order': 70,
    },{
        'id': 213,
        'key': 'Larceny',
        'parent': 5,
        'kind': None,
        'start_rating': 0,
        'list_order': 75,
    },{
        'id': 214,
        'key': 'Stealth',
        'parent': 5,
        'kind': None,
        'start_rating': 0,
        'list_order': 80,
    },{
        'id': 215,
        'key': 'Craft',
        'parent': 5,
        'kind': None,
        'start_rating': 0,
        'list_order': 85,
        'features_remove': (1,)
    },{
        'id': 216,
        'key': 'Investigation',
        'parent': 5,
        'kind': None,
        'start_rating': 0,
        'list_order': 90,
    },{
        'id': 217,
        'key': 'Lore',
        'parent': 5,
        'kind': None,
        'start_rating': 0,
        'list_order': 95,
    },{
        'id': 218,
        'key': 'Medicine',
        'parent': 5,
        'kind': None,
        'start_rating': 0,
        'list_order': 100,
    },{
        'id': 219,
        'key': 'Occult',
        'parent': 5,
        'kind': None,
        'start_rating': 0,
        'list_order': 105,
    },{
        'id': 220,
        'key': 'Integrity',
        'parent': 5,
        'kind': None,
        'start_rating': 0,
        'list_order': 110,
    },{
        'id': 221,
        'key': 'Performance',
        'parent': 5,
        'kind': None,
        'start_rating': 0,
        'list_order': 115,
    },{
        'id': 222,
        'key': 'Presence',
        'parent': 5,
        'kind': None,
        'start_rating': 0,
        'list_order': 120,
    },{
        'id': 223,
        'key': 'Resistance',
        'parent': 5,
        'kind': None,
        'start_rating': 0,
        'list_order': 125,
    },{
        'id': 224,
        'key': 'Survival',
        'parent': 5,
        'kind': None,
        'start_rating': 0,
        'list_order': 130,
    },{
        'id': 225,
        'key': 'Martial Arts',
        'parent': 5,
        'kind': None,
        'start_rating': 0,
        'list_order': 135,
        'features_remove': (1, 2, 3, 5,)
    },

    # Advantages
    {
        'id': 300,
        'key': 'Essence',
        'parent': 6,
        'kind': None,
        'start_rating': 1,
        'list_order': 200,
    },{
        'id': 301,
        'key': 'Willpower',
        'parent': 6,
        'kind': None,
        'start_rating': 5,
        'list_order': 201,
    },

    # Martial Arts Styles
    {
        'id': 400,
        'key': 'Snake',
        'parent': 8,
        'kind': None,
        'start_rating': 0,
        'list_order': 0,
        'features_add': (1, 2),
    },{
        'id': 401,
        'key': 'Tiger',
        'parent': 8,
        'kind': None,
        'start_rating': 0,
        'list_order': 0,
        'features_add': (1, 2),
    },{
        'id': 402,
        'key': 'Single Point Shining into the Void',
        'parent': 8,
        'kind': None,
        'start_rating': 0,
        'list_order': 0,
        'features_add': (1, 2),
    },{
        'id': 403,
        'key': 'White Reaper',
        'parent': 8,
        'kind': None,
        'start_rating': 0,
        'list_order': 0,
        'features_add': (1, 2),
    },{
        'id': 404,
        'key': 'Ebon Shadow',
        'parent': 8,
        'kind': None,
        'start_rating': 0,
        'list_order': 0,
        'features_add': (1, 2),
    },{
        'id': 405,
        'key': 'Crane',
        'parent': 8,
        'kind': None,
        'start_rating': 0,
        'list_order': 0,
        'features_add': (1, 2),
    },{
        'id': 406,
        'key': 'Silver-Voiced Nightingale',
        'parent': 8,
        'kind': None,
        'start_rating': 0,
        'list_order': 0,
        'features_add': (1, 2),
    },{
        'id': 407,
        'key': 'Righteous Devil',
        'parent': 8,
        'kind': None,
        'start_rating': 0,
        'list_order': 0,
        'features_add': (1, 2),
    },{
        'id': 408,
        'key': 'Black Claw',
        'parent': 8,
        'kind': None,
        'start_rating': 0,
        'list_order': 0,
        'features_add': (1, 2),
    },{
        'id': 409,
        'key': 'Steel Devil',
        'parent': 8,
        'kind': None,
        'start_rating': 0,
        'list_order': 0,
        'features_add': (1, 2),
    },

)


MERITS = {
    'merit': {
        'kind': 'merit',
        'category': 'Merit',
    },
    'flaw': {
        'kind': 'flaw',
        'category': 'Flaw',
    },
    'pact': {
        'kind': 'pact',
        'category': 'Pact',
    }
}

POWERS = {
    'solar_charm': {
        'category': 'Solar Charms',
        'kind': 'solar_charm'
    },
    'sorcery_spell': {
        'category': 'Sorcery',
        'kind': 'sorcery_spell'
    },
    'necromancy_spell': {
        'category': 'Necromancy',
        'kind': 'necromancy_spell'
    },
}

POOLS = {
    'personal': {
        'name': 'Personal',
        'kind': 'essence',
        'category': 'Pool',
        'unit': 'Motes of Personal Essence',
        'list_order': 10,
    },
    'peripheral': {
        'name': 'Peripheral',
        'kind': 'essence',
        'category': 'Pool',
        'unit': 'Motes of Peripheral Essence',
        'list_order': 15,
    },
    'willpower': {
        'name': 'Willpower',
        'kind': 'essence',
        'category': 'Pool',
        'unit': 'Points of Temporary Willpower',
        'list_order': 16
    },
    'limit': {
        'name': 'Limit',
        'unit': 'Points of Limit',
        'kind': 'limit',
        'category': 'Track',
        'refresh': 'empty',
        'list_order': 10
    },

}


def universal_willpower(handler):
    return handler.stats_values['willpower']


def solar_personal(handler):
    return handler.stats_values['essence']*3 + 10


def solar_peripheral(handler):
    return handler.stats_values['essence']*7 + 26


def solar_limit(handler):
    return 10


def abyssal_personal(handler):
    return solar_personal(handler)


def abyssal_peripheral(handler):
    return solar_peripheral(handler)


def abyssal_resonance(handler):
    return 10


def terrestrial_personal(handler):
    return handler.stats_values['essence'] + 11


def terrestrial_peripheral(handler):
    return handler.stats_values['essence']*4 + 23


def terrestrial_limit(handler):
    return 10


def lunar_personal(handler):
    return handler.stats_values['essence'] + 15


def lunar_peripheral(handler):
    return handler.stats_values['essence']*4 + 34


def lunar_limit(handler):
    return 10


def sidereal_personal(handler):
    return handler.stats_values['essence']*2 + 9


def sidereal_peripheral(handler):
    return handler.stats_values['essence']*6 + 25


def sidereal_limit(handler):
    return 10


def liminal_personal(handler):
    return handler.stats_values['essence']*3 + 10


def liminal_peripheral(handler):
    return handler.stats_values['essence']*4 + 23


def liminal_limit(handler):
    return 10


CATEGORY = {
    'Solar': (
    {
        'id': 1,
        'key': 'Dawn',
        'caste_stats': (200, 211, 201, 212, 202, 223, 204, 203),
        'list_order': 1
    },{
        'id': 2,
        'key': 'Zenith',
        'caste_stats': (210, 220, 221, 217, 222, 223, 224, 203),
        'list_order': 2
    },{
        'id': 3,
        'key': 'Twilight',
        'caste_stats': (205, 215, 220, 216, 206, 217, 218, 219),
        'list_order': 3
    },{
        'id': 4,
        'key': 'Night',
        'caste_stats': (210, 211, 212, 216, 213, 207, 214, 209),
        'list_order': 4
    },{
        'id': 5,
        'key': 'Eclipse',
        'caste_stats': (205, 213, 206, 219, 222, 207, 208, 209),
        'list_order': 5
    },
    ),
    'Abyssal': (
    {
        'id': 6,
        'key': 'Dusk',
        'caste_stats': (200, 211, 201, 212, 202, 223, 204, 203),
        'list_order': 1
    },{
        'id': 7,
        'key': 'Midnight',
        'caste_stats': (210, 220, 221, 217, 222, 223, 224, 203),
        'list_order': 2
    },{
        'id': 8,
        'key': 'Daybreak',
        'caste_stats': (205, 215, 220, 216, 206, 217, 218, 219),
        'list_order': 3
    },{
        'id': 9,
        'key': 'Day',
        'caste_stats': (210, 211, 212, 216, 213, 207, 214, 209),
        'list_order': 4
    },{
        'id': 10,
        'key': 'Moonshadow',
        'caste_stats': (205, 213, 206, 219, 222, 207, 208, 209),
        'list_order': 5
    },
    )

}


"""
    # Lunar Castes
    {
        'id': 11,
        'key': 'Full Moon',
        'caste_abilities': (100, 101, 102)
    },{
        'id': 12,
        'key': 'Changing Moon',
        'caste_abilities': (103, 104, 105)
    },{
        'id': 13,
        'key': 'No Moon',
        'caste_abilities': (106, 107, 108)
    },

    # First Age Lunar Castes
    {
        'id': 14,
        'key': 'Waxing Moon',
        'caste_abilities': (103, 104, 105)
    },{
        'id': 15,
        'key': 'Waning Moon',
        'caste_abilities': (101, 105, 109)
    },{
        'id': 16,
        'key': 'Half Moon',
        'caste_abilities': (103, 107, 108)
    },

"""


POOL_DATA = {
    'Mortal': {'willpower': universal_willpower},
    'Solar': {'personal': solar_personal, 'peripheral': solar_peripheral, 'willpower': universal_willpower,
                  'limit': solar_limit},
    'Abyssal': {'personal': abyssal_personal, 'peripheral': abyssal_peripheral, 'willpower': universal_willpower,
                  'resonance': abyssal_resonance},
    'Lunar': {'personal': lunar_personal, 'peripheral': lunar_peripheral, 'willpower': universal_willpower,
                  'limit': lunar_limit},
    'Terrestrial': {'personal': terrestrial_personal, 'peripheral': terrestrial_peripheral,
                  'willpower': universal_willpower, 'limit': terrestrial_limit},
    'Sidereal': {'personal': sidereal_personal, 'peripheral': sidereal_peripheral, 'willpower': universal_willpower,
                  'limit': sidereal_limit},
    'Liminal': {'personal': liminal_personal, 'peripheral': liminal_peripheral, 'willpower': universal_willpower,
                  'limit': liminal_limit},

}

TEMPLATES = {
    # Mortal
    1: {'sheet_footer': 'Mortals: The Heroes',
    },

    # Solar
    2: {'sheet_footer': ANSIString('{ySolars: The Lawgivers{n')
    },

    # Abyssal
}


TEMPLATE_DATA = (
    {
        'id': 1,
        'key': 'Mortal',
        'category1_name': 'Profession',
    },{
        'id': 2,
        'key': 'Solar',
        'categories': CATEGORY['Solar'],
        'extra_sheet_colors': {'border': 'Y', 'slash': 'r', 'section_name': 'y'},
        'list_order': 5,
        'category1_name': 'Caste',
    },
)
"""
    {
        'id': 3,
        'key': 'Abyssal',
        'categories': (6, 7, 8, 9, 10),
        'extra_sheet_colors': {'border': 'X', 'slash': 'R', 'section_name': 'r'},
        'list_order': 10,
    },
)

    'abyssal': {
        'name': 'Abyssal',
        'list_order': 10,
        'charm_type': 'abyssal_charm',
        'info_defaults': {'Caste': None},
        'info_choices': {'Caste': ('Dusk', 'Midnight', 'Moonshadow', 'Daybreak', 'Day')},
        'extra_sheet_colors':
        'sheet_column_1': ('Caste',),
        'sheet_column_2': (),
        'sheet_footer': ANSIString('{rAbyssals: The Deathknights{n')
    },
    'lunar': {
        'name': 'Lunar',
        'list_order': 15,
        'pools':
        'charm_type': 'lunar_charm',
        'info_defaults': {'Caste': None},
        'info_choices': {'Caste': ('Full Moon', 'Changing Moon', 'No Moon')},
        'extra_sheet_colors': {'border': '155', 'slash': '125', 'section_name': 'c'},
        'sheet_column_1': ('Caste',),
        'sheet_column_2': (),
        'sheet_footer': ANSIString('{cLunars: The Stewards{n')
    },
    'terrestrial': {
        'name': 'Terrestrial',
        'list_order': 20,
        'charm_type': 'terrestrial_charm',
        'info_defaults': {'Aspect': None},
        'info_choices': {'Aspect': ('Fire', 'Air', 'Water', 'Wood', 'Earth')},
        'extra_sheet_colors': {'border': 'Y', 'slash': 'r', 'section_name': 'y'},
        'sheet_column_1': ('Aspect',),
        'sheet_column_2': (),
        'sheet_footer': ANSIString('{rTerrestrials: The Dragon-Blooded{n')
    },
    'sidereal': {
        'name': 'Sidereal',
        'list_order': 25,
        'charm_type': 'sidereal_charm',
        'info_defaults': {'Caste': None},
        'info_choices': {'Caste': ('Journeys', 'Battles', 'Serenity', 'Secrets', 'Endings')},
        'extra_sheet_colors': {'border': 'Y', 'slash': 'r', 'section_name': 'y'},
        'sheet_column_1': ('Caste',),
        'sheet_column_2': (),
        'sheet_footer': ANSIString('{mSidereals: The Viziers')
    },
    'liminimal': {
        'name': 'Liminal',
        'list_order': 30,
        'pools':
        'charm_type': 'liminal_charm',
        'info_defaults': {'Aspect': None},
        'info_choices': {'Aspect': ('Blood', 'Breath', 'Flesh', 'Marrow', 'Soil')},
        'extra_sheet_colors': {'border': 'Y', 'slash': 'r', 'section_name': 'y'},
        'sheet_column_1': ('Aspect',),
        'sheet_column_2': (),
        'sheet_footer': ANSIString('{wLiminals: The Chernozem')
    },
    'jadeborn': {
        'name': 'Jadeborn',
        'list_order': 30,
        'pools': {'personal': liminal_personal, 'willpower': universal_willpower,
                  'limit': liminal_limit},
        'charm_type': 'liminal_charm',
        'info_defaults': {'Aspect': None},
        'info_choices': {'Aspect': ('Blood', 'Breath', 'Flesh', 'Marrow', 'Soil')},
        'extra_sheet_colors': {'border': 'Y', 'slash': 'r', 'section_name': 'y'},
        'sheet_column_1': ('Aspect',),
        'sheet_column_2': (),
        'sheet_footer': ANSIString('{wJadeborn: The Mountain-Folk')
    },
}

EXPERIENCE = {
    'xp': {
        'name': 'XP',
        'list_order': 1,
    },
    'solar_xp': {
        'name': 'Solar XP',
        'list_order': 2,
    },
    'silver_xp': {
        'name': 'Silver XP',
        'list_order': 20,
    },
    'gold_xp': {
        'name': 'Gold XP',
        'list_order': 30,
    },
    'white_xp': {
        'name': 'White XP',
        'list_order': 40
    }
}
"""