from storyteller.exbase.extras import CharmManager, Merits as _Mer, Sorcery, Necromancy, ATTRIBUTE_CHARMS

ABILITY_CHARMS = {1: 'Archery', 2: 'Athletics', 3: 'Awareness', 5: 'Bureaucracy', 6: 'Craft', 7: 'Dodge',
                   8: 'Integrity', 9: 'Investigation', 10: 'Larceny', 11: 'Linguistics', 12: 'Lore', 13: 'Medicine',
                   14: 'Melee', 15: 'Occult', 16: 'Performance', 17: 'Presence', 18: 'Resistance', 19: 'Ride',
                   20: 'Sail', 21: 'Socialize', 22: 'Stealth', 23: 'Survival', 24: 'Thrown', 25: 'War',
                  4: 'Martial Arts', }


class SolarCharms(CharmManager):
    category_id = 200
    name = 'Solar Charms'
    choice_init = ABILITY_CHARMS


class AbyssalCharms(SolarCharms):
    category_id = 201
    name = 'Abyssal Charms'


class TerrestrialCharms(SolarCharms):
    name = 'Terrestrial Charms'
    category_id = 202


class SiderealCharms(SolarCharms):
    name = 'Sidereal Charms'
    category_id = 203


class LunarCharms(CharmManager):
    category_id = 204
    name = 'Lunar Charms'
    choice_init = ATTRIBUTE_CHARMS
    extra_init = {10: 'Knacks'}


class InfernalCharms(CharmManager):
    category_id = 205
    name = 'Infernal Charms'
    extra_init = {1: 'Malfeas', 2: 'Cecelyne', 3: 'SWLIHN', 4: 'Adorjan', 5: 'Ebon Dragon', 6: 'Kimbery',
                  7: 'Martial Arts', 8: 'Heretical'}


ALL_EXTRAS = (Sorcery, SolarCharms, AbyssalCharms, TerrestrialCharms, SiderealCharms, LunarCharms, InfernalCharms)