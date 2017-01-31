from storyteller.exbase.extras import CharmManager, Merits, Flaws, Rituals, Sorcery, ATTRIBUTE_CHARMS
from storyteller.exbase.extras import MutableSet

ABILITY_CHARMS = {1: 'Archery', 2: 'Athletics', 3: 'Awareness', 4: 'Brawl', 5: 'Bureaucracy', 6: 'Craft', 7: 'Dodge',
                   8: 'Integrity', 9: 'Investigation', 10: 'Larceny', 11: 'Linguistics', 12: 'Lore', 13: 'Medicine',
                   14: 'Melee', 15: 'Occult', 16: 'Performance', 17: 'Presence', 18: 'Resistance', 19: 'Ride',
                   20: 'Sail', 21: 'Socialize', 22: 'Stealth', 23: 'Survival', 24: 'Thrown', 25: 'War'}


class CraftSet(MutableSet):
    name = 'Crafts'
    category_id = 50
    sub_id = 1


class StyleSet(CraftSet):
    name = 'Styles'
    sub_id = 2


class SolarCharms(CharmManager):
    category_id = 200
    name = 'Solar Charms'
    choice_init = ABILITY_CHARMS


class AbyssalCharms(SolarCharms):
    category_id = 201
    name = 'Abyssal Charms'


class LunarCharms(CharmManager):
    category_id = 202
    name = 'Lunar Charms'
    choice_init = ATTRIBUTE_CHARMS


class TerrestrialCharms(SolarCharms):
    category_id = 203
    name = 'Terrestrial Charms'


ALL_EXTRAS = (CraftSet, StyleSet, Merits, Flaws, Rituals, Sorcery, SolarCharms, AbyssalCharms, LunarCharms,
              TerrestrialCharms)