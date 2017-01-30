from storyteller.exbase.extras import CharmManager, Merits, Flaws, Rituals, Sorcery

ABILITY_CHARMS = {1: 'Archery', 2: 'Athletics', 3: 'Awareness', 4: 'Brawl', 5: 'Bureaucracy', 6: 'Craft', 7: 'Dodge',
                   8: 'Integrity', 9: 'Investigation', 10: 'Larceny', 11: 'Linguistics', 12: 'Lore', 13: 'Medicine',
                   14: 'Melee', 15: 'Occult', 16: 'Performance', 17: 'Presence', 18: 'Resistance', 19: 'Ride',
                   20: 'Sail', 21: 'Socialize', 22: 'Stealth', 23: 'Survival', 24: 'Thrown', 25: 'War'}


class SolarCharms(CharmManager):
    category_id = 200
    name = 'Solar Charms'
    choice_init = ABILITY_CHARMS


ALL_EXTRAS = (Merits, Flaws, Rituals, Sorcery, SolarCharms)