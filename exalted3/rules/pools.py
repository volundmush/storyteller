from __future__ import unicode_literals

from evennia.utils import lazy_property
from storyteller.exalted3.models import Pool as PoolModel, PoolCommit

class Commit(object):
    key = '<unknown>'
    amount = 0
    owner = None
    model = None

    def __str__(self):
        return self.key

    def __int__(self):
        return self.amount

    def __init__(self, owner, model):
        self.owner = owner
        self.model = model

    def delete(self):
        self.model.delete()

class Pool(object):
    key = '<unknown>'
    id = 0
    owner = None
    max = 0
    used = 0
    model = None
    spent_multiple = "%s spent %s motes of Personal Essence on: %s"
    spent_singular = '%s spent %s mote of Personal Essence on: %s'
    gain_multiple = '%s gained %s motes of Personal Essence for: %s'
    gain_singular = '%s gained %s mote of Personal Essence for: %s'
    features = ('burn', 'regain', 'commit', 'refresh')
    on_refresh = 1
    category = None
    list_order = 0

    def __init__(self, owner):
        self.owner = owner
        model, created = PoolModel.objects.get_or_create(persona=self.owner.persona, pool_id=self.id)
        self.model = model
        self.load()

    def load(self):
        self.used = int(self.model.spent)
        self.commitments = list()
        for commitment in self.model.commits.all():
            self.commitments.append(Commit(self.owner, commitment))

    def save(self):
        self.model.spent = self.used
        self.model.save(update_fields=['spent'])

    def spend(self, amount, reason=None):
        try:
            amount = int(amount)
        except ValueError:
            raise ValueError("Amounts must be numbers!")
        if amount < 1:
            raise ValueError("Cannot spend nothing or negatives!")
        if amount > self.remaining:
            raise ValueError("You don't have enough to spend!")
        self.used += amount
        if not reason:
            reason = 'No reason given!'
        if amount > 1:
            self.owner.msg(self.spent_multiple % (self.owner.owner, amount, reason))
        else:
            self.owner.msg(self.spent_singular % (self.owner.owner, amount, reason))
        self.save()

    def gain(self, amount, reason=None):
        try:
            amount = int(amount)
        except ValueError:
            raise ValueError("Amounts must be numbers!")
        if amount < 1:
            raise ValueError("Cannot gain nothing or negatives!")
        if amount > self.can_gain:
            amount = self.can_gain
        self.used -= amount
        if amount > 1:
            self.owner.msg(self.gain_multiple % (self.owner.owner, amount, reason))
        else:
            self.owner.msg(self.gain_singular % (self.owner.owner, amount, reason))
        self.save()


    @property
    def remaining(self):
        calc = self.current_max - self.total_commit - self.used
        if calc > 0:
            return 0
        return calc

    @property
    def current_max(self):
        return self.max - self.total_commit

    @property
    def can_gain(self):
        return self.current_max - self.remaining

    @property
    def total_commit(self):
        return sum(self.commitments)

    def refresh(self):
        if self.on_refresh:
            self.refill()
        else:
            self.empty()

    def refill(self):
        self.used = 0
        self.save()

    def empty(self):
        self.used = self.current_max
        self.save()

    @property
    def max(self):
        return 0

    @lazy_property
    def willpower(self):
        return self.owner.stats.stats_dict['Willpower']

    @lazy_property
    def essence(self):
        return self.owner.stats.stats_dict['Essence']

    def __repr__(self):
        return '<%s: %s (%s/%s)>' % (self.category, self.key, self.remaining, self.max)


class Willpower(Pool):
    category = 'Pool'
    key = 'Willpower'
    id = 1
    spent_multiple = "%s spent %s points of Willpower on: %s"
    spent_singular = '%s spent %s point of Willpower on: %s'
    gain_multiple = '%s gained %s points of Willpower for: %s'
    gain_singular = '%s gained %s point of Willpower for: %s'
    features = ('burn', 'regain', 'refresh')
    list_order = 10

    @property
    def max(self):
        return int(self.willpower)


class Limit(Pool):
    category = 'Track'
    key = 'Limit'
    id = 2
    spent_multiple = "%s spent %s points of Limit on: %s"
    spent_singular = '%s spent %s point of Limit on: %s'
    gain_multiple = '%s gained %s points of Limit for: %s'
    gain_singular = '%s gained %s point of Limit for: %s'
    features = ('burn', 'regain')
    on_refresh = 0
    max = 10

class EssencePool(Pool):
    category = 'Pool'

class PersonalEssence(EssencePool):
    key = 'Personal'
    id = 3
    list_order = 1

    @property
    def max(self):
        return int(self.essence)*3 + 10


class PeripheralEssence(EssencePool):
    key = 'Peripheral'
    id = 4
    spent_multiple = "%s spent %s motes of Peripheral Essence on: %s"
    spent_singular = '%s spent %s mote of Peripheral Essence on: %s'
    gain_multiple = '%s gained %s motes of Peripheral Essence for: %s'
    gain_singular = '%s gained %s mote of Peripheral Essence for: %s'
    list_order = 3

    @property
    def max(self):
        return int(self.essence)*7 + 26

# Mortal
class MortalWillpower(Willpower):
    pass


MORTAL_POOLS = [MortalWillpower]

# Solar
class SolarWillpower(Willpower):
    pass


class SolarLimit(Limit):
    pass


class SolarPersonal(PersonalEssence):
    pass


class SolarPeripheral(PeripheralEssence):
    pass

SOLAR_POOLS = [SolarWillpower, SolarLimit, SolarPeripheral, SolarPeripheral]

# Solar
class AbyssalWillpower(Willpower):
    pass


class AbyssalLimit(Limit):
    pass


class AbyssalPersonal(PersonalEssence):
    pass


class AbyssalPeripheral(PeripheralEssence):
    pass


ABYSSAL_POOLS = [AbyssalWillpower, AbyssalLimit, AbyssalPeripheral, AbyssalPeripheral]

# Terrestrial
class TerrestrialWillpower(Willpower):
    pass


class TerrestrialLimit(Limit):
    pass


class TerrestrialPersonal(PersonalEssence):

    @property
    def max(self):
        return int(self.essence) + 11


class TerrestrialPeripheral(PeripheralEssence):

    @property
    def max(self):
        return int(self.essence)*4 + 23

TERRESTRIAL_POOLS = [TerrestrialWillpower, TerrestrialLimit, TerrestrialPersonal, TerrestrialPeripheral]

__all__ = ['SOLAR_POOLS', 'MORTAL_POOLS', 'ABYSSAL_POOLS', 'TERRESTRIAL_POOLS']