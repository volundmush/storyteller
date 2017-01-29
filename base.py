from __future__ import unicode_literals
from athanor.utils.text import dramatic_capitalize, sanitize_string, partial_match


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

    def __init__(self, owner, tem, mod):
        self.owner = owner
        self.handler = owner
        self.data = owner.data
        self.template = tem
        self.model = mod

    def __str__(self):
        return self.template.name

    def __int__(self):
        return self.template.id


class Template(object):
    name = '<Unknown>'
    id = 0
    x_classes = ()
    y_classes = ()
    z_classes = ()
    x_name = None
    y_name = None
    z_name = None
    pool_classes = list()
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