from __future__ import unicode_literals
from storyteller.exbase.stats import STAT_BASE, MartialArts as OldMartial, Brawl, CharacterStat


class CharacterMartial(CharacterStat):
    pass


class MartialArts(OldMartial):
    id = 112
    name = 'Martial Arts'
    use = CharacterMartial

BASE_STATS = STAT_BASE + (MartialArts, Brawl)


ALL_STATS = BASE_STATS