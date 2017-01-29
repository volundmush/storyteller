from __future__ import unicode_literals
from athanor.utils.text import dramatic_capitalize, sanitize_string, partial_match

# CHARACTER Stats and Specialties

class CharacterSpecialty(object):

    def __init__(self, owner, proto, model):
        self.owner = owner
        self.handler = owner.handler
        self.model = model
        self.specialty = proto
        self.rating = int(model.rating)

    @property
    def name(self):
        return self.specialty.name

    def __str__(self):
        return self.name

    def __int__(self):
        return self.rating

    def __repr__(self):
        return '<%s %s Specialty: %s>' % (self.owner, self.name, self.rating)


class CharacterStat(object):
    specialty = CharacterSpecialty

    def __init__(self, owner, stat, model):
        self.owner = owner
        self.handler = owner.handler
        self.data = self.handler.data
        self.model = model
        self.stat = stat
        self.rating = int(model.rating)
        self.specialties = list()
        self.specialties_dict = dict()
        if self.specialty:
            for row in self.owner.persona.specialties.filter(specialty__stat_id=self.id):
                proto = self.stat.specialties_dict[row.specialty.id]
                new_spec = self.specialty(self, proto, row)
                self.specialties_dict[row.specialty.id] = new_spec
        self.load()

    def __str__(self):
        return self.name

    def __int__(self):
        return self.rating

    def __repr__(self):
        return '<%s %s: %s>' % (self.name, self.stat.category, self.rating)

    @property
    def name(self):
        return self.stat.name

    @property
    def id(self):
        return self.stat.id

    @property
    def list_order(self):
        return self.stat.list_order

    def load(self):
        pass

    def save(self):
        self.model.rating = self.rating
        self.model.save(update_fields=['rating'])

    def set(self, value=None):
        if not value:
            raise ValueError("No value entered!")
        try:
            val = int(value)
        except ValueError:
            raise ValueError("Must enter a number.")
        if val < self.stat.lowest or val > self.stat.highest:
            raise ValueError("Stat must be between %s and %s!" % (self.stat.lowest, self.stat.highest))
        old = self.rating
        self.rating = val
        if old != val:
            self.save()


# GAME Stats and Specialties
class Specialty(object):
    use = CharacterSpecialty

    def __init__(self, owner, model):
        self.handler = owner
        self.stat = owner
        self.model = model
        self.name = model.key
        self.id = model.id

    def __str__(self):
        return self.name

    def __int__(self):
        return self.id

    @property
    def full_name(self):
        return '%s/%s' % (self.stat.name, self.name)


class Stat(object):
    name = '<unknown>'
    id = 0
    category = None
    sub_category = None
    tags = tuple()
    default = 0
    can_roll = True
    can_purchase = True
    can_specialize = False
    list_order = 0
    use = CharacterStat
    load_default = False
    lowest = 0
    highest = 10
    max_specialty = 1
    max_all_specialties = 3
    specialty = Specialty

    def __str__(self):
        return self.name

    def __int__(self):
        return self.id

    def __repr__(self):
        return '<%s: (%s) %s>' % (self.category, self.id, self.name)

    def __init__(self, data):
        self.data = data
        self.game = data.game
        self.specialties = list()
        self.specialties_dict = dict()
        if self.specialty:
            for row in self.game.specialties.filter(stat_id=self.id):
                new_spec = self.specialty(self, row)
                self.specialties.append(new_spec)
                self.specialties_dict[new_spec.id] = new_spec

    def add(self, name=None):
        if not name:
            raise ValueError("No specialty name entered!")
        name = dramatic_capitalize(sanitize_string(name))
        if self.game.specialties.filter(stat_id=self.id, key__iexact=name).count():
            raise ValueError("Specialty name already in use.")
        new_mod = self.game.specialties.create(stat_id=self.id, key=name)
        new_spec = self.specialty(self, new_mod)
        self.specialties.append(new_spec)
        self.specialties_dict[new_mod.id] = new_spec
        return new_spec