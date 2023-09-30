from evennia.utils import lazy_property
from storyteller.characters import StorytellerCharacter as _StorytellerCharacter
from storyteller.handlers import AdvantageHandler, SpecialtyHandler, TemplateHandler, AttributeHandler
from ..handlers import AbilityHandler, StyleHandler, CharmHandler, SpellHandler, EvocationHandler


class Ex3Character(_StorytellerCharacter):

    @lazy_property
    def st_template(self):
        return TemplateHandler(self)

    @lazy_property
    def st_advantages(self):
        return AdvantageHandler(self)

    @lazy_property
    def st_attributes(self):
        return AttributeHandler(self)

    @lazy_property
    def st_abilities(self):
        return AbilityHandler(self)

    @lazy_property
    def st_specialties(self):
        return SpecialtyHandler(self)

    @lazy_property
    def st_styles(self):
        return StyleHandler(self)

    @lazy_property
    def st_charms(self):
        return CharmHandler(self)

    @lazy_property
    def st_spells(self):
        return SpellHandler(self)

    @lazy_property
    def st_evocations(self):
        return EvocationHandler(self)
