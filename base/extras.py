from __future__ import unicode_literals
from athanor.utils.text import dramatic_capitalize, sanitize_string


class CharacterExtra(object):

    def __init__(self, owner, extra, row):
        self.owner = owner
        self.handler = owner.handler
        self.extra = extra
        self.game = owner.game
        self.data = owner.data
        self.model = row
        self.load()

    def load(self):
        pass

    def __str__(self):
        return self.name

    def name(self):
        return self.extra.name


class CharacterExtraStat(CharacterExtra):
    pass


class CharacterExtraSpecialty(CharacterExtraStat):
    pass


class CharacterMerit(object):
    pass


class CharacterWordPower(CharacterExtra):
    pass


class Extra(object):
    use = CharacterExtra

    def __init__(self, owner, row):
        self.owner = owner
        self.handler = owner.handler
        self.data = owner.data
        self.game = owner.game
        self.model = row
        self.name = str(row.key)
        self.id = int(row.id)
        self.load()

    def load(self):
        pass


class ExtraSpecialty(Extra):
    use = CharacterExtraSpecialty


class CharacterExtraStat(Extra):

    def load(self):
        self.rating = int(self.model.rating)


class ExtraMerit(Extra):
    use = CharacterMerit


class ExtraStat(Extra):
    use = CharacterExtraStat
    specialty = ExtraSpecialty
    lowest = 0
    highest = 10


class WordPower(Extra):
    pass


class ExtraSet(object):
    category_id = 0
    sub_id = 0
    name = '<unknown>'
    can_add = True
    can_take = True
    can_extend = False
    sub_classes = ()
    static_classes = ()
    use = ExtraStat
    sub = None
    use_subs = False
    use_stats = True

    def __init__(self, owner, root=None, model=None, sub_id=None, name=None):
        self.owner = owner
        if not root:
            self.root = self
            self.data = owner
            self.game = owner.game
            self.handler = owner
        else:
            self.root = root
            self.data = owner.data
            self.game = owner.game
            self.handler = owner.handler
        if model:
            self.model = model
            self.sub_id = int(model.sub_id)
            self.name = str(model.key)
        else:
            self.model, created = self.game.extras.get_or_create(category_id=self.category_id,
                                                                 sub_id=self.sub_id, key=self.name)
        if name:
            self.name = name
        if sub_id:
            self.sub_id = sub_id
        self.subs = list()
        self.subs_dict = dict()
        self.stats = list()
        self.stats_dict = dict()
        self.stats_name = dict()

        if self.use_stats:
            self.load_stats()

        if self.use_subs:
            self.load_subs()

    def load_stats(self):
        self.stats = [self.use(self, row) for row in self.model.entries.all()]
        self.stats_dict = {ent.id: ent for ent in self.stats}
        self.stats_name = {ent.name: ent for ent in self.stats}

    def load_subs(self):
        rows = self.model.__class__.objects.filter(category_id=self.category_id)
        self.subs = [self.sub(self, root=self.root, model=row) for row in rows]
        self.subs_dict = {sub.sub_id: sub for sub in self.subs}
        self.subs_name = [self.use(self, row) for row in self.model.entries.all()]

    @property
    def id(self):
        return self.category_id

    def __str__(self):
        return self.name

    def add(self, creator, name=None):
        if not self.can_add:
            raise ValueError("Cannot add entries to %s!" % self.name)
        if not name:
            raise ValueError("No name entered!")
        name = dramatic_capitalize(sanitize_string(name))
        if self.model.entries.filter(key__iexact=name).count():
            raise ValueError("Name is already in use!")
        new_mod = self.model.entries.create(creator=creator, key=name)
        new_stat = self.use(self, new_mod)
        self.stats.append(new_stat)
        self.stats_dict[new_stat.id] = new_stat
        self.stats_name[name] = new_stat
        return new_stat

    def extend(self, name=None):
        if not self.can_extend:
            raise ValueError("Cannot extend %s with new sub-categories." % self.name)
        if not name:
            raise ValueError("No name entered!")
        name = dramatic_capitalize(sanitize_string(name))
        old_ids = self.model.__class__.objects.filter(category_id=self.category_id).values_list('sub_id', flat=True)
        new_id = max(old_ids) + 1
        new_mod = self.model.__class__.objects.create(category_id=self.category_id, sub_id=new_id, key=name)
        new_sub = self.sub(self, root=self.root, model=new_mod)
        self.subs.append(new_sub)
        self.subs_dict[new_sub.sub_id] = new_sub
        self.subs_name[name] = new_sub
        return new_sub



class MutableSet(ExtraSet):
    can_add = True


class MeritSet(MutableSet):
    category_id = 1
    sub_id = 0
    name = 'Merits'
    use = ExtraMerit


class SubManager(ExtraSet):
    can_add = False
    use_subs = True
    can_take = False
    use_stats = False


class StaticSet(ExtraSet):
    category_id = 2
    name = 'Extras'
    can_add = False

    def load_stats(self):
        self.stats = [sta(self) for sta in self.static_classes]
        self.stats_dict = {sta.id: sta for sta in self.stats}
        self.stats_name = {sta.name: sta for sta in self.stats}


class WordSet(ExtraSet):
    category_id = 3
    name = 'Words'
    use = WordPower
