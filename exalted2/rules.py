from __future__ import unicode_literals

STATS = {
    # attributes!
    'strength': {
        'name': 'Strength',
        'type': 'Attribute',
        'category': 'Physical',
        'list_order': 1,
        'tags': ('favor', 'caste', 'dots', 'roll', 'specialize'),
        'start_value': 1
    },
    'dexterity': {
        'name': 'Dexterity',
        'type': 'Attribute',
        'category': 'Physical',
        'list_order': 2,
        'tags': ('favor', 'caste', 'dots', 'roll', 'specialize'),
        'start_value': 1
    },
    'stamina': {
        'name': 'Stamina',
        'type': 'Attribute',
        'category': 'Physical',
        'list_order': 3,
        'tags': ('favor', 'caste', 'dots', 'roll', 'specialize'),
        'start_value': 1
    },
    'charisma': {
        'name': 'Charisma',
        'type': 'Attribute',
        'category': 'Social',
        'list_order': 4,
        'tags': ('favor', 'caste', 'dots', 'roll', 'specialize'),
        'start_value': 1
    },
    'manipulation': {
        'name': 'Manipulation',
        'type': 'Attribute',
        'category': 'Social',
        'list_order': 5,
        'tags': ('favor', 'caste', 'dots', 'roll', 'specialize'),
        'start_value': 1
    },
    'appearance': {
        'name': 'Appearance',
        'type': 'Attribute',
        'category': 'Social',
        'list_order': 6,
        'tags': ('favor', 'caste', 'dots', 'roll', 'specialize'),
        'start_value': 1
    },
    'perception': {
        'name': 'Perception',
        'type': 'Attribute',
        'category': 'Mental',
        'list_order': 7,
        'tags': ('favor', 'caste', 'dots', 'roll', 'specialize'),
        'start_value': 1
    },
    'intelligence': {
        'name': 'Intelligence',
        'type': 'Attribute',
        'category': 'Mental',
        'list_order': 8,
        'tags': ('favor', 'caste', 'dots', 'roll', 'specialize'),
        'start_value': 1
    },
    'wits': {
        'name': 'Wits',
        'type': 'Attribute',
        'category': 'Mental',
        'list_order': 9,
        'tags': ('favor', 'caste', 'dots', 'roll', 'specialize'),
        'start_value': 1
    },

    #Abilities!
    'archery': {
        'name': 'Archery',
        'type': 'Ability',
        'tags': ('favor', 'caste', 'dots', 'roll', 'specialize'),
        'list_order': 10,
    },
    'martial_arts': {
        'name': 'Martial Arts',
        'type': 'Ability',
        'tags': ('favor', 'caste', 'dots', 'roll', 'specialize'),
        'list_order': 15,
    },
    'melee': {
        'name': 'Melee',
        'type': 'Ability',
        'tags': ('favor', 'caste', 'dots', 'roll', 'specialize'),
        'list_order': 20,
    },
    'war': {
        'name': 'War',
        'type': 'Ability',
        'tags': ('favor', 'caste', 'dots', 'roll', 'specialize'),
        'list_order': 25,
    },
    'thrown': {
        'name': 'Thrown',
        'type': 'Ability',
        'tags': ('favor', 'caste', 'dots', 'roll', 'specialize'),
        'list_order': 30,
    },
    'bureaucracy': {
        'name': 'Bureaucracy',
        'type': 'Ability',
        'tags': ('favor', 'caste', 'dots', 'roll', 'specialize'),
        'list_order': 35,
    },
    'linguistics': {
        'name': 'Linguistics',
        'type': 'Ability',
        'tags': ('favor', 'caste', 'dots', 'roll', 'specialize'),
        'list_order': 40,
    },
    'ride': {
        'name': 'Ride',
        'type': 'Ability',
        'tags': ('favor', 'caste', 'dots', 'roll', 'specialize'),
        'list_order': 45,
    },
    'sail': {
        'name': 'Sail',
        'type': 'Ability',
        'tags': ('favor', 'caste', 'dots', 'roll', 'specialize'),
        'list_order': 50,
    },
    'socialize': {
        'name': 'Socialize',
        'type': 'Ability',
        'tags': ('favor', 'caste', 'dots', 'roll', 'specialize'),
        'list_order': 55,

    },
    'athletics': {
        'name': 'Athletics',
        'type': 'Ability',
        'tags': ('favor', 'caste', 'dots', 'roll', 'specialize'),
        'list_order': 60,
    },
    'awareness': {
        'name': 'Awareness',
        'type': 'Ability',
        'tags': ('favor', 'caste', 'dots', 'roll', 'specialize'),
        'list_order': 65,
    },
    'dodge': {
        'name': 'Dodge',
        'type': 'Ability',
        'tags': ('favor', 'caste', 'dots', 'roll', 'specialize'),
        'list_order': 70,
    },
    'larceny': {
        'name': 'Larceny',
        'type': 'Ability',
        'tags': ('favor', 'caste', 'dots', 'roll', 'specialize'),
        'list_order': 75,
    },
    'stealth': {
        'name': 'Stealth',
        'type': 'Ability',
        'tags': ('favor', 'caste', 'dots', 'roll', 'specialize'),
        'list_order': 80,
    },
    'craft': {
        'name': 'Craft',
        'type': 'Ability',
        'tags': ('favor', 'caste'),
        'list_order': 85,
    },
    'investigation': {
        'name': 'Investigation',
        'type': 'Ability',
        'tags': ('favor', 'caste', 'dots', 'roll', 'specialize'),
        'list_order': 90,
    },
    'lore': {
        'name': 'Lore',
        'type': 'Ability',
        'tags': ('favor', 'caste', 'dots', 'roll', 'specialize'),
        'list_order': 95,
    },
    'medicine': {
        'name': 'Medicine',
        'type': 'Ability',
        'tags': ('favor', 'caste', 'dots', 'roll', 'specialize'),
        'list_order': 100,
    },
    'occult': {
        'name': 'Occult',
        'type': 'Ability',
        'tags': ('favor', 'caste', 'dots', 'roll', 'specialize'),
        'list_order': 105,
    },
    'integrity': {
        'name': 'Integrity',
        'type': 'Ability',
        'tags': ('favor', 'caste', 'dots', 'roll', 'specialize'),
        'list_order': 110,
    },
    'performance': {
        'name': 'Performance',
        'type': 'Ability',
        'tags': ('favor', 'caste', 'dots', 'roll', 'specialize'),
        'list_order': 115,
    },
    'presence': {
        'name': 'Presence',
        'type': 'Ability',
        'tags': ('favor', 'caste', 'dots', 'roll', 'specialize'),
        'list_order': 120,
    },
    'resistance': {
        'name': 'Resistance',
        'type': 'Ability',
        'tags': ('favor', 'caste', 'dots', 'roll', 'specialize'),
        'list_order': 125,
    },
    'survival': {
        'name': 'Survival',
        'type': 'Ability',
        'tags': ('favor', 'caste', 'dots', 'roll', 'specialize'),
        'list_order': 130,
    },

    # Advantages
    'essence': {
        'name': 'Essence',
        'type': 'Advantage',
        'tags': ('dots', 'roll'),
        'start_value': 1,
    },
    'willpower': {
        'name': 'Willpower',
        'type': 'Advantage',
        'tags': ('dots', 'roll'),
        'start_value': 1,
    },

    # Virtues
    'conviction': {
        'name': 'Conviction',
        'type': 'Virtue',
        'list_order': 10,
        'tags': ('dots', 'roll'),
        'start_value': 1,
    },
    'compassion': {
        'name': 'Compassion',
        'type': 'Virtue',
        'list_order': 15,
        'tags': ('dots', 'roll'),
        'start_value': 1,
    },
    'valor': {
        'name': 'Valor',
        'type': 'Virtue',
        'list_order': 20,
        'tags': ('dots', 'roll'),
        'start_value': 1,
    },
    'temperance': {
        'name': 'Temperance',
        'type': 'Virtue',
        'list_order': 25,
        'tags': ('dots', 'roll'),
        'start_value': 1,
    },

    # Graces!
    'heart': {
        'name': 'Heart',
        'type': 'Grace',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'cup': {
        'name': 'Cup',
        'type': 'Grace',
        'tags': ('dots', 'roll'),
        'list_order': 5,
    },
    'sword': {
        'name': 'sword',
        'type': 'Grace',
        'tags': ('dots', 'roll'),
        'list_order': 10,
    },
    'staff': {
        'name': 'staff',
        'type': 'Grace',
        'tags': ('dots', 'roll'),
        'list_order': 15,
    },
    'ring': {
        'name': 'ring',
        'type': 'Grace',
        'tags': ('dots', 'roll'),
        'list_order': 20,
    },
    'way': {
        'name': 'way',
        'type': 'Grace',
        'tags': ('dots', 'roll'),
        'list_order': 25,
    },

    # Colleges
    'the_corpse': {
        'name': 'The Corpse',
        'type': 'College',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'the_crow': {
        'name': 'The Crow',
        'type': 'College',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'the_haywain': {
        'name': 'The Haywain',
        'type': 'College',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'the_rising_smoke': {
        'name': 'The Rising Smoke',
        'type': 'College',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'the_sword': {
        'name': 'The Sword',
        'type': 'College',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'the_captain': {
        'name': 'The Captain',
        'type': 'College',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'the_gull': {
        'name': 'The Gull',
        'type': 'College',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'the_mast': {
        'name': 'The Mast',
        'type': 'College',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'the_messenger': {
        'name': 'The Messenger',
        'type': 'College',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'the_ships_wheel': {
        'name': "The Ship's Wheel",
        'type': 'College',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'the_ewer': {
        'name': 'The Ewer',
        'type': 'College',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'the_lovers': {
        'name': 'The Lovers',
        'type': 'College',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'the_musician': {
        'name': 'The Musician',
        'type': 'College',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'the_peacock': {
        'name': 'The Peacock',
        'type': 'College',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'the_pillar': {
        'name': 'The Pillar',
        'type': 'College',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'the_guardians': {
        'name': 'The Guardians',
        'type': 'College',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'the_key': {
        'name': 'The Key',
        'type': 'College',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'the_mask': {
        'name': 'The Mask',
        'type': 'College',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'the_sorcerer': {
        'name': 'The Sorcerer',
        'type': 'College',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'the_treasure_trove': {
        'name': 'The Treasure Trove',
        'type': 'College',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'the_banner': {
        'name': 'The Banner',
        'type': 'College',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'the_gauntlet': {
        'name': 'The Gauntlet',
        'type': 'College',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'the_quiver': {
        'name': 'The Quiver',
        'type': 'College',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'the_shield': {
        'name': 'The Shield',
        'type': 'College',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'the_spear': {
        'name': 'The Spear',
        'type': 'College',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'the_comet': {
        'name': 'The Comet',
        'type': 'College',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'the_lightning_bolt': {
        'name': 'The Lightning Bolt',
        'type': 'College',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },

    # Paths
    'celestial_air': {
        'name': 'Celestial Air',
        'type': 'Path',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'clear_air': {
        'name': 'Clear Air',
        'type': 'Path',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'solid_earth': {
        'name': 'Solid Earth',
        'type': 'Path',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'yielding_earth': {
        'name': 'Yielding Earth',
        'type': 'Path',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'blazing_fire': {
        'name': 'Blazing Fire',
        'type': 'Path',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'flickering_fire': {
        'name': 'Flickering Fire',
        'type': 'Path',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'flowing_water': {
        'name': 'Flowing Water',
        'type': 'Path',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'shimmering_water': {
        'name': 'Shimmering Water',
        'type': 'Path',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'growing_wood': {
        'name': 'Growing Wood',
        'type': 'Path',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'shaping_wood': {
        'name': 'Shaping Wood',
        'type': 'Path',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'glorious_consumption': {
        'name': 'Glorious Consumption',
        'type': 'Path',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'coagulated_eucharist': {
        'name': 'Coagulated Eucharist',
        'type': 'Path',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'technomorphic_transcendance': {
        'name': 'Technomorphic Transcendance',
        'type': 'Path',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'ecstatic_armageddon': {
        'name': 'Ecstatic Armageddon',
        'type': 'Path',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },
    'tormented_bodhisattva': {
        'name': 'Tormented Bodhisattva',
        'type': 'Path',
        'tags': ('dots', 'roll'),
        'list_order': 1,
    },

    # Slots
    'general_slot': {
        'name': 'General',
        'type': 'Slot',
        'tags': ('dots', ),
        'list_order': 1,
    },
    'dedicated_slot': {
        'name': 'Dedicated',
        'type': 'Slot',
        'tags': ('dots', ),
        'list_order': 2,
    },


}


def personal_check(character):
    pass


def gossamer_check(character):
    pass


def dissonance_check(character):
    pass


POOLS = {
    'personal': {
        'name': 'Personal',
        'list_order': 0,
        'unit': 'Motes of Personal Essence',
        'tags': ('gain', 'spend', 'refresh', 'commit', 'universal'),
        'refresh': 'max',
        'check': personal_check,
    },
    'peripheral': {
        'name': 'Peripheral',
        'list_order': 5,
        'unit': 'Motes of Peripheral Essence',
        'tags': ('gain', 'spend', 'refresh', 'commit'),
        'refresh': 'max'
    },
    'willpower': {
        'name': 'Willpower',
        'list_order': 9,
        'unit': 'Temporary Willpower',
        'tags': ('gain', 'spend', 'refresh', 'commit'),
        'refresh': 'max'
    },
    'limit': {
        'name': 'Limit',
        'unit': 'Points of Limit',
        'tags': ('gain', 'spend', 'refresh', 'commit', 'universal'),
        'refresh': 'empty'
    },
    'expanded': {
        'name': 'Expanded',
        'list_order': 6,
        'unit': 'Motes of Expanded Peripheral Essence',
        'tags': ('gain', 'spend', 'refresh', 'commit'),
        'refresh': 'max'
    },
    'overdrive': {
        'name': 'Overdrive',
        'list_order': 7,
        'unit': 'Motes of Overdrive Peripheral Essence',
        'tags': ('gain', 'spend', 'refresh', ),
        'refresh': 'empty'
    },
    'paradox': {
        'name': 'Paradox',
        'unit': 'Points of Paradox',
        'tags': ('gain', 'spend', 'refresh', 'commit'),
        'refresh': 'empty'
    },
    'clarity': {
        'name': 'Clarity',
        'unit': 'Points of Clarity',
        'tags': ('gain', 'spend', 'refresh', 'commit'),
        'refresh': 'empty'
    },
    'divergence': {
        'name': 'Divergence',
        'unit': 'Points of Divergence',
        'tags': ('gain', 'spend', 'refresh', 'commit'),
        'refresh': 'empty'
    },
    'dissonance': {
        'name': 'Dissonance',
        'unit': 'Points of Dissonance',
        'tags': ('gain', 'spend', 'refresh', 'commit', 'universal'),
        'refresh': 'empty',
        'check': dissonance_check
    },
    'stasis': {
        'name': 'Stasis',
        'unit': 'Points of Stasis',
        'tags': ('gain', 'spend', 'refresh', 'commit'),
        'refresh': 'empty'
    },
    'gossamer': {
        'name': 'Gossamer',
        'list_order': 8,
        'unit': 'Strands of Gossamer',
        'tags': ('gain', 'spend', 'refresh', 'commit', 'universal'),
        'refresh': 'empty',
        'check': gossamer_check
    },
    'resonance': {
        'name': 'Resonance',
        'unit': 'Points of Resonance',
        'tags': ('gain', 'spend', 'refresh', 'commit'),
        'refresh': 'empty'
    },

}

EXPAND_POOL = {
    'solar': {10: ('Immanent Solar Glory', )},

    'abyssal': {10: ('Essence Engorgement Technique', )},

    'infernal': {10: ("Sun-Heart Furnace Soul", "Sweet Agony Savored", "Flames Lit Within", "Riding Tide Ascension",
                      "Beauteous Carnage Incentive", "Transcendent Desert Within", "Glory-Stoking Congregation",
                      "Reassuring Slave Chorus")},

    'lunar': {10: ('Silver Lunar Resolution', )},

    'alchemical': {10: ("Auxiliary Essence Storage Unit", )},

    'raksha': {5: ('Bottomless Dream Gullet', )},

    'spirit': {10: ('Essence Plethora', )}
}

OVERDRIVE_POOL = {
    'solar': {10: ('Storm-Gathering Practice', "Hero's Fatal Resolve", 'Fading Light Quickening',
                   "Righteous Avenger's Aspect", 'Certain Victory Formulation', 'Red Dawn Ascending',
                   'Essence-Gathering Temper', 'You Shall Not Pass', "Virtuous Warrior's Fortitude",
                   'Labors Treasured and Defended', 'Is This Tomorrow', 'Triumph Signed By Excellence',
                   'Honest Turnabout Assault', 'Wrongly-Condemned Rage', 'Jousting at Giants',
                   "Fearless Admiral's Dominion")},

    'abyssal': {10: ("Sunlight Bleeding Away", "Methodical Sniper Method", "'Til Death Do You Part",
                     "Sanguine Trophies Collected", "Pyrrhic Victory Conflagration", "Child of the Apocalypse",
                     "That I Should Be Haunted", "World-Betraying Knife Visage", "Monster in the Mist",
                     "Vengeful Mariner's Shanty"),
                15: ('Bright Days Painted Black', )},

    'infernal': {10: ("The King Still Stands", "Wayward Serf Remonstrations", "Specks Before Infinity",
                      "Follow The Leader", "Force-Draining Exigence", "Wind Shearing Hearts", "Hungry Wind Howling",
                      "The Face in the Darkness", "Wicked Void Reversal"),
                 15: ("Rage-Stoked Inferno Soul", "The Tide Turns"),
                 20: ("Song of the Depths", )},

    'lunar': {10: ("Never To Rise Again", "Biting At the Heels", "Undying Ratel's Vengeance",
                   "Disappointed Guardian-Spirit Correction", "Protean Exemplar Differentiation",
                   "World-Warden Onslaught", "Hunter-As-Bait Gambit", "Snarling Watchdog Retribution",
                   "Sleeping Dragon Awakens")},

    'sidereal': {10: ("Guarding the Weave", "Portentous Omens Manifested", "Tactic-Snatching Ingenuity",
                      "Mana Drips From Lotus Petals", "Covert Shadows Woven", "Horizon-Cresting Cavalry Rescue")},

    'alchemical': {5: ('Optimized Overcharge Device', ),
                   1: ('Expanded Charge Battery Submodule', )}
}

def retrieve_stats(character):
    essence = character.ndb.stats_dict['essence']
    willpower = character.ndb.stats_dict['willpower']
    virtues = character.ndb.stats_type['Virtue']
    return essence, willpower, virtues

def universal_willpower(character):
    return character.ndb.stats_dict['willpower']


def universal_limit(character):
    return 10


def solar_personal(character):
    essence, willpower, virtues = retrieve_stats(character)
    return essence*3 + willpower


def solar_peripheral(character):
    essence, willpower, virtues = retrieve_stats(character)
    return essence*7 + willpower + sum(virtues)


def universal_expanded(character):
    """
    def retrieve_max(self, owner):
        extended_charms = owner.template.template.extended_charms
        if not extended_charms:
            return 0
        total_extended = list()
        for worth, charm_names in extended_charms.items():
            found_values = sum([charm.current_value for charm in owner.advantages.cache_advantages
                                if charm.base_name == 'Charm' and charm.full_name in charm_names])
            if found_values:
                total_extended.append(found_values * worth)
        return sum(total_extended)
    """

def universal_overdrive(character):

    """
    def calculate_overdrive(self, owner):
        overdrive_charms = owner.template.template.overdrive_charms
        if not overdrive_charms:
            return 0
        total_overdrive = list()
        for worth, charm_names in overdrive_charms.items():
            found_values = sum([charm.current_value for charm in owner.advantages.cache_advantages
                                if charm.base_name == 'Charm' and charm.full_name in charm_names])
            if found_values:
                total_overdrive.append(found_values * worth)
        return sum(total_overdrive)

    def retrieve_max(self, owner):
        pool_calc = self.calculate_overdrive(owner)
        return sorted([0, pool_calc, 25])[1]
    """

def terrestrial_personal(character):
    essence, willpower, virtues = retrieve_stats(character)
    return essence + 11


def terrestrial_peripheral(character):
    essence, willpower, virtues = retrieve_stats(character)
    return essence*4 + 23


def lunar_personal(character):
    essence, willpower, virtues = retrieve_stats(character)
    return essence + willpower*2


def lunar_peripheral(character):
    essence, willpower, virtues = retrieve_stats(character)
    return essence*4 + willpower*2 + max(virtues)*4


def sidereal_personal(character):
    essence, willpower, virtues = retrieve_stats(character)
    return essence*2 + willpower


def sidereal_peripheral(character):
    essence, willpower, virtues = retrieve_stats(character)
    return essence*6 + willpower + sum(virtues)


def spirit_personal(character):
    essence, willpower, virtues = retrieve_stats(character)
    return essence*10


def alchemical_personal(character):
    essence, willpower, virtues = retrieve_stats(character)
    return 0


def alchemical_peripheral(character):
    essence, willpower, virtues = retrieve_stats(character)
    return 0


def dragonking_personal(character):
    essence, willpower, virtues = retrieve_stats(character)
    return essence*4 + willpower*2 + sum(character.ndb.stats_dict['conviction'], character.ndb.stats_dict['valor'])


def godblooded_personal(character):
    essence, willpower, virtues = retrieve_stats(character)
    return 0



TEMPLATES = {
    'mortal': {
        'name': 'Mortal',
        'list_order': 0,
        'pools': {'willpower': universal_willpower}
    },
    'solar': {
        'name': 'Solar',
        'list_order': 5,
        'pools': {'personal': solar_personal, 'peripheral': solar_peripheral, 'willpower': universal_willpower,
                  'limit': universal_limit},
        'charm_type': 'Solar',
        'info_fields': ('Caste', 'Virtue Flaw'),
        'info_choices': {'Caste': ('Dawn', 'Zenith', 'Eclipse', 'Twilight', 'Night')},
        'extra_sheet_colors': {'border': 'Y', 'slash': 'r', 'section_name': 'y'},
        'sheet_column_1': ('Caste',),
        'sheet_column_2': ()
    },
    'abyssal': {
        'name': 'Abyssal',
        'list_order': 6,
        'pools': {'personal': solar_personal, 'peripheral': solar_peripheral, 'willpower': universal_willpower,
                  'resonance': universal_limit},
        'charm_type': 'Abyssal',
        'info_fields': ('Caste', 'Flawed Virtue', 'Liege', 'Doom'),
        'info_choices': {'Caste': ('Dusk', 'Midnight', 'Moonshadow', 'Daybreak', 'Day')},
        'extra_sheet_colors': {'border': 'Y', 'slash': 'r', 'section_name': 'y'},
        'sheet_column_1': ('Caste', 'Flawed Virtue', 'Doom'),
        'sheet_column_2': ('Liege', )
    },
    'infernal': {
        'name': 'Infernal',
        'list_order': 7,
        'pools': {'personal': solar_personal, 'peripheral': solar_peripheral, 'willpower': universal_willpower,
                  'limit': universal_limit},
        'charm_type': 'Infernal',
        'info_fields': ('Caste', 'Urge Archetype', 'Favored Yozi'),
        'info_choices': {'Caste': ('Slayer', 'Malefactor', 'Fiend', 'Defiler', 'Scourge')},
        'extra_sheet_colors': {'border': 'Y', 'slash': 'r', 'section_name': 'y'},
        'sheet_column_1': ('Caste', 'Urge Archetype'),
        'sheet_column_2': ('Favored Yozi',)
    },
    'lunar': {
        'name': 'Lunar',
        'list_order': 15,
        'pools': {'personal': lunar_personal, 'peripheral': lunar_peripheral, 'willpower': universal_willpower,
                  'limit': universal_limit},
        'charm_type': 'Lunar',
        'info_fields': ('Caste', 'Totem Animal', 'Virtue Flaw'),
        'info_choices': {'Caste': ('Full Moon', 'Changing Moon', 'No Moon')},
        'extra_sheet_colors': {'border': 'Y', 'slash': 'r', 'section_name': 'y'},
        'sheet_column_1': ('Caste', 'Virtue Flaw'),
        'sheet_column_2': ('Totem Animal', )
    },
    'terrestrial': {
        'name': 'Terrestrial',
        'list_order': 20,
        'pools': {'personal': terrestrial_personal, 'peripheral': terrestrial_peripheral,
                  'willpower': universal_willpower, 'limit': universal_limit},
        'charm_type': 'Terrestrial',
        'info_fields': ('Aspect', 'Family', 'Nation', 'Primary Virtue'),
        'info_choices': {'Aspect': ('Fire', 'Air', 'Water', 'Wood', 'Earth')},
        'extra_sheet_colors': {'border': 'Y', 'slash': 'r', 'section_name': 'y'},
        'sheet_column_1': ('Aspect', 'Nation'),
        'sheet_column_2': ('Family', 'Primary Virtue')
    },
    'sidereal': {
        'name': 'Sidereal',
        'list_order': 25,
        'pools': {'personal': sidereal_personal, 'peripheral': sidereal_peripheral, 'willpower': universal_willpower,
                  'limit': universal_limit, 'paradox': universal_limit},
        'charm_type': 'Sidereal',
        'info_fields': ('Caste', 'Faction'),
        'info_choices': {'Caste': ('Journeys', 'Battles', 'Serenity', 'Secrets', 'Endings')},
        'extra_sheet_colors': {'border': 'Y', 'slash': 'r', 'section_name': 'y'},
        'sheet_column_1': ('Caste',),
        'sheet_column_2': ('Faction',)
    },
    'alchemical': {
        'name': 'Alchemical',
        'list_order': 30,
        'pools': {'personal': alchemical_personal, 'peripheral': alchemical_peripheral,
                  'willpower': universal_willpower, 'clarity': universal_limit},
        'charm_type': 'Alchemical',
        'info_fields': ('Caste', 'Nation', 'Primary Virtue'),
        'info_choices': {'Caste': ('Orichalcum', 'Moonsilver', 'Starmetal', 'Jade', 'Soulsteel')},
        'extra_sheet_colors': {'border': 'Y', 'slash': 'r', 'section_name': 'y'},
        'sheet_column_1': ('Caste', ),
        'sheet_column_2': ('Nation', 'Primary Virtue')
    },
    'raksha': {
        'name': 'Raksha',
        'list_order': 35,
        'pools': {'personal': spirit_personal, 'willpower': universal_willpower, 'stasis': universal_limit},
        'charm_type': 'Raksha',
        'info_fields': ('Caste', 'Lure',),
        'info_choices': {'Caste': ("Diplomat", "Courtier", "Imperial Raksha", "Scribe", "Entertainer", "Luminary",
                                   "Eshu", "Ornamental Raksha", "Warrior", "Anarch", "Xia", "Cataphract", "Worker",
                                   "Panjandrum", "Artisan", "Strategos", "Guide", "Harbinger", "Vagabond", "Nomad",
                                   "Ferryman", "Herald", "Skald", "Dragoon", "Attendant")},
        'extra_sheet_colors': {'border': 'Y', 'slash': 'r', 'section_name': 'y'},
        'sheet_column_1': ('Caste', ),
        'sheet_column_2': ('Lure', )
    },
    'jadeborn': {
        'name': 'Jadeborn',
        'list_order': 40,
        'pools': {'personal': spirit_personal, 'willpower': universal_willpower, 'divergence': universal_limit},
        'charm_type': 'Jadeborn',
        'info_fields': ('Caste', ),
        'info_choices': {'Caste': ('Artisan', 'Worker', 'Warrior')},
        'extra_sheet_colors': {'border': 'Y', 'slash': 'r', 'section_name': 'y'},
        'sheet_column_1': ('Caste', ),
        'sheet_column_2': ()
    },
    'dragon-king': {
        'name': 'Dragon-King',
        'list_order': 45,
        'pools': {'personal': dragonking_personal, 'willpower': universal_willpower},
        'charm_type': None,
        'info_fields': ('Breed', ),
        'info_choices': {'Breed': ('Anklok', 'Mosok', 'Pterok', 'Raptok')},
        'extra_sheet_colors': {'border': 'Y', 'slash': 'r', 'section_name': 'y'},
        'sheet_column_1': ('Breed', ),
        'sheet_column_2': ()
    },
    'ghost': {
        'name': 'Ghost',
        'list_order': 50,
        'pools': {'personal': spirit_personal, 'willpower': universal_willpower},
        'charm_type': None,
        'info_fields': (),
        'info_choices': {},
        'extra_sheet_colors': {'border': 'Y', 'slash': 'r', 'section_name': 'y'},
        'sheet_column_1': (),
        'sheet_column_2': ()
    },
    'spirit': {
        'name': 'Spirit',
        'list_order': 55,
        'pools': {'personal': spirit_personal, 'willpower': universal_willpower},
        'charm_type': 'Spirit',
        'info_fields': ('Nature', ),
        'info_choices': {'Nature': ('God', 'Demon', 'Elemental')},
        'extra_sheet_colors': {'border': 'Y', 'slash': 'r', 'section_name': 'y'},
        'sheet_column_1': ('Nature', ),
        'sheet_column_2': ()
    },
    'god-blooded': {
        'name': 'God-Blooded',
        'list_order': 60,
        'pools': {'personal': godblooded_personal, 'willpower': universal_willpower},
        'charm_type': 'God-Blooded',
        'info_fields': ('Heritage', ),
        'info_choices': {'Heritage': ('Divine', 'Demon', 'Fae', 'Ghost', 'Solar', 'Lunar', 'Sidereal', 'Abyssal',
                                 'Infernal')},
        'extra_sheet_colors': {'border': 'Y', 'slash': 'r', 'section_name': 'y'},
        'sheet_column_1': ('Heritage', ),
        'sheet_column_2': ()
    },

}
