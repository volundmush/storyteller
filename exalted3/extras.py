from storyteller.exbase.extras import CharmManager, Merits, Flaws, Rituals, Sorcery, ATTRIBUTE_CHARMS
from storyteller.exbase.extras import MutableSet

ABILITY_CHARMS = ('Archery', 'Athletics', 'Awareness', 'Brawl', 'Bureaucracy', 'Craft', 'Dodge',
                   'Integrity', 'Investigation', 'Larceny', 'Linguistics', 'Lore', 'Medicine',
                   'Melee', 'Occult', 'Performance', 'Presence',  'Resistance', 'Ride',
                   'Sail', 'Socialize', 'Stealth', 'Survival', 'Thrown', 'War')


class CraftSet(MutableSet):
    name = 'Crafts'


class StyleSet(MutableSet):
    name = 'Styles'


class SolarCharms(CharmManager):
    name = 'Solar Charms'
    sub_init = ABILITY_CHARMS


class AbyssalCharms(SolarCharms):
    name = 'Abyssal Charms'


class LunarCharms(CharmManager):
    name = 'Lunar Charms'
    sub_init = ATTRIBUTE_CHARMS


class TerrestrialCharms(SolarCharms):
    name = 'Terrestrial Charms'


ALL_EXTRAS = (CraftSet, StyleSet, Merits, Flaws, Rituals, Sorcery, SolarCharms, AbyssalCharms, LunarCharms,
              TerrestrialCharms)