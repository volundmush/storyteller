from __future__ import unicode_literals
from evennia.utils import lazy_property

class CharacterStat(object):
    owner = None
    handler = None
    stat = None
    rating = None

    def __init__(self, owner, handler, stat):
        self.owner = owner
        self.handler = handler
        self.stat = stat

    def __str__(self):
        return self.name

    def __int__(self):
        return self.rating

    @property
    def name(self):
        return self.stat.name

    @property
    def id(self):
        return self.stat.id


class CharacterWillpowerStat(CharacterStat):
    pass


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

    def __str__(self):
        return self.name

    def __int__(self):
        return self.id

    def __repr__(self):
        return '<%s: (%s) %s>' % (self.category, self.id, self.name)


class Attribute(Stat):
    category = 'Attribute'
    default = 1


class PhysicalAttribute(Attribute):
    sub_category = 'Physical'


class SocialAttribute(Attribute):
    sub_category = 'Social'


class MentalAttribute(Attribute):
    sub_category = 'Mental'


class Skill(Stat):
    category = 'Skill'
    default = 0
    can_specialize = True


class PhysicalSkill(Skill):
    sub_category = 'Physical'


class SocialSkill(Skill):
    sub_category = 'Social'


class MentalSkill(Skill):
    sub_category = 'Mental'


class Advantage(Stat):
    category = 'Advantage'


class PowerStat(Advantage):
    id = 1
    name = 'PowerStat'
    default = 1


class Willpower(Advantage):
    id = 2
    name = 'Willpower'
    use = CharacterWillpowerStat


# Specialty Data
class CharacterSpecialty(object):
    pass


class Specialty(object):
    use = CharacterSpecialty

    def __init__(self, data, model):
        self.stat = data.stats_dict[model.stat_id]
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

# Merit Data
class CharacterMerit(object):
    pass


class Merit(object):
    use = CharacterMerit
    category = 'Merit'

    def __init__(self, data, model):
        self.data = data
        self.model = model
        self.id = model.id
        self.name = model.key

    def __str__(self):
        return self.name


# Splat Data
class Splat(object):
    name = '<Unknown'
    id = 0
    display = 'Splat'

    def __str__(self):
        return self.name

    def __int__(self):
        return self.id




# Template Data
class CharacterTemplate(object):
    pass


class Template(object):
    name = '<Unknown>'
    id = 0
    x_classes = ()
    y_classes = ()
    z_classes = ()
    x_name = None
    y_name = None
    z_name = None
    pool_classes = ()
    willpower = 1
    extra_stat_classes = ()
    use = CharacterTemplate

    def __str__(self):
        return self.name

    def __int__(self):
        return self.id

    def __repr__(self):
        return '<Template: %s>' % self.name

    def __init__(self, data):
        if self.x_classes:
            self.x_choices = tuple([data.x_splats_dict[cla.id] for cla in self.x_classes])
        if self.y_classes:
            self.y_choices = tuple([data.y_splats_dict[cla.id] for cla in self.y_classes])
        if self.z_classes:
            self.z_choices = tuple([data.z_splats_dict[cla.id] for cla in self.z_classes])
        self.pools = tuple([data.pools_dict[cla.id] for cla in self.pool_classes])
        if self.extra_stat_classes:
            self.extra_stats = tuple([data.stats_dict[cla.id] for cla in self.extra_stat_classes])


class Commit(object):
    name = '<unknown>'
    amount = 0
    owner = None
    model = None

    def __str__(self):
        return self.key

    def __int__(self):
        return self.amount

    def __init__(self, owner, model):
        self.owner = owner
        self.model = model

    def delete(self):
        self.model.delete()


class CharacterPool(object):
    pass


class CharacterWillPower(CharacterPool):
    pass


class Pool(object):
    name = '<unknown>'
    id = 0
    unit_singular = 'point'
    unit_plural = 'points'
    display_name = 'Pool'
    features = ('burn', 'regain', 'commit', 'refresh')
    on_refresh = 1
    category = None
    list_order = 0
    power = 'Essence'
    use = CharacterPool

    def __str__(self):
        return self.name


class WillpowerPool(Pool):
    category = 'Pool'
    name = 'Willpower'
    id = 1
    unit_singular = 'point'
    unit_plural = 'points'
    display_name = 'Willpower'
    features = ('burn', 'regain', 'refresh')
    list_order = 10
    use = CharacterWillPower