from __future__ import unicode_literals

from storyteller.exbase.templates import Mortal as BaseMortal, Solar as BaseSolar
from storyteller.exalted3.pools import SOLAR_POOLS, MORTAL_POOLS


class Mortal(BaseMortal):
    pool_classes = MORTAL_POOLS


class Solar(BaseSolar):
    pool_classes = SOLAR_POOLS


ALL_TEMPLATES = (Mortal, Solar)