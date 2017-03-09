from __future__ import unicode_literals

from athanor.utils.text import partial_match

class Handler(object):
    """
    Not meant to be used directly. Parent Class for all StorytellerHandler Sections!
    """
    name = 'Handler'
    can_set = True
    can_add = True
    can_remove = True
    can_create = True
    can_clear = True


    def __init__(self, owner):
        self.owner = owner
        self.character = owner.character
        self.persona = owner.persona
        self.handler = owner
        self.data = owner.data
        self.game = owner.game
        self.load()
        self.load_extra()

    def load(self):
        """
        Meant to be overloaded for each Handler.
        :return:
        """
        pass

    def load_extra(self):
        """
        A second overloadable so you don't have to super() if you inherit from the existing Handlers for things.
        :return:
        """
        pass

    def __str__(self):
        return self.name

    def menu_display(self, viewer):
        pass


class TemplateHandler(Handler):
    name = 'Template'
    can_add = False
    can_remove = False
    can_create = False

    def __init__(self, owner):
        self.owner = owner
        self.character = owner.character
        self.handler = owner
        self.data = owner.data
        self.game = self.data.game
        pers = self.game.personas.filter(character=self.character).first()
        if not pers:
            pers = self.game.personas.create(character=self.character, key=self.character.key)
        self.persona = pers
        self.owner.persona = pers
        tem = self.data.templates_dict[pers.template]
        self.template = tem.use(self, tem, pers)
        self.load()
        self.load_extra()

    def set(self, name=None, value=None):
        options = {'Template': self.set_template}
        if not name:
            raise ValueError("What will you set?")
        found = partial_match(name, options.keys())
        if found:
            return options[found](value)
        return self.template.set(name, value)

    def set_template(self, value=None):
        choices = self.data.templates
        if not value:
            raise ValueError("What Template will you use? Choices are: %s" % ', '.join([str(tem) for tem in choices]))
        tem = partial_match(value, choices)
        if not tem:
            raise ValueError("Template not found. Choices are: %s" % ', '.join([str(tem) for tem in choices]))
        self.persona.template = tem.id
        self.persona.save(update_fields=['template'])
        self.template = tem.use(self, tem, self.persona)
        return "Template Changed to: %s" % tem

    def menu_display(self, viewer):
        message = list()
        message.append(viewer.player.render.header('%s - Sheet Template' % (self.character.key)))
        start_table = viewer.player.render.make_table(['Options', 'Choices'], width=[24, 56])
        start_table.add_row('Template', ', '.join([str(tem) for tem in self.data.templates]))
        for op in self.template.options:
            start_table.add_row(op[0], op[1])
        message.append(start_table)
        message.append(viewer.player.render.separator('Commands'))
        mode_table = viewer.player.render.make_table(['Cmd', 'Explanation'], width=[24, 56])
        cmds = (
            ('mode <type>', "Change current editing mode!"),
            ('set <option>=<value>', "Change an above property. Example: set Template=Mortal"),
            ('sheet', 'Display current progress'),
            ('menu', "Display this help menu."),
            ('finish', "Leave editor.")
        )
        for cmd in cmds:
            mode_table.add_row(cmd[0], cmd[1])
        message.append(mode_table)
        message.append(viewer.player.render.footer())
        return message

class StatHandler(Handler):
    """
    Object responsible for storing, sorting, readying and managing the Stats (Abilities, Attributes, Advantages,
    etc). Component of StorytellerHandler.
    """
    name = 'Stats'
    can_create = False
    can_clear = False

    def load(self):
        self.owner.persona.stats.all().exclude(id__in=self.data.stats_dict.keys()).delete()
        stats = self.owner.persona.stats.all()
        if not stats or len(self.data.stats) != stats.count():
            self.load_defaults()
            stats = self.owner.persona.stats.all()
        all_stats = list()
        self.specialties = list()
        self.roll = list()
        for row in stats:
            proto = self.data.stats_dict[row.stat_id]
            new_stat = proto.use(self, proto, row)
            all_stats.append(new_stat)
        self.stats = sorted(all_stats, key=lambda stat: stat.list_order)
        self.stats_name = {stat.name: stat for stat in self.stats}
        self.stats_dict = {stat.id: stat for stat in self.stats}

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

    def set(self, name=None, value=None):
        choices = self.stats
        choice_names = ', '.join([str(ch) for ch in choices])
        if not name:
            raise ValueError("What will you set? Choices are: %s" % choice_names)
        found = partial_match(name, choices)
        if not found:
            raise ValueError("Stat not found! Choices are: %s" % choice_names)
        return found.set(value)

    def menu_display(self, viewer):
        message = list()
        message.append(viewer.player.render.header('%s - Sheet Stats' % (self.character.key)))
        start_table = viewer.player.render.make_table(['Options', 'Choices'], width=[24, 56])
        start_table.add_row('Stats', ', '.join([str(stat) for stat in self.data.stats]))
        message.append(start_table)
        message.append(viewer.player.render.separator('Commands'))
        mode_table = viewer.player.render.make_table(['Cmd', 'Explanation'], width=[24, 56])
        cmds = (
            ('mode <type>', "Change current editing mode!"),
            ('set <stat>=<value>', "Change an above property. Example: set Strength=3"),
            ('sheet', 'Display current progress'),
            ('menu', "Display this help menu."),
            ('finish', "Leave editor.")
        )
        for cmd in cmds:
            mode_table.add_row(cmd[0], cmd[1])
        message.append(mode_table)
        message.append(viewer.player.render.footer())
        return message

class SheetHandler(Handler):
    """
    Object responsible for manging Sheet Output.
    """
    def load(self):
        self.sections = sorted([sec(self) for sec in self.data.load_sheet], key=lambda ord: ord.list_order)

    def render(self, width=80):
        message = list()
        for sec in [sec for sec in self.sections if sec.display]:
            rendered = sec.render(width=width)
            if rendered:
                message.append(rendered)
        return '\n'.join(message)


class PoolHandler(Handler):
    """
    Object responsible for manging Pools.
    """
    pass


class ExtraHandler(Handler):

    def load(self):
        self.extras = [ex.use(self, ex, root=self) for ex in self.data.extras]
        self.extras_dict = {ex.id: ex for ex in self.extras}
        self.extras_name = {ex.name: ex for ex in self.extras}


class StorytellerHandler(object):
    """
    An instance of Storyteller is loaded onto every Character who'll be doing Storyteller stuff. This is the primary
    interface for all commands and database functions.
    """
    data = None
    template_handler = TemplateHandler
    stat_handler = StatHandler
    sheet_handler = SheetHandler
    pool_handler = PoolHandler
    extra_handler = ExtraHandler

    def __init__(self, owner):
        self.owner = owner
        self.character = owner
        self.game = self.data.game

        for prep in (self.prepare_template, self.prepare_stats, self.prepare_sheet, self.prepare_extras,
                     self.prepare_pools):
            prep()

    def prepare_template(self):
        self.template = self.template_handler(self)

    def prepare_stats(self):
        self.stats = self.stat_handler(self)

    def prepare_sheet(self):
        self.sheet = self.sheet_handler(self)

    def prepare_pools(self):
        self.pools = self.pool_handler(self)

    def prepare_extras(self):
        self.extras = self.extra_handler(self)