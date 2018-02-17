from evennia.utils import lazy_property

from storyteller.classes import StorytellerCharacter
from storyteller.chronicles.handler import ChroniclesHandler

class ChroniclesCharacter(StorytellerCharacter):

    @lazy_property
    def storyteller(self):
        return ChroniclesHandler(self)