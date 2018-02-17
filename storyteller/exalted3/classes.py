from evennia.utils import lazy_property

from storyteller.classes import StorytellerCharacter
from storyteller.exalted3.handler import Ex3Handler


class Ex3Character(StorytellerCharacter):

    @lazy_property
    def story(self):
        return Ex3Handler(self)