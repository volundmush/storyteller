from __future__ import unicode_literals
from athanor.utils.text import dramatic_capitalize, sanitize_string, ANSIString

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
        self.flag_1 = int(model.flag_1)
        self.flag_2 = int(model.flag_2)
        self.specialties = list()
        self.specialties_dict = dict()
        if self.specialty:
            for row in self.handler.persona.specialties.filter(specialty__stat_id=self.id):
                proto = self.stat.specialties_dict[row.specialty.id]
                new_spec = self.specialty(self, proto, row)
                self.specialties_dict[row.specialty.id] = new_spec
        self.load()

    def __str__(self):
        return self.name

    def __int__(self):
        return self.rating

    def __repr__(self):
        return '<%s %s: %s>' % (self.name, self.category, self.rating)

    @property
    def category(self):
        return self.stat.category

    @property
    def sub_category(self):
        return self.stat.sub_category

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

    @property
    def favored(self):
        return self.flag_1

    @property
    def supernal(self):
        return self.flag_2


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

    @property
    def display_name(self):
        return self.name

    @property
    def display_prefix(self):
        if self.supernal:
            return '|r*|n'
        if self.favored:
            return '|w+|n'
        return ' '

    @property
    def display(self):
        if self.rating:
            return True
        if self.flag_1 or self.flag_2:
            return True
        if self.specialties:
            return True

    def sheet_format(self, width=23, no_prefix=False, fill_char='.', colors=None):
        if not colors:
            colors = {'statname': 'n', 'statfill': 'n', 'statdot': 'n'}
        display_name = ANSIString('|%s%s|n' % (colors['statname'], self.display_name))
        if no_prefix:
            prefix = ' '
        else:
            prefix = ANSIString('|r%s|n' % self.display_prefix)
        final_display = prefix + display_name
        if self.rating > width - len(final_display) - 1:
            dot_display = ANSIString('|%s%s|n' % (colors['statdot'], self.rating))
        else:
            dot_display = ANSIString('|%s%s|n' % (colors['statdot'], '*' * int(self)))
        fill_length = width - len(final_display) - len(dot_display)
        fill = ANSIString('|%s%s|n' % (colors['statfill'], fill_char * fill_length))
        return final_display + fill + dot_display


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