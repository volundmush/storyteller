from __future__ import unicode_literals
from storyteller.base.customs import CustomSet, CustomStat, CharacterCustomStat

# Merit Data
class CharacterMerit(CharacterCustomStat):
    specialty = None

    def load(self):
        self.context = str(self.model.context)


class Merit(CustomStat):
    specialty = None
    use = CharacterMerit


class MeritSet(CustomSet):
    use = Merit
    category_id = 100