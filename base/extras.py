from __future__ import unicode_literals
from athanor.utils.text import dramatic_capitalize, sanitize_string


class CharacterExtraSet(object):
    add_increases_quantity = False
    set_is_add = False
    on_zero_remove = False

    def __init__(self, owner, extra, root=None, parent=None):
        self.character = owner.character
        self.persona = owner.persona
        self.owner = owner
        self.game = owner.game
        self.data = owner.data
        self.handler = owner.handler
        self.root = root
        self.parent = parent
        self.extra = extra
        self.subs = list()
        self.subs_name = dict()
        self.subs_dict = dict()
        self.stats = list()
        self.stats_dict = dict()
        self.stats_name = dict()

        if self.extra.use_stats:
            self.load_stats()

        if self.extra.use_subs:
            self.load_subs()

        self.extra.users.append(self)

    def __repr__(self):
        if self.parent:
            return '<%s: %s>' % (self.parent.name, self.name)
        return '<Extras: %s>' % (self.name)

    def __str__(self):
        return self.name

    def __int__(self):
        return self.id

    @property
    def name(self):
        return self.extra.name

    @property
    def id(self):
        return self.extra.id

    def load_stats(self):
        for row in self.persona.extras.filter(stat__category=self.extra.model).order_by('stat__key'):
            ext = self.extra.stats_dict[row.stat.id]
            new_stat = self.extra.stat.use(self, ext, row)
            self.stats.append(new_stat)
            self.stats_dict[ext.id] = new_stat
            self.stats_dict[ext.name] = new_stat

    def load_subs(self):
        for sub in self.extra.subs:
            new_sub = self.extra.use(self, sub, root=self.root, parent=self)
            self.subs.append(new_sub)
            self.subs_dict[new_sub.id] = new_sub
            self.subs_name[new_sub.name] = new_sub

    def extend(self, name=None):
        return self.extra.extend(creator=self.character, name=name)

    def create(self, name=None):
        return self.extra.create(creator=self.character, name=name)

    def add(self, name=None, value=None):
        pass

    def set(self, name=None, value=None):
        pass

    def remove(self, name=None, value=None):
        pass

    def clear(self, name=None, value=None):
        pass

    def delete(self):
        """
        This is called by a parent ExtraSet in some circumstances. Purges all child character data through calling
        nested .delete() functions on contained objects.
        :return:
        """
        for id in self.stats_dict.keys():
            self.delete_stat(id)
        for id in self.subs_dict.keys():
            self.delete_sub(id)

    def delete_sub(self, id):
        """
        Delete a sub-ExtraCharacterSet and everything it manages from the database.
        :param id:
        :return:
        """
        sub = self.subs_dict[id]
        if sub:
            sub.delete()
            self.subs.remove(sub)
            del self.subs_dict[id]

    def delete_stat(self, id):
        """
        Delete a character's Stat and any Specialties (if they have any) by calling its .delete() function.
        :param id:
        :return:
        """
        stat = self.stats_dict[id]
        if stat:
            stat.delete()
            self.stats.remove(stat)
            del self.stats_dict[id]


class CharacterExtra(object):

    def __init__(self, owner, extra, row):
        self.owner = owner
        self.handler = owner.handler
        self.extra = extra
        self.game = owner.game
        self.data = owner.data
        self.model = row
        self.extra.users.append(self)
        self.load()

    def load(self):
        pass

    def __str__(self):
        return self.name

    def name(self):
        return self.extra.name

    def delete(self):
        """
        Hook called by any deletion from the ExtraSet subsystem. Ensures operation mirrored in CharacterExtras.
        :return:
        """
        self.delete_extra()
        self.model.delete()

    def delete_extra(self):
        """
        Hook attribute to be called before primary deletion. Used mostly for Specialties.
        :return:
        """
        pass


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
        self.users = list()
        self.load()

    def load(self):
        pass

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<%s: %s>' % (self.owner.name, self.name)

    def delete(self):
        """
        Calls the .delete() function on all player instances and cleans up the stat's Model. This is meant to be
        called from the ExtraSet via its .delete_stat() method.
        :return:
        """
        for user in self.users:
            user.delete()
        self.model.delete()


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
    name = '<unknown>'
    can_create = True
    can_take = True
    can_extend = False
    use = CharacterExtraSet
    stat = ExtraStat
    sub = None
    use_subs = False
    use_stats = True
    created = False
    sub_init = tuple()
    stat_init = tuple()

    def __repr__(self):
        if not self.parent:
            return '<%s: %s>' % (self.__class__.__name__, self.name)
        return '<%s - %s>' % (self.owner.name, self.name)

    def __init__(self, owner, root=None, model=None, name=None, parent=None):
        self.users = list()
        self.owner = owner
        self.parent = parent
        if name:
            self.name = name
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
            self.parent = model.parent
            self.name = str(model.key)
        else:
            self.model, self.created = self.game.extras.get_or_create(parent=parent, key=self.name)
        self.id = int(self.model.id)
        self.subs = list()
        self.subs_dict = dict()
        self.stats = list()
        self.stats_dict = dict()
        self.stats_name = dict()

        if self.created:
            self.load_init()

        if self.use_stats:
            self.load_stats()

        if self.use_subs:
            self.load_subs()

    def load_stats(self):
        self.stats = [self.stat(self, row) for row in self.model.entries.all()]
        self.stats_dict = {ent.id: ent for ent in self.stats}
        self.stats_name = {ent.name: ent for ent in self.stats}

    def load_subs(self):
        rows = self.model.children.all().order_by('key')
        self.subs = [self.sub(self, root=self.root, model=row) for row in rows]
        self.subs_dict = {sub.id: sub for sub in self.subs}
        self.subs_name = {sub.name: sub for sub in self.subs}

    def load_init(self):
        for sub in self.sub_init:
            ent, created = self.model.children.get_or_create(game=self.game, key=sub)
        for thing in self.stat_init:
            th, created = self.model.entries.get_or_create()

    def __str__(self):
        return self.name

    def create(self, creator, name=None):
        if not self.can_create:
            raise ValueError("Cannot add entries to %s!" % self.name)
        if not name:
            raise ValueError("No name entered!")
        name = dramatic_capitalize(sanitize_string(name))
        if self.model.entries.filter(key__iexact=name).count():
            raise ValueError("Name is already in use!")
        new_mod = self.model.entries.create(creator=creator, key=name)
        new_stat = self.stat(self, new_mod)
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
        new_mod = self.model.children.create(game=self.game, key=name)
        new_sub = self.sub(self, root=self.root, model=new_mod)
        self.subs.append(new_sub)
        self.subs_dict[new_sub.sub_id] = new_sub
        self.subs_name[name] = new_sub
        return new_sub

    def delete(self):
        """
        Used to delete an ExtraSet from the database including all player data. Intended to be called from a
        parent ExtraSet.
        :return:
        """
        for user in self.users:
            user.delete()
        for id in self.stats_dict.keys():
            self.delete_stat(id)
        for id in self.subs_dict.keys():
            self.delete_sub(id)
        self.model.delete()

    def delete_sub(self, id):
        """
        Deletes a whole sub-ExtraSet and removes it and everything it contains from the database and players.
        :return:
        """
        sub = self.subs_dict[id]
        if sub:
            sub.delete()
            del self.subs_dict[id]
            self.subs.remove(sub)

    def delete_stat(self, id):
        """
        Deletes a Stat's Model and removes it from the ExtraSet. This propogates to all Character instances and
        the database so be careful!
        :param id:
        :return:
        """
        stat = self.stats_dict[id]
        if stat:
            stat.delete()
            del self.stats_dict[id]
            self.stats.remove(stat)

class MutableSet(ExtraSet):
    can_create = True


class MeritSet(MutableSet):
    category_id = 1
    sub_id = 0
    name = 'Merits'
    stat = ExtraMerit


class SubManager(ExtraSet):
    can_create = False
    use_subs = True
    can_take = False
    use_stats = False


class WordSet(ExtraSet):
    category_id = 3
    name = 'Words'
    stat = WordPower
