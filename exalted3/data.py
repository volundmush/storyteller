from __future__ import unicode_literals
from storyteller.exalted3.stats import ALL_STATS
from storyteller.exalted3.customs import ALL_CUSTOMS


from storyteller.base.data import GameData

from storyteller.base import Template, Splat
from storyteller.base import Pool, CharacterPool, WillpowerPool, Specialty, Merit, CustomSet
from storyteller.models import Game
from storyteller.exalted3.models import CharmSet

from athanor.utils.text import dramatic_capitalize, sanitize_string, partial_match




# CUSTOMS


# Merits
class ExMerit(Merit):
    pass


class ExFlaw(ExMerit):
    pass


class MeritManager(object):
    category_id = 1
    name = 'Merits'
    use = ExMerit

    def __init__(self, data):
        self.data = data
        self.game = data.game
        self.choices = [self.use(self, mod) for mod in self.game.merits.filter(category_id=self.category_id)]

    def add(self, name=None):
        pass


class FlawManager(MeritManager):
    category_id = 2
    name = 'Flaws'
    use = ExFlaw


ALL_MERITS = (MeritManager,)

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

    def __repr__(self):
        return '<%s PowerSet: %s>' % (self.owner, self.name)


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
    pool_classes = (WillpowerPool,)
    willpower = 3


class Solar(Template):
    id = 2
    name = 'Solar'
    x_name = 'Caste'
    x_classes = (Dawn, Zenith, Twilight, Night, Eclipse)
    pool_classes = (WillpowerPool, SolarPersonal, SolarPeripheral)
    willpower = 5


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


class ExData(GameData):
    load_stats = ALL_STATS
    load_custom = ALL_CUSTOMS




GAME_DATA = GameData('Exalted 3e')