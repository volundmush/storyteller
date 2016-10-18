from evennia.utils import lazy_property

from storyteller.classes import StorytellerCharacter
from storyteller.handler import Ex3Handler


class Ex3Character(StorytellerCharacter):

    @lazy_property
    def ex3(self):
        return Ex3Handler(self)