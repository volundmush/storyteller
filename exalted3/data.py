from __future__ import unicode_literals
from storyteller.exalted3.stats import ALL_STATS
from storyteller.exalted3.customs import ALL_CUSTOMS
from storyteller.exalted3.pools import ALL_POOLS
from storyteller.exalted3.splats import ALL_SPLATS
from storyteller.exalted3.templates import ALL_TEMPLATES
from storyteller.exalted3.sheet import ALL_SHEET

from storyteller.base.data import GameData


class ExData(GameData):
    load_stats = ALL_STATS
    load_custom = ALL_CUSTOMS
    load_pools = ALL_POOLS
    load_templates = ALL_TEMPLATES
    load_x = ALL_SPLATS
    load_sheet = ALL_SHEET



GAME_DATA = ExData('Exalted 3e')