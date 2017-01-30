from __future__ import unicode_literals
from storyteller.handler import StatHandler, StorytellerHandler
from storyteller.exalted3.data import GAME_DATA


class _Ex3StatHandler(StatHandler):

    @property
    def abilities(self):
        return sorted([stat for stat in self.stats if stat.category == 'Ability'], key=lambda abil: abil.list_order)

    @property
    def essence(self):
        return self.stats_name['Essence']

    @property
    def willpower(self):
        return self.stats_name['Willpower']


class Ex3Handler(StorytellerHandler):
    data = GAME_DATA
    stat_handler = _Ex3StatHandler