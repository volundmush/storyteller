from storyteller.base.sheet import Attributes as OldAttr, Skills, AdvantageWordSection, SheetSection


class Attributes(OldAttr):
    pass


class Abilities(Skills):
    name = 'Abilities'

    def load(self):
        self.entries = self.handler.stats.abilities


ALL_SHEET = (Attributes, Abilities)

class CharmSection(AdvantageWordSection):
    name = 'Charms'
    display_categories = tuple()
    charm_categorized = dict()
    sub_choices = tuple()
    kind = 'charm'
    list_order = 500

    def load(self):
        super(CharmSection, self).load()
        self.display_categories = sorted(list(set(stat.power.category for stat in self.entries)))
        for category in self.display_categories:
            self.charm_categorized[category] = sorted([power for power in self.entries if power.power.category == category],
                                                      key=lambda power2: str(power2))

    def sheet_render(self, width=78):
        powers = self.entries
        if not powers:
            return
        section = list()
        colors = self.colors
        section.append(self.header(self.name, width=width))
        for category in self.display_categories:
            cat_line = '====%s====' % category
            cat_line = cat_line.center(width-2)
            section.append(self.border(cat_line, width=width))
            skill_display = [power.sheet_format(width=23, colors=colors, mode='word') for power
                             in self.charm_categorized[category]]
            skill_table = unicode(tabular_table(skill_display, field_width=37, line_length=width-2))
            section.append(self.border(skill_table, width=width))
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
        self.pools = self.handler.pools.all_pools
        self.tracks = self.handler.pools.all_tracks
        self.experience = sorted([exp for exp in self.owner.storyteller.exp_kinds.all() if exp.entries.count()],
                                 key=lambda xp: xp.list_order)


    def render(self, width=78):
        colors = self.colors
        line1 = self.header(width=width)
        line2 = ' {%s\\{n%s{n{%s/{n' % (colors['border'], self.owner.storyteller.sheet_footer.center(width - 4),
                                        colors['border'])
        line3 = '  {%s.%s.{n' % (colors['border'], '-' * (width-6))

        section = list()
        section.append(self.triple_header(['Pools', 'Tracks', 'Experience'], width=width))
        col_widths = self.calculate_widths(width)
        pools = '\n'.join([pool.sheet_format(rjust=12) for pool in self.pools if pool.max])
        tracks = '\n'.join([pool.sheet_format(rjust=13) for pool in self.tracks if pool.max])
        experience = '\n'.join([xp.sheet_format(rjust=13) for xp in self.experience])
        section.append(self.columns([pools, tracks, experience], width=width))
        section.append(line1)
        section.append(line2)
        section.append(line3)
        return '\n'.join(unicode(line) for line in section)