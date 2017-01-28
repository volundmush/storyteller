from __future__ import unicode_literals
from storyteller.base import PhysicalAttribute, SocialAttribute, MentalAttribute, Stat
from storyteller.base import PowerStat, Willpower as OldWillpower, CharacterStat, Template, Splat
from storyteller.base import Pool, CharacterPool, WillpowerPool


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

# Pools

class SolarPersonal(Pool):
    id = '2'
    name = 'Personal'


class SolarPeripheral(Pool):
    id = 3
    name = 'Peripheral'


ALL_POOLS = (WillpowerPool, SolarPersonal, SolarPeripheral)

# Splats
# Mortal
class _Profession(Splat):
    pass


class Warrior(_Profession):
    id = 1
    name = 'Warrior'



class Priest(_Profession):
    id = 2
    name = 'Priest'


class Savant(_Profession):
    id = 3
    name = 'Savant'


class Criminal(_Profession):
    id = 4
    name = 'Criminal'


class Broker(_Profession):
    id = 5
    name = 'Broker'

# Solar
class _Caste(Splat):
    pass

class Dawn(_Caste):
    id = 6
    name = 'Dawn'


class Zenith(_Caste):
    id = 7
    name = 'Zenith'


class Twilight(_Caste):
    id = 8
    name = 'Twilight'


class Night(_Caste):
    id = 9
    name = 'Night'


class Eclipse(_Caste):
    id = 10
    name = 'Eclipse'


ALL_X_SPLATS = (Warrior, Priest, Savant, Criminal, Broker, Dawn, Zenith, Twilight, Night, Eclipse)


class Mortal(Template):
    id = 1
    name = 'Mortal'
    x_name = 'Profession'
    x_classes = (Warrior, Priest, Savant, Criminal, Broker)
    pool_classes = (WillpowerPool)

class Solar(Template):
    id = 2
    name = 'Solar'
    x_name = 'Caste'
    x_classes = (Dawn, Zenith, Twilight, Night, Eclipse)
    pool_classes = (WillpowerPool, SolarPersonal, SolarPeripheral)


ALL_TEMPLATES = (Mortal, Solar)



class GameData(object):
    id = 0

    def __init__(self, id):
        self.id = id

        self.stats = [stat() for stat in ALL_STATS]
        self.stats_dict = {stat.id: stat for stat in self.stats}
        self.stats_name = {stat.name: stat for stat in self.stats}

        self.x_splats = [Spl() for Spl in ALL_X_SPLATS]
        self.x_splats_dict = {spl.id: spl for spl in self.x_splats}

        self.y_splats = ()
        self.y_splats_dict = {}

        self.z_splats = ()
        self.z_splats_dict = {}

        self.pools = [pool() for pool in ALL_POOLS]
        self.pools_dict = {pool.id: pool for pool in self.pools}

        self.templates = [tem(self) for tem in ALL_TEMPLATES]


GAME_DATA = GameData(1)