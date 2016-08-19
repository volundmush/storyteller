from __future__ import unicode_literals
from commands.library import tabular_table, dramatic_capitalize, partial_match

from world.storyteller.sheet import SheetSection, StatSection, Attributes as OldAttributes, Skills, \
    AdvantageStatSection, AdvantageWordSection, Specialties as OldSpecialties, Favored as OldFavored, \
    TemplateSection as OldTemplate, MeritSection as OldMerit, CustomSection


class TemplateSection(OldTemplate):
    list_order = 0
    pass


class Attributes(OldAttributes):
    list_order = 5
    pass


class Abilities(Skills):
    list_order = 10
    name = 'Abilities'
    kind = 'ability'


class Crafts(CustomSection):
    list_order = 15
    name = 'Crafts'
    kind = 'craft'


class Styles(Crafts):
    list_order = 20
    name = 'Styles'
    kind = 'style'


class Specialties(OldSpecialties):
    list_order = 25


class Favored(OldFavored):
    pass


class Supernal(OldFavored):
    pass


class Merit(OldMerit):
    name = 'Merits'
    list_order = 30


class Flaw(Merit):
    name = 'Flaws'
    kind = 'flaw'
    list_order = 40


class CharmSection(AdvantageWordSection):
    name = 'Charms'
    display_categories = tuple()
    charm_categorized = dict()
    sub_choices = tuple()
    kind = 'charm'
    list_order = 500

    def load(self):
        super(CharmSection, self).load()
        self.display_categories = sorted(list(set(stat.power.category for stat in self.existing)))
        for category in self.display_categories:
            self.charm_categorized[category] = sorted([power for power in self.existing if power.power.category == category],
                                                      key=lambda power2: str(power2))

    def add(self, sub_category, key, amount=1):
        key = dramatic_capitalize(key)
        found_category = partial_match(sub_category, self.sub_choices)
        if not found_category:
            raise ValueError("'%s' is not a valid category for %s. Choices are: %s" % (sub_category, self.name,
                                                                                       ', '.join(self.sub_choices)))
        try:
            amount = int(amount)
        except ValueError:
            raise ValueError("That isn't an integer!")
        if not amount > 0:
            raise ValueError("%s must be raised by positive numbers.")
        find_power = [power for power in self.existing if power.power.category == found_category and power.power.key == key]
        if find_power:
            find_power[0].rating += amount
            find_power[0].save()
            return
        game = self.owner.storyteller.game
        power_kind, created = game.powers.get_or_create(key=self.kind)
        power_category, created2 = power_kind.categories.get_or_create(key=found_category)
        power, created3 = power_category.powers.get_or_create(key=key)
        new_power, created4 = power.characters.get_or_create(character=self.owner.storyteller)
        if created3:
            new_power.rating = amount
        else:
            new_power.rating += amount
        new_power.save()
        self.load()

    def sheet_render(self, width=78):
        powers = self.existing
        if not powers:
            return
        section = list()
        colors = self.sheet_colors
        section.append(self.sheet_header(self.name, width=width))
        for category in self.display_categories:
            cat_line = '====%s====' % category
            cat_line = cat_line.center(width-2)
            section.append(self.sheet_border(cat_line, width=width))
            skill_display = [power.sheet_format(width=23, colors=colors, mode='word') for power
                             in self.charm_categorized[category]]
            skill_table = unicode(tabular_table(skill_display, field_width=37, line_length=width-2))
            section.append(self.sheet_border(skill_table, width=width))
        return '\n'.join(unicode(line) for line in section)


class SolarCharms(CharmSection):
    name = 'Solar Charms'
    kind = 'solar_charm'
    sub_choices = ('Archery', 'Brawl', 'Melee', 'War', 'Thrown', 'Bureaucracy', 'Linguistics', 'Ride', 'Sail',
                   'Socialize', 'Athletics', 'Awareness', 'Dodge', 'Larceny', 'Stealth', 'Craft', 'Investigation',
                   'Lore', 'Medicine', 'Occult', 'Integrity', 'Performance', 'Presence', 'Resistance', 'Survival')
    list_order = 505


class AbyssalCharms(SolarCharms):
    name = 'Abyssal Charms'
    kind = 'abyssal_charm'
    list_order = 510


class TerrestrialCharms(SolarCharms):
    name = 'Terrestrial Charms'
    kind = 'terrestrial_charm'
    list_order = 515


class LunarCharms(SolarCharms):
    name = 'Lunar Charms'
    kind = 'lunar_charm'
    sub_choices = ('Strength', 'Dexterity', 'Stamina', 'Charisma', 'Manipulation', 'Appearance', 'Intelligence', 'Wits',
                   'Perception', 'Knacks')
    list_order = 520


class MartialCharms(CharmSection):
    pass


class Sorcery(CharmSection):
    name = 'Sorcery'
    sub_choices = ('Terrestrial Circle Spells', 'Celestial Circle Spells', 'Solar Circle Spells')
    kind = 'sorcery_spell'
    list_order = 700


class Necromancy(Sorcery):
    name = 'Necromancy'
    sub_choices = ('Shadowlands Circle Spells', 'Labyrinth Circle Spells', 'Void Circle Spells')
    kind = 'necromancy_spell'
    list_order = 705


class PoolSection(SheetSection):
    name = 'Pool'
    list_order = 900
    kind = 'pool'
    pools = list()
    tracks = list()
    experience = list()

    def load(self):
        self.pools = sorted([pool for pool in self.owner.storyteller.pools.all() if pool.category == 'Pool'],
                            key=lambda po: po.list_order)
        self.tracks = sorted([pool for pool in self.owner.storyteller.pools.all() if pool.category == 'Track'],
                             key=lambda po: po.list_order)
        self.experience = sorted([exp for exp in self.owner.storyteller.exp_kinds.all() if exp.entries.count()],
                                 key=lambda xp: xp.list_order)


    def sheet_render(self, width=78):
        colors = self.sheet_colors
        line1 = self.sheet_header(width=width)
        line2 = ' {%s\\{n%s{n{%s/{n' % (colors['border'], self.owner.storyteller.sheet_footer.center(width - 4),
                                        colors['border'])
        line3 = '  {%s.%s.{n' % (colors['border'], '-' * (width-6))

        section = list()
        section.append(self.sheet_triple_header(['Pools', 'Tracks', 'Experience'], width=width))
        col_widths = self.calculate_widths(width)
        pools = '\n'.join([pool.sheet_format(rjust=12) for pool in self.pools if pool.max])
        tracks = '\n'.join([pool.sheet_format(rjust=13) for pool in self.tracks if pool.max])
        experience = '\n'.join([xp.sheet_format(rjust=13) for xp in self.experience])
        section.append(self.sheet_columns([pools, tracks, experience], width=width))
        section.append(line1)
        section.append(line2)
        section.append(line3)
        return '\n'.join(unicode(line) for line in section)



SECTION_LIST = (TemplateSection, Attributes, Abilities, Specialties, Favored, Supernal, SolarCharms, AbyssalCharms,
                LunarCharms, TerrestrialCharms, MartialCharms, Sorcery, Necromancy, Merit, Flaw, Crafts, Styles,
                PoolSection)
