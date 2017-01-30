from __future__ import unicode_literals

from storyteller.base.pools import Pool, ReversePool, WillpowerPool, CharacterPool

# Pools


class Limit(Pool):
    id = 2
    name = 'Limit'


class SolarPersonal(Pool):
    id = 3
    name = 'Personal'


class SolarPeripheral(Pool):
    id = 4
    name = 'Peripheral'

MORTAL_POOLS = (WillpowerPool,)

SOLAR_POOLS = (WillpowerPool, SolarPeripheral, SolarPersonal, Limit)


ALL_POOLS = (WillpowerPool, SolarPersonal, SolarPeripheral, Limit)