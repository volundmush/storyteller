from __future__ import unicode_literals


class StatHandler(object):
    owner = None

    def __init__(self, owner):
        self.owner = owner
        self.persona = owner.persona
        self.stats_list = [stat(self.owner) for stat in self.owner.template.stat_list + self.owner.template.extra_stats]
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
        self.skills = dict()
        for category in ['Physical', 'Social', 'Mental']:
            self.attributes[category] = sorted([stat for stat in self.category.get('Skill',())
                                                if stat.sub_category == category], key=lambda stat: stat.list_order)

    def save(self):
        for stat in self.stats_list:
            stat.save()


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
            new_merit = self.owner.merit_map[saved.merit_id](self.owner, entry)
            self.merits_list.append(new_merit)
            self.merits_dict.get(new_merit.category, list()).append(new_merit)


    def save(self):
        for merit in self.merits_list:
            merit.save()


class StorytellerHandler(object):
    owner = None
    template = None
    stats = None
    persona = None
    merits = None
    game = None
    pool_map = None
    template_map = None
    merit_map = None
    game_id = 0

    def __init__(self, owner):
        self.owner = owner
        self.load()

    def load(self):
        persona = None
        last_persona = self.owner.db.persona
        if last_persona:
            found_persona = self.owner.personas.filter(game_id=self.game_id, id=last_persona).first()
            if not found_persona:
                persona = None
            else:
                persona = found_persona
        if not persona:
            self.persona, created = self.owner.personas.get_or_create(key=self.owner.key, game_id=self.game_id)
            self.owner.db.persona = self.persona.id
        else:
            self.persona = persona
        self.template = self.template_map[self.persona.template](self)
        self.stats = StatHandler(self)
        #self.merits = MeritHandler(self)
        self.pools = PoolHandler(self)

    def save(self):
        self.template.save()
        self.persona.save()
        self.stats.save()
        #self.merits.save()
        self.pools.save()

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.owner)