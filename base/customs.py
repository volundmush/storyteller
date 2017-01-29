from __future__ import unicode_literals
from athanor.utils.text import dramatic_capitalize, sanitize_string, partial_match

# CUSTOM STAT HANDLING

class CharacterCustomStat(object):
    specialty = CharacterCustomSpecialty

    def __init__(self, owner, stat, model):
        self.owner = owner
        self.handler = owner.handler
        self.data = self.handler.data
        self.game = self.handler.game
        self.stat = stat
        self.handler = owner.handler
        self.model = model
        self.rating = int(model.rating)
        self.id = int(model.id)
        self.specialties = list()
        self.specialties_dict = dict()
        if self.specialty:
            for row in self.model.specialties.all():
                proto = self.stat.specialties_dict[row.name.id]
                new_spec = self.specialty(self, proto, row)
                self.specialties.append(new_spec)
                self.specialties_dict[row.id] = new_spec
        self.load()

    @property
    def name(self):
        return self.stat.name

    def __str__(self):
        return self.name

    def load(self):
        pass

class CharacterCustomSpecialty(object):

    def __init__(self, owner, spec, model):
        self.owner = owner
        self.handler = owner.handler
        self.game = owner.game
        self.data = owner.data
        self.spec = spec
        self.model = model
        self.id = int(model.id)
        self.rating = int(model.rating)

    @property
    def name(self):
        return self.spec.name

    def __str__(self):
        return self.name

    def __int__(self):
        return self.rating


class CustomSpecialty(object):

    def __init__(self, owner, mod):
        self.owner = owner
        self.handler = owner.handler
        self.game = owner.game
        self.data = owner.data
        self.model = mod
        self.id = int(mod.id)
        self.name = str(mod.key)

    def __str__(self):
        return self.name

    def __int__(self):
        return self.id


class CustomStat(object):
    use = CharacterCustomStat
    specialty = CustomSpecialty

    def __init__(self, owner, mod):
        self.owner = owner
        self.handler = owner.handler
        self.data = owner.data
        self.game = owner.game
        self.model = mod
        self.id = int(mod.id)
        self.name = str(mod.key)
        self.specialties = list()
        self.specialties_dict = dict()
        if self.specialty:
            for row in self.model.specialties.all():
                new_spec = self.specialty(self, row)
                self.specialties.append(new_spec)
                self.specialties_dict[row.id] = new_spec

    def __str__(self):
        return self.name

    def __int__(self):
        return self.id

    def __repr__(self):
        return '<%s: %s>' % (self.owner.name, self.name)


class CustomSet(object):
    category_id = 0
    name = '<unknown>'
    use = CustomStat

    def __init__(self, owner):
        self.owner = owner
        self.handler = owner
        self.data = owner.data
        self.game = owner.game
        self.model, created = self.game.customs.get_or_create(category_id=self.category_id)
        self.stats = [self.use(self, mod) for mod in self.model.stats.all()]
        self.stats_dict = {stat.id: stat for stat in self.stats}

    def add(self, creator, name=None):
        if not name:
            raise ValueError("No name entered!")
        name = dramatic_capitalize(sanitize_string(name))
        if self.model.stats.filter(key__iexact=name).count():
            raise ValueError("Name already in use.")
        new_mod = self.model.stats.create(key=name, creator=creator)
        new_stat = self.use(self, new_mod)
        self.stats.append(new_stat)
        self.stats_dict[new_mod.id] = new_stat
        return new_stat