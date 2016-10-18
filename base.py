from __future__ import unicode_literals
from evennia.utils import lazy_property


class Stat(object):
    key = '<unknown>'
    id = 0
    category = None
    sub_category = None
    default = 0
    can_roll = True
    can_purchase = True
    can_specialize = False
    list_order = 0
    value_storage = None
    loaded = False
    model = None

    def __str__(self):
        return self.key

    def __int__(self):
        return self.value

    def __repr__(self):
        return '<%s: %s (%s)>' % (self.category, self.key, self.value)

    def __init__(self, owner):
        self.owner = owner

    def load(self):
        self.loaded = True
        self.model, created = self.owner.persona.stats.get_or_create(stat_id=self.id)
        if created:
            self.value_storage = self.default
        else:
            self.value_storage = self.model.rating

    def save(self):
        if not self.loaded:
            self.load()
        self.model.rating = self.value_storage
        self.model.save(update_fields=['rating'])

    @property
    def value(self):
        if not self.loaded:
            self.load()
        return self.value_storage


class Attribute(Stat):
    category = 'Attribute'
    default = 1


class PhysicalAttribute(Attribute):
    sub_category = 'Physical'


class SocialAttribute(Attribute):
    sub_category = 'Social'


class MentalAttribute(Attribute):
    sub_category = 'Mental'


class Skill(Stat):
    category = 'Skill'
    default = 0
    can_specialize = True


class PhysicalSkill(Skill):
    sub_category = 'Physical'


class SocialSkill(Skill):
    sub_category = 'Social'


class MentalSkill(Skill):
    sub_category = 'Mental'


class Advantage(Stat):
    category = 'Advantage'


class PowerStat(Advantage):
    id = 1
    key = 'PowerStat'
    default = 1


class Willpower(Advantage):
    id = 2
    key = 'Willpower'


class Splat(object):
    owner = None
    key = '<Unknown'
    id = 0
    display = 'Splat'

    def __str__(self):
        return self.key

    def __int__(self):
        return self.id

    def __init__(self, owner):
        self.owner = owner


class Template(object):
    owner = None
    key = '<Unknown>'
    id = 0
    x_splat = None
    y_splat = None
    z_splat = None
    x_choices = ()
    y_choices = ()
    z_choices = ()
    x_default = None
    y_default = None
    z_default = None
    x_name = None
    y_name = None
    z_name = None
    pool_list = ()
    extra_pools = ()
    willpower = 1
    stat_list = ()
    extra_stats = ()

    def __str__(self):
        return self.key

    def __int__(self):
        return self.id

    def __repr__(self):
        return '<Template: %s>' % self.key

    def __init__(self, owner):
        self.owner = owner
        self.pools = list()
        persona = self.owner.persona
        for splat_type in ['x', 'y', 'z']:
            splats = getattr(self, '%s_choices' % splat_type)
            if not splats:
                continue
            splat_id = getattr(persona, '%s_splat' % splat_type)
            if not splat_id:
                default = getattr(self, '%s_default')
                if not default:
                    continue
                else:
                    splat_id = default
            splat_class = splats.get(splat_id, None)
            if not splat_class:
                continue
            setattr(self, '%s_splat', splat_class(self))

    def save(self):
        persona = self.owner.persona
        if self.x_splat:
            persona.x_splat = self.x_splat.id
        if self.y_splat:
            persona.y_splat = self.y_splat.id
        if self.z_splat:
            persona.z_splat = self.z_splat.id
        persona.save(update_fields=['x_splat', 'y_splat', 'z_splat'])


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
    unit_singular = 'point'
    unit_plural = 'points'
    display_name = 'Pool'
    features = ('burn', 'regain', 'commit', 'refresh')
    on_refresh = 1
    category = None
    list_order = 0
    power = 'Essence'

    def __init__(self, owner):
        self.owner = owner
        self.model, created = owner.persona.pools.get_or_create(pool_id=self.id)
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
        display = self.display(amount, reason, mode='spent')
        self.owner.msg(display)
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
        display = self.display(amount, reason, mode='gained')
        self.owner.msg(display)
        self.save()

    def display(self, amount, reason=None, mode='gained'):
        if not reason:
            reason = 'No reason given!'
        if amount > 1:
            units = self.unit_plural
        else:
            units = self.unit_singular
        return '%s %s %s %s of %s for: %s' % (self.owner.owner, mode, amount, units, self.display_name, reason)

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

    def __repr__(self):
        return '<%s: %s (%s/%s)>' % (self.category, self.key, self.remaining, self.max)

    @lazy_property
    def willpower(self):
        return self.owner.stats.stats_dict['Willpower']

    @lazy_property
    def power(self):
        return self.owner.stats.stats_dict[self.power]


class WillpowerPool(Pool):
    category = 'Pool'
    key = 'Willpower'
    id = 1
    unit_singular = 'point'
    unit_plural = 'points'
    display_name = 'Willpower'
    features = ('burn', 'regain', 'refresh')
    list_order = 10

    @property
    def max(self):
        return int(self.willpower)