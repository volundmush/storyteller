from __future__ import unicode_literals

class Splat(object):
    id = 0
    name = '<unknown>'

    def __init__(self, owner):
        self.owner = owner
        self.handler = owner
        self.game = owner.game
        self.data = owner
