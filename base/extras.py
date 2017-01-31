from __future__ import unicode_literals


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

    def __init__(self, owner, root=None):
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
        self.model, created = self.game.extras.get_or_create(category_id=self.category_id, sub_id=self.sub_id)
        self.subs = list()
        self.subs_dict = dict()
        self.stats = list()
        self.stats_dict = dict()
        self.stats_name = dict()
        self.load()

    def load(self):
        pass

    @property
    def id(self):
        return self.category_id

    def __str__(self):
        return self.name

    def add(self, name=None):
        if not self.can_add:
            raise ValueError("Cannot add entries to %s!" % self.name)


    def extend(self, name=None):
        if not self.can_extend:
            raise ValueError("Cannot extend %s with new sub-categories." % self.name)


class MutableSet(ExtraSet):
    can_add = True

    def load(self):
        self.stats = [self.use(self, row) for row in self.model.entries.all()]
        self.stats_dict = {ent.id: ent for ent in self.stats}
        self.stats_name = {ent.name: ent for ent in self.stats}


class MeritSet(MutableSet):
    category_id = 1
    sub_id = 0
    name = 'Merits'
    use = ExtraMerit


class SubManager(ExtraSet):
    can_add = False
    use_subs = True
    can_take = False

    def load(self):
        self.subs = [cla(self, self.root) for cla in self.sub_classes]
        self.subs_dict = {sub.name: sub for sub in self.subs}
        self.entries = [self.use(self, row) for row in self.model.entries.all()]


class StaticSet(ExtraSet):
    category_id = 2
    name = 'Extras'
    can_add = False

    def load(self):
        self.stats = [sta(self) for sta in self.static_classes]
        self.stats_dict = {sta.id: sta for sta in self.stats}
        self.stats_name = {sta.name: sta for sta in self.stats}


class WordSet(ExtraSet):
    category_id = 3
    name = 'Words'
    use = WordPower
