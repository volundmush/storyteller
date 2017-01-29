from __future__ import unicode_literals


class StatHandler(object):
    """
    Object responsible for storing, sorting, readying and managing the Stats (Abilities, Attributes, Advantages,
    etc). Component of StorytellerHandler.
    """

    def __init__(self, owner):
        """
        Construct the StatHandler. Load all stats and prepare lists and dictionaries for referencing.

        :param owner: An Instance of StorytellerHandler.
        """
        self.owner = owner
        self.handler = owner
        self.data = owner.data
        self.game = owner.game
        self.owner.persona.stats.all().exclude(id__in=self.data.stats_dict.keys()).delete()
        stats = self.owner.persona.stats.all()
        if not stats or len(self.data.stats) != stats.count():
            self.load_defaults()
            stats = self.owner.persona.stats.all()
        all_stats = list()
        for row in stats:
            proto = self.data.stats_dict[row.stat_id]
            new_stat = proto.use(self, proto, row)
            all_stats.append(new_stat)
        self.stats = sorted(all_stats, key=lambda stat: stat.list_order)
        self.stats_name = {stat.name: stat for stat in self.stats}
        self.stats_dict = {stat.id: stat for stat in self.stats}

        # Call hook for specific game stuff.
        self.load_extra()

    @property
    def attributes(self):
        return [stat for stat in self.stats if stat.category == 'Attribute']

    @property
    def physical_attributes(self):
        return [stat for stat in self.attributes if stat.sub_category == 'Physical']

    @property
    def social_attributes(self):
        return [stat for stat in self.attributes if stat.sub_category == 'Social']

    @property
    def mental_attributes(self):
        return [stat for stat in self.attributes if stat.sub_category == 'Mental']

    def load_defaults(self):
        """
        This is called only if there is NO saved data for the character. It loads some default data for Attributes,
        Essence, Willpower, etc, using the .default properties of the Stats from GAME_DATA.

        :return:
        """
        stat_ids = set(self.data.stats_dict.keys())
        char_ids = set(self.owner.persona.stats.all().values_list('stat_id', flat=True))
        not_have = stat_ids.difference(char_ids)

        for id in not_have:
            stat = self.data.stats_dict[id]
            new = self.owner.persona.stats.create(stat_id=stat.id, rating=stat.default)

    def load_extra(self):
        """
        This method is meant to be overloaded for running additional initializations per-game.
        :return:
        """
        pass


class StorytellerHandler(object):
    """
    An instance of Storyteller is loaded onto every Character who'll be doing Storyteller stuff. This is the primary
    interface for all commands and database functions.
    """
    data = None
    stat_handler = StatHandler

    def __init__(self, owner):
        self.owner = owner
        self.game = self.data.game

        for prep in (self.prepare_template, self.prepare_stats):
            prep()

    def prepare_template(self):
        pers = self.game.personas.filter(character=self.owner).first()
        if not pers:
            pers = self.game.personas.create(character=self.owner, key=self.owner.key)
        self.persona = pers
        tem = self.data.templates_dict[pers.template]
        self.template = tem.use(self, tem, pers)

    def prepare_stats(self):
        self.stats = self.stat_handler(self)