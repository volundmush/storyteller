from __future__ import unicode_literals
from storyteller.base.extras import CharacterWordPower as _CharWord, MeritSet as _MeritSet
from storyteller.base.extras import CharacterMerit as _CharacterMerit, MutableSet, WordSet, SubManager

ATTRIBUTE_CHARMS = {1: 'Strength', 2: 'Dexterity', 3: 'Stamina', 4: 'Charisma', 5: 'Manipulation',
                    6: 'Appearance', 7: 'Perception', 8: 'Intelligence', 9: 'Wits'}


class Merits(_MeritSet):
    pass


class Flaws(_MeritSet):
    sub_id = 1
    name = 'Flaws'


class Rituals(_MeritSet):
    sub_id = 2
    name = 'Rituals'


class CharmSet(WordSet):

    def __init__(self, owner, root, id, name):
        self.category_id = owner.category_id
        self.sub_id = id
        self.name = name
        super(CharmSet, self).__init__(owner, root)


class CharmManager(SubManager):
    can_add = False
    use = CharmSet
    category_id = 100
    choice_init = {}
    extra_init = {}

    def load(self):
        choices = dict()
        choices.update(self.choice_init)
        choices.update(self.extra_init)
        self.subs = list()
        for k, v in choices.iteritems():
            new_charms = self.use(self, self.root, k, v)
            self.subs.append(new_charms)
        self.subs_dict = {cha.id: cha for cha in self.subs}
        self.subs_name = {cha.name: cha for cha in self.subs}


class Sorcery(CharmManager):
    name = 'Sorcery'
    category_id = 101
    choice_init = {1: 'Terrestrial', 2: 'Celestial', 3: 'Solar'}


class Necromancy(CharmManager):
    name = 'Necromancy'
    category_id = 102
    choice_init = {1: 'Shadowlands', 2: 'Labyrinth', 3: 'Void'}

