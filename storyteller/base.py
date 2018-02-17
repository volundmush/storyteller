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