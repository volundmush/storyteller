from athanor.utils.text import dramatic_capitalize, sanitize_string


class CharacterPower(object):

    def __init__(self, owner, stat, model):
        self.owner = owner
        self.handler = owner.handler
        self.data = self.handler.data
        self.model = model
        self.stat = stat
        self.rating = int(model.rating)
        self.load()

    def __str__(self):
        return self.name

    def __int__(self):
        return self.rating

    def __repr__(self):
        return '<%s %s: %s>' % (self.name, self.category, self.rating)

    @property
    def category(self):
        return self.stat.category

    @property
    def sub_category(self):
        return self.stat.sub_category

    @property
    def name(self):
        return self.stat.name

    @property
    def id(self):
        return self.stat.id

    @property
    def list_order(self):
        return self.stat.list_order

    def load(self):
        pass

    def save(self):
        self.model.rating = self.rating
        self.model.save(update_fields=['rating'])

    def set(self, value=None):
        if not value:
            raise ValueError("No value entered!")
        try:
            val = int(value)
        except ValueError:
            raise ValueError("Must enter a number.")
        if val < self.stat.lowest or val > self.stat.highest:
            raise ValueError("Stat must be between %s and %s!" % (self.stat.lowest, self.stat.highest))
        old = self.rating
        self.rating = val
        if old != val:
            self.save()
        return "%s Set to: %s" % (self.name, val)

    @property
    def display_name(self):
        return self.name


class Power(object):
    id = 0
    category = '<unknown>'
    sub_category = '<unknown>'
    name = '<unknown>'
    tags = tuple()
    default = 0
    can_roll = False
    list_order = 0
    use = CharacterPower
    lowest = 0
    highest = 10

    def __str__(self):
        return self.name

    def __int__(self):
        return self.id

    def __repr__(self):
        return '<%s: (%s) %s>' % (self.category, self.id, self.name)

    def __init__(self, data):
        self.data = data
        self.game = data.game

    def qualify(self, checker):
        """
        This Method will be called on all Stats in a game to decide which ones players should load. It is meant to be
        overloaded depending on the stat. For instance, Vampire Disciplines (World of Darkness) should return true if
        checker is a vampire OR a Ghoul. The base Stat returns true for everyone.

        Args:
            checker: a StorytellerHandler instance.

        Returns:
            Bool - Whether checker qualifies for this Stat.

        """
        return True