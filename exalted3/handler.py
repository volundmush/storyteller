from __future__ import unicode_literals

from storyteller.exalted3.rules.templates import TEMPLATE_MAP, CASTE_MAP
#from storyteller.exalted3.rules.merits import MERIT_MAP
from storyteller.exalted3.models import Stat

class StatHandler(object):
    owner = None

    def __init__(self, owner):
        self.owner = owner
        save_data, created = Stat.objects.get_or_create(persona=self.owner.persona)
        self.save_data = save_data
        self.stats_list = [stat(self.owner, save_data) for stat in self.owner.template.stat_list]
        self.stats_dict = {stat.key: stat for stat in self.stats_list}
        self.stats_id = {stat.id: stat for stat in self.stats_list}
        self.category = dict()
        categories = set([stat.category for stat in self.stats_list])
        for category in categories:
            self.category[category] = sorted([stat for stat in self.stats_list if stat.category == category],
                                             key=lambda stat: stat.list_order)
        self.attributes = dict()
        for category in ['Physical', 'Social', 'Mental']:
            self.attributes[category] = sorted([stat for stat in self.category['Attribute']
                                                if stat.sub_category == category], key=lambda stat: stat.list_order)

    def save(self):
        for stat in self.stats_list:
            stat.save(no_update=True)
        self.save_data.save()


class PoolHandler(object):
    owner = None

    def __init__(self, owner):
        self.owner = owner
        self.pool_list = [pool(self.owner) for pool in self.owner.template.pools]
        self.pool_dict = dict()
        categories = set([pool.category for pool in self.pool_list])
        for category in categories:
            self.pool_dict[category] = sorted([pool for pool in self.pool_list if pool.category == category],
                                              key=lambda pool: pool.list_order)

    def save(self):
        for pool in self.pool_list:
            pool.save()

class MeritHandler(object):
    owner = None

    def __init__(self, owner):
        self.owner = owner
        self.merits_list = list()
        self.merits_dict = dict()
        self.load()


    def load(self):
        saved = self.owner.persona.merits.all()
        for entry in saved:
            new_merit = MERIT_MAP[saved.merit_id](self.owner, entry)
            self.merits_list.append(new_merit)
            self.merits_dict.get(new_merit.category, list()).append(new_merit)


    def save(self):
        for merit in self.merits_list:
            merit.save()


class Ex3Handler(object):
    owner = None
    template = None
    stats = None
    persona = None
    merits = None

    def __init__(self, owner):
        self.owner = owner
        self.load()

    def load(self):
        if self.owner.db.ex3_persona:
            self.persona = self.owner.db.ex3_persona
        else:
            persona, created = self.owner.ex3_personas.get_or_create(key=self.owner.key)
            self.persona = persona
        self.template = TEMPLATE_MAP[self.persona.template](self)
        self.caste = CASTE_MAP[self.persona.caste](self)
        self.stats = StatHandler(self)
        #self.merits = MeritHandler(self)
        self.pools = PoolHandler(self)

    def save(self):
        self.persona.save()
        self.stats.save()
        #self.merits.save()
        self.pools.save()

    def __repr__(self):
        return '<Ex3Handler: %s>' % self.owner