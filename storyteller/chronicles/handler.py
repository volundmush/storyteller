from __future__ import unicode_literals
from storyteller.handler import StorytellerHandler
from storyteller.chronicles.templates import TEMPLATE_MAP


class ChroniclesHandler(StorytellerHandler):
    merit_map = None
    game_id = 1
    persona_stor = 'chronicles_persona'
    template_map = TEMPLATE_MAP