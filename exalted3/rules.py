from __future__ import unicode_literals
from evennia.utils.ansi import ANSIString

# And finally, the Stats for Exalted 3rd Edition.

STATS = {
    # attributes!
    'strength': {
        'name': 'Strength',
        'kind': 'attribute',
        'category': 'Physical',
        'list_order': 1,
        'start_rating': 1,
        'features_add': (),
        'features_remove': (),
    },
    'dexterity': {
        'name': 'Dexterity',
        'kind': 'attribute',
        'category': 'Physical',
        'list_order': 2,
        'start_rating': 1,
        'features_add': (),
        'features_remove': (),
    },
    'stamina': {
        'name': 'Stamina',
        'kind': 'attribute',
        'category': 'Physical',
        'list_order': 3,
        'start_rating': 1,
        'features_add': (),
        'features_remove': (),

    },
    'charisma': {
        'name': 'Charisma',
        'kind': 'attribute',
        'category': 'Social',
        'list_order': 4,
        'start_rating': 1,
        'features_add': (),
        'features_remove': (),

    },
    'manipulation': {
        'name': 'Manipulation',
        'kind': 'attribute',
        'category': 'Social',
        'list_order': 5,
        'start_rating': 1,
        'features_add': (),
        'features_remove': (),

    },
    'appearance': {
        'name': 'Appearance',
        'kind': 'attribute',
        'category': 'Social',
        'list_order': 6,
        'start_rating': 1,
        'features_add': (),
        'features_remove': (),

    },
    'perception': {
        'name': 'Perception',
        'kind': 'attribute',
        'category': 'Mental',
        'list_order': 7,
        'start_rating': 1,
        'features_add': (),
        'features_remove': (),

    },
    'intelligence': {
        'name': 'Intelligence',
        'kind': 'attribute',
        'category': 'Mental',
        'list_order': 8,
        'start_rating': 1,
        'features_add': (),
        'features_remove': (),

    },
    'wits': {
        'name': 'Wits',
        'kind': 'attribute',
        'category': 'Mental',
        'list_order': 9,
        'start_rating': 1,
        'features_add': (),
        'features_remove': (),

    },

    #Abilities!
    'archery': {
        'name': 'Archery',
        'kind': 'ability',
        'category': 'Ability',
        'list_order': 10,
        'start_rating': 0,
        'features_add': (),
        'features_remove': (),

    },
    'brawl': {
        'name': 'Brawl',
        'kind': 'ability',
        'category': 'Ability',
        'list_order': 15,
        'start_rating': 0,
        'features_add': (),
        'features_remove': (),

    },
    'melee': {
        'name': 'Melee',
        'kind': 'ability',
        'category': 'Ability',
        'list_order': 20,
        'start_rating': 0,
        'features_add': (),
        'features_remove': (),

    },
    'war': {
        'name': 'War',
        'kind': 'ability',
        'category': 'Ability',
        'list_order': 25,
        'start_rating': 0,
        'features_add': (),
        'features_remove': (),

    },
    'thrown': {
        'name': 'Thrown',
        'kind': 'ability',
        'category': 'Ability',
        'list_order': 30,
        'start_rating': 0,
        'features_add': (),
        'features_remove': (),

    },
    'bureaucracy': {
        'name': 'Bureaucracy',
        'kind': 'ability',
        'category': 'Ability',
        'list_order': 35,
        'start_rating': 0,
        'features_add': (),
        'features_remove': (),

    },
    'linguistics': {
        'name': 'Linguistics',
        'kind': 'ability',
        'category': 'Ability',
        'list_order': 40,
        'start_rating': 0,
        'features_add': (),
        'features_remove': (),

    },
    'ride': {
        'name': 'Ride',
        'kind': 'ability',
        'category': 'Ability',
        'list_order': 45,
        'start_rating': 0,
        'features_add': (),
        'features_remove': (),

    },
    'sail': {
        'name': 'Sail',
        'kind': 'ability',
        'category': 'Ability',
        'list_order': 50,
        'start_rating': 0,
        'features_add': (),
        'features_remove': (),

    },
    'socialize': {
        'name': 'Socialize',
        'kind': 'ability',
        'category': 'Ability',
        'list_order': 55,
        'start_rating': 0,
        'features_add': (),
        'features_remove': (),

    },
    'athletics': {
        'name': 'Athletics',
        'kind': 'ability',
        'category': 'Ability',
        'list_order': 60,
        'start_rating': 0,
        'features_add': (),
        'features_remove': (),

    },
    'awareness': {
        'name': 'Awareness',
        'kind': 'ability',
        'category': 'Ability',
        'list_order': 65,
        'start_rating': 0,
        'features_add': (),
        'features_remove': (),

    },
    'dodge': {
        'name': 'Dodge',
        'kind': 'ability',
        'category': 'Ability',
        'list_order': 70,
        'start_rating': 0,
        'features_add': (),
        'features_remove': (),

    },
    'larceny': {
        'name': 'Larceny',
        'kind': 'ability',
        'category': 'Ability',
        'list_order': 75,
        'start_rating': 0,
        'features_add': (),
        'features_remove': (),

    },
    'stealth': {
        'name': 'Stealth',
        'kind': 'ability',
        'category': 'Ability',
        'list_order': 80,
        'start_rating': 0,
        'features_add': (),
        'features_remove': (),

    },
    'craft': {
        'name': 'Craft',
        'kind': 'ability',
        'category': 'Ability',
        'list_order': 85,
        'start_rating': 0,
        'features_add': (),
        'features_remove': ('dot', 'roll')
    },
    'investigation': {
        'name': 'Investigation',
        'kind': 'ability',
        'category': 'Ability',
        'list_order': 90,
        'start_rating': 0,
        'features_add': (),
        'features_remove': (),

    },
    'lore': {
        'name': 'Lore',
        'kind': 'ability',
        'category': 'Ability',
        'list_order': 95,
        'start_rating': 0,
        'features_add': (),
        'features_remove': (),

    },
    'medicine': {
        'name': 'Medicine',
        'kind': 'ability',
        'category': 'Ability',
        'list_order': 100,
        'start_rating': 0,
        'features_add': (),
        'features_remove': (),

    },
    'occult': {
        'name': 'Occult',
        'kind': 'ability',
        'category': 'Ability',
        'list_order': 105,
        'start_rating': 0,
        'features_add': (),
        'features_remove': (),

    },
    'integrity': {
        'name': 'Integrity',
        'kind': 'ability',
        'category': 'Ability',
        'list_order': 110,
        'start_rating': 0,
        'features_add': (),
        'features_remove': (),

    },
    'performance': {
        'name': 'Performance',
        'kind': 'ability',
        'category': 'Ability',
        'list_order': 115,
        'start_rating': 0,
        'features_add': (),
        'features_remove': (),

    },
    'presence': {
        'name': 'Presence',
        'kind': 'ability',
        'category': 'Ability',
        'list_order': 120,
        'start_rating': 0,
        'features_add': (),
        'features_remove': (),

    },
    'resistance': {
        'name': 'Resistance',
        'kind': 'ability',
        'category': 'Ability',
        'list_order': 125,
        'start_rating': 0,
        'features_add': (),
        'features_remove': (),

    },
    'survival': {
        'name': 'Survival',
        'kind': 'ability',
        'category': 'Ability',
        'list_order': 130,
        'start_rating': 0,
        'features_add': (),
        'features_remove': (),

    },
    'martial_arts': {
        'name': 'Martial Arts',
        'kind': 'ability',
        'category': 'Ability',
        'list_order': 13,
        'start_rating': 0,
        'features_add': (),
        'features_remove': ('dot', 'roll', 'favor', 'caste')
    },

    # Advantages
    'essence': {
        'name': 'Essence',
        'category': 'Advantage',
        'kind': 'advantage',
        'list_order': 5,
        'start_rating': 1,
        'features_add': (),
        'features_remove': ('favor', 'supernal', 'caste', 'special'),
    },
    'willpower': {
        'name': 'Willpower',
        'kind': 'advantage',
        'category': 'Ability',
        'list_order': 5,
        'start_rating': 5,
        'features_add': (),
        'features_remove': ('favor', 'supernal', 'caste', 'special'),
    }

}


CUSTOM = {
    'craft': {
            'kind': 'craft',
            'category': 'Craft',
            'features_default': ('dot', 'roll', 'special')
        },
        'style': {
            'kind': 'style',
            'category': 'Style',
            'features_default': ('dot', 'roll', 'special')
        }
}

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


TEMPLATES = {
    'mortal': {
        'name': 'Mortal',
        'list_order': 0,
        'pools': {'willpower': universal_willpower},
        'charm_type': None,
        'info_defaults': {},
        'info_choices': {},
        'extra_sheet_colors': {},
        'sheet_column_1': (),
        'sheet_column_2': (),
        'sheet_footer': 'Mortals: The Heroes'
    },
    'solar': {
        'name': 'Solar',
        'list_order': 5,
        'pools': {'personal': solar_personal, 'peripheral': solar_peripheral, 'willpower': universal_willpower,
                  'limit': solar_limit},
        'charm_type': 'solar_charm',
        'info_defaults': {'Caste': None},
        'info_choices': {'Caste': ('Dawn', 'Zenith', 'Eclipse', 'Twilight', 'Night')},
        'extra_sheet_colors': {'border': 'Y', 'slash': 'r', 'section_name': 'y'},
        'sheet_column_1': ('Caste',),
        'sheet_column_2': (),
        'sheet_footer': ANSIString('{ySolars: The Lawgivers{n')
    },
    'abyssal': {
        'name': 'Abyssal',
        'list_order': 10,
        'pools': {'personal': abyssal_personal, 'peripheral': abyssal_peripheral, 'willpower': universal_willpower,
                  'resonance': abyssal_resonance},
        'charm_type': 'abyssal_charm',
        'info_defaults': {'Caste': None},
        'info_choices': {'Caste': ('Dusk', 'Midnight', 'Moonshadow', 'Daybreak', 'Day')},
        'extra_sheet_colors': {'border': 'Y', 'slash': 'r', 'section_name': 'y'},
        'sheet_column_1': ('Caste',),
        'sheet_column_2': (),
        'sheet_footer': ANSIString('{rAbyssals: The Deathknights{n')
    },
    'lunar': {
        'name': 'Lunar',
        'list_order': 15,
        'pools': {'personal': lunar_personal, 'peripheral': lunar_peripheral, 'willpower': universal_willpower,
                  'limit': lunar_limit},
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
        'pools': {'personal': terrestrial_personal, 'peripheral': terrestrial_peripheral,
                  'willpower': universal_willpower, 'limit': terrestrial_limit},
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
        'pools': {'personal': sidereal_personal, 'peripheral': sidereal_peripheral, 'willpower': universal_willpower,
                  'limit': sidereal_limit},
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
        'pools': {'personal': liminal_personal, 'peripheral': liminal_peripheral, 'willpower': universal_willpower,
                  'limit': liminal_limit},
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

EX3_RULES = {
    'stats': STATS,
    'powers': POWERS,
    'merits': MERITS,
    'custom': CUSTOM,
    'pools': POOLS,
    'templates': TEMPLATES,
    'experience': EXPERIENCE
}
