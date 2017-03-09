from __future__ import unicode_literals
from athanor.utils.text import dramatic_capitalize, sanitize_string, partial_match


class CharacterExtraSet(object):

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
        self.confirm_delete = None

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
        choices = self.extra.stats
        if not name:
            raise ValueError("What will you set? Your choices are: %s" % ', '.join(choices))
        stat = partial_match(name, choices)
        if not stat and self.extra.can_create:
            raise ValueError("That stat is not available, but can be created.")
        elif not stat and not self.extra.can_create:
            raise ValueError("That stat is not available. Your choices are: %s" % ', '.join(choices))
        val = stat.validate_set(value)
        my_stat = self.stats_dict.get(stat.id, None)
        if not val and my_stat is None:
            raise ValueError("There's no point in adding a Stat at zero.")
        if not my_stat:
            my_stat = self.add_stat(stat)
        return my_stat.add(val)

    def set(self, name=None, value=None):
        if self.extra.set_is_add:
            return self.add(name, value)
        choices = self.extra.stats
        if not name:
            raise ValueError("What will you set? Your choices are: %s" % ', '.join(choices))
        stat = partial_match(name, choices)
        if not stat and self.extra.can_create:
            raise ValueError("That stat is not available, but can be created.")
        elif not stat and not self.extra.can_create:
            raise ValueError("That stat is not available. Your choices are: %s" % ', '.join(choices))
        val = stat.validate_set(value)
        my_stat = self.stats_dict.get(stat.id, None)
        if not val and my_stat is None:
            raise ValueError("There's no point in adding a Stat at zero.")
        if not my_stat:
            my_stat = self.add_stat(stat)
        if not val and self.extra.set_zero_is_remove:
            if not self.confirm_delete is my_stat and self.extra.confirm_remove:
                self.confirm_delete = my_stat
                return "This will remove %s. To confirm, enter the command again." % my_stat
            message = "Deleted %s." % my_stat
            self.delete_stat(my_stat.id)
            del my_stat
            if self.extra.clear_unused_stats and not stat.model.users.count():
                self.extra.delete_stat(stat.id)
            return message
        return my_stat.set(val)

    def add_stat(self, stat):
        new_mod, created = self.persona.extras.get_or_create(stat=stat.model)
        new_stat = self.extra.stat.use(self, stat, new_mod)
        self.stats.append(new_stat)
        self.stats_dict[stat.id] = new_stat
        self.stats_name[stat.name] = new_stat
        return new_stat


    def remove(self, name=None, value=None):
        choices = self.extra.stats
        if not name:
            raise ValueError("What will you set? Your choices are: %s" % ', '.join(choices))
        stat = partial_match(name, choices)
        if not stat and self.extra.can_create:
            raise ValueError("That stat is not available, but can be created.")
        elif not stat and not self.extra.can_create:
            raise ValueError("That stat is not available. Your choices are: %s" % ', '.join(choices))
        val = stat.validate_set(value)
        my_stat = self.stats_dict.get(stat.id, None)
        if not val and my_stat is None:
            raise ValueError("There's no point in adding a Stat at zero.")
        if not my_stat:
            my_stat = self.add_stat(stat)
        return my_stat.add(val)

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

    @property
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
    can_specialty = False

    def load(self):
        self.rating = int(self.model.rating)

        if self.can_specialty:
            self.load_specialties()

        # For if even normal load is not enough.
        self.load_extra()

    def load_extra(self):
        # Just a hook in case this is needed...
        pass

    def load_specialties(self):
        pass

    def set(self, value=None):
        if value is None:
            raise ValueError("Must enter a value!")
        try:
            val = int(value)
        except ValueError:
            raise ValueError("Must enter a number.")
        if val < 0:
            raise ValueError("A positive whole number.")

        self.rating = val
        self.model.rating = val
        self.model.save(update_fields=['rating'])
        return "%s is now rated at: %s" % (self.name, val)


    def __int__(self):
        return self.rating


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


class ExtraStat(Extra):
    use = CharacterExtraStat
    specialty = ExtraSpecialty
    lowest = 0
    highest = 10

    def validate_set(self, value=None):
        if value is None:
            raise ValueError("You did not enter a value to set it to!")
        try:
            val = int(value)
        except ValueError:
            raise ValueError("You must enter a number value!")
        if val < 0:
            raise ValueError("A stat cannot be set negative...")
        if val < self.lowest or val > self.highest:
            raise ValueError("Must be between %s and %s." % (self.lowest, self.highest))
        return val


class ExtraMerit(Extra):
    use = CharacterMerit



class WordPower(CharacterExtraStat):
    specialty = None


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

    confirm_remove = False
    add_increases_quantity = False
    set_is_add = False
    set_zero_is_remove = False
    clear_unused_stats = False
    can_add = False
    can_set = True
    can_clear = True
    can_remove = True

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
    can_add = False
    can_set = True
    set_zero_is_remove = True
    clear_unused_stats = True


class MeritSet(MutableSet):
    name = 'Merits'
    stat = ExtraMerit


class SubManager(ExtraSet):
    can_create = False
    use_subs = True
    can_take = False
    use_stats = False


class WordSet(ExtraSet):
    name = 'Words'
    stat = WordPower
