from __future__ import unicode_literals

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
    use = Commit


class CharacterWillPower(CharacterPool):
    pass


class Pool(object):
    name = '<unknown>'
    id = 0
    unit_singular = 'point'
    unit_plural = 'points'
    display_name = 'Pool'
    tags = ('burn', 'gain', 'commit', 'refresh')
    on_refresh = 1
    category = None
    list_order = 0
    power = 'Essence'
    use = CharacterPool

    def __str__(self):
        return self.name


class ReversePool(Pool):
    on_refresh = 0


class WillpowerPool(Pool):
    category = 'Pool'
    name = 'Willpower'
    id = 1
    unit_singular = 'point'
    unit_plural = 'points'
    display_name = 'Willpower'
    tags = ('burn', 'gain', 'refresh')
    list_order = 10
    use = CharacterWillPower