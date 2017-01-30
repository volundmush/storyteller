from __future__ import unicode_literals

class CharacterStatPower(object):

    def __init__(self, owner, power, mod):
        self.owner = owner
        self.power = power
        self.model = mod
        self.rating = int(mod.rating)

    @property
    def name(self):
        return self.power.name

    @property
    def id(self):
        return self.power.id

    def __int__(self):
        return self.id

    def __str__(self):
        return self.name


class StatPower(object):
    id = 0
    name = '<unknown>'
    use = CharacterStatPower
    lowest = 0
    highest = 10

    def __init__(self, owner):
        self.owner = owner
        self.handler = owner.handler
        self.data = owner.data
        self.game = owner.game


class StatPowerSet(object):
    category_id = 0
    name = '<unknown>'
    power_classes = ()

    def __init__(self, owner):
        self.owner = owner
        self.data = owner
        self.game = owner.game
        self.handler = owner
        self.model, created = self.game.statpowers.get_or_create(category_id=self.category_id)
        self.power_objs = [cla(self) for cla in self.power_classes]

    @property
    def id(self):
        return self.category_id

    def __str__(self):
        return self.name