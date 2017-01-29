from __future__ import unicode_literals
from storyteller.base.stats import CharacterStat
from storyteller.base.data import PhysicalAttribute, SocialAttribute, MentalAttribute, Stat, PowerStat, Willpower as OldWillpower

class CharacterCraft(CharacterStat):
    pass


class CharacterMartial(CharacterStat):
    pass


# Advantages
class Essence(PowerStat):
    name = 'Essence'


class Willpower(OldWillpower):
    pass

ALL_ADVANTAGES = (Essence, Willpower)

# Attributes

class Strength(PhysicalAttribute):
    id = 3
    name = 'Strength'
    list_order = 1


class Dexterity(PhysicalAttribute):
    id = 4
    name = 'Dexterity'
    list_order = 2


class Stamina(PhysicalAttribute):
    id = 5
    name = 'Stamina'
    list_order = 3


class Charisma(SocialAttribute):
    id = 6
    name = 'Charisma'
    list_order = 1


class Manipulation(SocialAttribute):
    id = 7
    name = 'Manipulation'
    list_order = 2


class Appearance(SocialAttribute):
    id = 8
    name = 'Appearance'
    list_order = 3


class Perception(MentalAttribute):
    id = 9
    name = 'Perception'
    list_order = 1


class Intelligence(MentalAttribute):
    id = 10
    name = 'Intelligence'
    list_order = 2


class Wits(MentalAttribute):
    id = 11
    name = 'Wits'
    list_order = 3


ALL_ATTRIBUTES = (Strength, Stamina, Dexterity, Charisma, Manipulation, Appearance, Intelligence, Wits, Perception)


class _Ability(Stat):
    category = 'Ability'
    can_purchase = True
    can_specialize = True
    can_roll = True


class Archery(_Ability):
    id = 100
    name = 'Archery'


class Athletics(_Ability):
    id = 101
    name = 'Athletics'


class Awareness(_Ability):
    id = 102
    name = 'Awareness'


class Brawl(_Ability):
    id = 103
    name = 'Brawl'


class Bureaucracy(_Ability):
    id = 104
    name = 'Bureaucracy'


class Craft(_Ability):
    id = 105
    name = 'Craft'
    can_roll = True
    can_purchase = False
    can_specialize = False
    use = CharacterCraft
    load_default = True

class Dodge(_Ability):
    id = 106
    name = 'Dodge'


class Integrity(_Ability):
    id = 107
    name = 'Integrity'


class Investigation(_Ability):
    id = 108
    name = 'Investigation'


class Larceny(_Ability):
    id = 109
    name = 'Larceny'


class Linguistics(_Ability):
    id = 110
    name = 'Linguistics'


class Lore(_Ability):
    id = 111
    name = 'Lore'


class MartialArts(_Ability):
    id = 112
    name = 'Martial Arts'
    use = CharacterMartial
    load_default = True


class Medicine(_Ability):
    id = 113
    name = 'Medicine'


class Melee(_Ability):
    id = 114
    name = 'Melee'


class Occult(_Ability):
    id = 115
    name = 'Occult'


class Performance(_Ability):
    id = 116
    name = 'Performance'


class Presence(_Ability):
    id = 117
    name = 'Presence'


class Resistance(_Ability):
    id = 118
    name = 'Resistance'


class Ride(_Ability):
    id = 119
    name = 'Ride'


class Sail(_Ability):
    id = 120
    name = 'Sail'


class Socialize(_Ability):
    id = 121
    name = 'Socialize'


class Stealth(_Ability):
    id = 122
    name = 'Stealth'


class Survival(_Ability):
    id = 123
    name = 'Survival'


class Thrown(_Ability):
    id = 124
    name = 'Thrown'


class War(_Ability):
    id = 125
    name = 'War'


ALL_ABILITIES = (Archery, Athletics, Awareness, Brawl, Bureaucracy, Craft, Dodge, Integrity, Investigation, Larceny,
                 Linguistics, Lore, MartialArts, Medicine, Melee, Occult, Performance, Presence, Resistance,
                 Ride, Sail, Socialize, Stealth, Survival, Thrown, War)


ALL_STATS = ALL_ATTRIBUTES + ALL_ABILITIES + ALL_ADVANTAGES