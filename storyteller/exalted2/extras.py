from storyteller.exbase.extras import CharmManager, Merits as _Mer, Sorcery, Necromancy, ATTRIBUTE_CHARMS

ABILITY_CHARMS = {'Archery', 'Athletics', 'Awareness', 'Bureaucracy', 'Craft', 'Dodge', 'Integrity',
                  'Investigation', 'Larceny', 'Linguistics', 'Lore', 'Medicine', 'Melee', 'Occult',
                  'Performance', 'Presence', 'Resistance', 'Ride', 'Sail', 'Socialize', 'Stealth',
                  'Survival', 'Thrown', 'War', 'Martial Arts', }


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