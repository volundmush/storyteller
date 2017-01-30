from __future__ import unicode_literals
from athanor.utils.text import dramatic_capitalize, sanitize_string, partial_match

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
    use = CharacterTemplate
    base_colors = {'border': 'n', 'slash': 'n', 'section_name': 'n',
                   'statdot': 'n', 'statname': 'n', 'statfill': 'n'}
    tem_colors = {}

    def __str__(self):
        return self.name

    def __int__(self):
        return self.id

    def __repr__(self):
        return '<Template: %s>' % self.name

    def __init__(self, owner):
        self.owner = owner
        self.handler = owner
        self.game = owner.game
        self.data = owner
        self.colors = dict()
        for d in (self.base_colors, self.tem_colors):
            self.colors.update(d)

        if self.x_classes:
            self.x_choices = tuple([self.data.x_splats_dict[cla.id] for cla in self.x_classes])
        if self.y_classes:
            self.y_choices = tuple([self.data.y_splats_dict[cla.id] for cla in self.y_classes])
        if self.z_classes:
            self.z_choices = tuple([self.data.z_splats_dict[cla.id] for cla in self.z_classes])
        self.pools = tuple([self.data.pools_dict[cla.id] for cla in self.pool_classes])