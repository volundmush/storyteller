from __future__ import unicode_literals
from storyteller.base import Pool, WillpowerPool

class Willpower(WillpowerPool):
    id = 1

    @property
    def max(self):
        return int(self.owner.stats.stats_dict['Composure']) + int(self.owner.stats.stats_dict['Resolve'])

class PowerPool(Pool):
    pass

    @property
    def max(self):
        power_dict = {1: 10, 2: 11, 3: 12, 4: 13, 5: 15, 6: 20, 7: 25, 8: 30, 9: 50, 10: 75}
        return power_dict.get(self.power, 0)


class Mana(PowerPool):
    id = 4
    key = 'Mana'
    display_name = 'Mana'
    power = 'Gnosis'


class Vitae(PowerPool):
    id = 2
    key = 'Vitae'
    display_name = 'Vitae'
    power = 'Blood Potency'