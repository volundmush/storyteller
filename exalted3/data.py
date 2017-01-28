from __future__ import unicode_literals
from storyteller.base import PhysicalAttribute, SocialAttribute, MentalAttribute, Stat
from storyteller.base import PowerStat, Willpower as OldWillpower, CharacterStat, Template, Splat
from storyteller.base import Pool, CharacterPool, WillpowerPool, Specialty, Merit
from storyteller.models import Game
from storyteller.exalted3.models import CharmSet

from athanor.utils.text import dramatic_capitalize, sanitize_string, partial_match


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


# Merits
class ExMerit(Merit):
    pass


class ExFlaw(ExMerit):
    pass


# Pools

class SolarPersonal(Pool):
    id = '2'
    name = 'Personal'


class SolarPeripheral(Pool):
    id = 3
    name = 'Peripheral'


ALL_POOLS = (WillpowerPool, SolarPersonal, SolarPeripheral)

# CHARMS AND POWERS

class ExPower(object):

    def __init__(self, powerset, model):
        self.owner = powerset
        self.model = model
        self.name = model.key

    def __str__(self):
        return self.name

class PowerSet(object):
    use = ExPower

    def __init__(self, owner, id, name):
        self.owner = owner
        self.id = id
        self.name = name
        self.model, created = CharmSet.objects.get_or_create(category_id=owner.category_id, sub_id=id)

        self.charms = [self.use(self, mod) for mod in self.model.charms.all()]

    def add(self, creator, name=None):
        if not name:
            raise ValueError("What should it be called?")


class CharmManager(object):
    category_id = 0
    use = PowerSet
    choice_init = {}

    def __init__(self, data):
        self.data = data
        self.choices = list()
        self.choices_dict = dict()
        for k, v in self.choice_init.iteritems():
            p = self.use(self, k, v)
            self.choices.append(p)
            self.choices_dict[p.id] = p

    def __str__(self):
        return self.name


class SolarCharm(CharmManager):
    category_id = 1
    name = 'Solar'
    choice_init = {1: 'Archery', 2: 'Athletics', 3: 'Awareness', 4: 'Brawl', 5: 'Bureaucracy', 6: 'Craft', 7: 'Dodge',
                   8: 'Integrity', 9: 'Investigation', 10: 'Larceny', 11: 'Linguistics', 12: 'Lore', 13: 'Medicine',
                   14: 'Melee', 15: 'Occult', 16: 'Performance', 17: 'Presence', 18: 'Resistance', 19: 'Ride',
                   20: 'Sail', 21: 'Socialize', 22: 'Stealth', 23: 'Survival', 24: 'Thrown', 25: 'War'}


class Sorcery(CharmManager):
    category_id = 100
    name = 'Sorcery'
    choice_init = {1: 'Terrestrial', 2: 'Celestial', 3: 'Solar'}


ALL_POWERSETS = (SolarCharm, Sorcery)

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


# GAME DATA

class MeritData(object):
    id = 0
    name = 'Merits'
    use = ExMerit

    def __init__(self, data):
        self.data = data
        self.game = data.game
        self.merits = [self.use(self.data, mod) for mod in self.game.merits.filter(category_id=self.id)]
        self.merits_dict = {mer.id: mer for mer in self.merits}

    def add(self, creator, name=None):
        if not name:
            raise ValueError("No name set!")
        name = dramatic_capitalize(sanitize_string(name))
        if self.game.merits.filter(category_id=self.id, key__iexact=name).count():
            raise ValueError("This name is already in use!")
        new_mod = self.game.merits.create(category_id=self.id, key=name, creator=creator)
        new_mer = self.use(self.data, new_mod)
        self.merits.append(new_mer)
        self.merits_dict[new_mer.id] = new_mer


class FlawData(MeritData):
    id = 1
    use = ExFlaw


class SpecialtyData(object):
    id = 0

    def __init__(self, id, data):
        self.id = id
        self.data = data
        self.game = data.game

        self.specialties = [Specialty(self, mod) for mod in self.game.specialties.all()]
        self.specialties_dict = {}
        for spec in self.specialties:
            if not spec.stat in self.specialties_dict.keys():
                self.specialties_dict[spec.stat] = list()
            self.specialties_dict[spec.stat].append(spec)

    def add(self, creator, stat=None, name=None):
        if not stat:
            raise ValueError("Stat not found!")
        stat = partial_match(self.data.stats, stat)
        if not stat:
            raise ValueError("Stat not found!")
        if not name:
            raise ValueError("Name not entered!")
        name = dramatic_capitalize(sanitize_string(name))
        if self.game.specialties.filter(stat_id=stat.id, key__iexact=name).count():
            raise ValueError("Specialty of that name already exists.")
        new_mod = self.game.specialties.create(stat_id=stat.id, key=name, creator=creator)
        new_spec = Specialty(self.data, new_mod)
        self.specialties.append(new_spec)
        spec_list = self.specialties_dict.get(stat, list())
        spec_list.append(new_spec)
        self.specialties_dict[stat] = spec_list


class GameData(object):
    id = 0

    def __init__(self, gamename):
        self.game, created = Game.objects.get_or_create(key=gamename)

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

        self.specialties = SpecialtyData(id, self)

        self.merits = MeritData(self)
        self.flaws = FlawData(self)

        self.powers = [cla(self) for cla in ALL_POWERSETS]
        self.powers_dict = {cla.category_id: cla for cla in self.powers}


GAME_DATA = GameData('Exalted 3e')