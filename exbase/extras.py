from __future__ import unicode_literals
from storyteller.base.extras import CharacterWordPower as _CharWord, MeritSet as _MeritSet
from storyteller.base.extras import CharacterMerit as _CharacterMerit, MutableSet, WordSet, SubManager

ATTRIBUTE_CHARMS = ('Strength', 'Dexterity', 'Stamina', 'Charisma', 'Manipulation', 'Appearance', 'Perception',
                    'Intelligence', 'Wits')


class Merits(_MeritSet):
    pass


class Flaws(_MeritSet):
    name = 'Flaws'


class Rituals(_MeritSet):
    name = 'Rituals'


class CharmSet(WordSet):

    def __repr__(self):
        return '<%s - %s: %s>' % (self.__class__.__name__, self.owner.name, self.name)


class CharmManager(SubManager):
    sub = CharmSet


class Sorcery(CharmManager):
    name = 'Sorcery'
    sub_init = ('Terrestrial', 'Celestial', 'Solar')


class Necromancy(CharmManager):
    name = 'Necromancy'
    sub_init = ('Shadowlands', 'Labyrinth', 'Void')

