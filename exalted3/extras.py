from storyteller.exbase.extras import CharmManager, Merits, Flaws, Rituals, Sorcery, ATTRIBUTE_CHARMS
from storyteller.exbase.extras import MutableSet

MARTIAL_ARTS = ('Snake', 'Tiger', 'Single Point Shining Into the Void', 'White Reaper', 'Ebon Shadow', 'Crane',
                'Silver-Voiced Nightingale', 'Righteous Devil', 'Black Claw', 'Steel Devil')

ABILITY_CHARMS = ('Archery', 'Athletics', 'Awareness', 'Brawl', 'Bureaucracy', 'Craft', 'Dodge',
                   'Integrity', 'Investigation', 'Larceny', 'Linguistics', 'Lore', 'Medicine',
                   'Melee', 'Occult', 'Performance', 'Presence',  'Resistance', 'Ride',
                   'Sail', 'Socialize', 'Stealth', 'Survival', 'Thrown', 'War')


class CraftSet(MutableSet):
    name = 'Crafts'
    stat_init = ('Weapon Forging', 'Armoring', 'Architecture', 'Tailoring', 'Woodwork', 'Carpentry', 'Cooking',
                 'Artifice', 'Geomancy', 'First Age Artifice')


class StyleSet(MutableSet):
    name = 'Styles'
    stat_init = MARTIAL_ARTS


class StyleCharms(CharmManager):
    name = 'Martial Arts Charms'
    sub_init = MARTIAL_ARTS


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


ALL_EXTRAS = (CraftSet, StyleSet, StyleCharms, Merits, Flaws, Rituals, Sorcery, SolarCharms, AbyssalCharms, LunarCharms,
              TerrestrialCharms)