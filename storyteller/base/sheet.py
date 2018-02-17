from __future__ import unicode_literals

import math
from django.conf import settings
from evennia.utils.evtable import EvTable
from evennia.utils.ansi import ANSIString
from athanor.utils.text import tabular_table

class SheetSection(object):
    name = '<unknown>'
    list_order = 0
    display = True

    def __init__(self, owner):
        self.owner = owner
        self.handler = owner.handler
        self.game = owner.game
        self.data = owner.data
        self.load()

    def __str__(self):
        return self.name

    def __int__(self):
        return self.list_order

    def __repr__(self):
        return '<SheetSection: %s>' % self.name

    @property
    def colors(self):
        return self.handler.template.template.template.colors

    def load(self):
        pass

    def render(self, width=80):
        return None

    def header(self, center_text=None, width=80):
        colors = self.colors
        start_char = ANSIString('|%s}|n' % colors['border'])
        end_char = ANSIString('|%s{|n' % colors['border'])
        if not center_text:
            center_section = '-' * (width - 2)
            center_section = ANSIString('|%s%s|n' % (colors['border'], center_section))
        else:
            show_width = width - 2
            fill = ANSIString('|%s-|n' % colors['border'])
            center_section = ANSIString('|%s/|n|%s%s|n|%s/|n' % (colors['slash'], colors['section_name'], center_text,
                                                                 colors['slash'])).center(show_width, fill)
        return start_char + center_section + end_char

    def triple_header(self, display_text=None, width=80):
        if not display_text:
            display_text = ['', '', '']
        colors = self.colors
        col_widths = self.calculate_widths(width-2)
        fill = ANSIString('|%s-|n' % colors['border'])
        sections = list()
        for count, header in enumerate(display_text):
            center_text = ANSIString('|%s/|n|%s%s|n|%s/|n' % (colors['slash'], colors['section_name'], header,
                                                              colors['slash'])).center(col_widths[count], fill)
            sections.append(center_text)

        start_char = ANSIString('|%s}|n' % colors['border'])
        end_char = ANSIString('|%s{|n' % colors['border'])
        return start_char + sections[0] + sections[1] + sections[2] + end_char

    def border(self, display_text=None, width=80):
        colors = self.colors
        ev_table = EvTable(border='cols', pad_width=0, valign='t',
                           border_left_char=ANSIString('|%s|' % colors['border']),
                           border_right_char=ANSIString('|%s|' % colors['border']), header=False)
        ev_table.add_row(display_text, width=width)
        return ev_table

    def columns(self, display_text=None, width=80):
        if not display_text:
            display_text = ['', '', '']
        colors = self.colors
        ev_table = EvTable(border='cols', pad_width=0, valign='t',
                           border_left_char=ANSIString('|%s|' % colors['border']),
                           border_right_char=ANSIString('|%s|' % colors['border']), header=False)
        ev_table.add_row(display_text[0], display_text[1], display_text[2])

        for count, col_width in enumerate(self.calculate_widths(width=width)):
            ev_table.reformat_column(count, width=col_width)
        return ev_table

    def sheet_two_columns(self, display_text=None, width=80):
        if not display_text:
            display_text = ['', '']
        colors = self.colors
        ev_table = EvTable(border='cols', pad_width=0, valign='t',
                           border_left_char=ANSIString('|%s||n' % colors['border']),
                           border_right_char=ANSIString('|%s||n' % colors['border']), header=False)
        ev_table.add_row(display_text[0], display_text[1])

        for count, col_width in enumerate(self.calculate_double(width=width)):
            ev_table.reformat_column(count, width=col_width)
        return ev_table

    def calculate_widths(self, width=80):
        column_widths = list()
        col_calc = width / float(3)
        for num in [0, 1, 2]:
            if num == 0:
                calculate = int(math.floor(col_calc))
                column_widths.append(calculate)
            if num == 1:
                calculate = int(math.ceil(col_calc))
                column_widths.append(calculate)
            if num == 2:
                calculate = int(width - 0 - column_widths[0] - column_widths[1])
                column_widths.append(calculate)
        return column_widths

    def calculate_double(self, width=80):
        column_widths = list()
        col_calc = width / float(2)
        for num in [0, 1]:
            if num == 0:
                calculate = int(math.floor(col_calc))
                column_widths.append(calculate)
            if num == 1:
                calculate = int(math.ceil(col_calc))
                column_widths.append(calculate)
        return column_widths


class StatSection(SheetSection):
    category = 'Skill'

    def load(self):
        self.entries = [stat for stat in self.handler.stats.stats if stat.category == self.category]

    def render(self, width=80):
        colors = self.colors
        skills = [stat for stat in self.entries if stat.display]
        if not skills:
            return
        section = list()
        section.append(self.header(self.name, width=width))
        skill_display = [stat.sheet_format(width=24, colors=colors) for stat in skills]
        skill_table = tabular_table(skill_display, field_width=24, line_length=width-2)
        section.append(self.border(skill_table, width=width))
        return '\n'.join(unicode(line) for line in section)

class CustomSection(StatSection):
    kind = 'custom'

    def load(self):
        self.entries = sorted([stat for stat in self.owner.storyteller.customs.all() if stat.stat.kind.key == self.kind],
                               key=lambda stat2: str(stat2))
    def render(self, width=80):
        colors = self.colors
        skills = [stat for stat in self.entries if stat.display()]
        if not skills:
            return
        section = list()
        section.append(self.header(self.name, width=width))
        skill_display = [stat.sheet_format(width=24, colors=colors) for stat in skills]
        skill_table = tabular_table(skill_display, field_width=24, line_length=width - 2)
        section.append(self.border(skill_table, width=width))
        return '\n'.join(unicode(line) for line in section)


class Attributes(StatSection):
    name = 'Attributes'
    list_order = 10
    display = True

    def load(self):
        self.physical = self.handler.stats.physical_attributes
        self.social = self.handler.stats.social_attributes
        self.mental = self.handler.stats.mental_attributes

    def render(self, width=80):
        colors = self.colors
        section = list()
        section.append(self.triple_header(['Physical Attributes', 'Social Attributes', 'Mental Attributes'],
                                                width=width))
        col_widths = self.calculate_widths(width)
        physical = '\n'.join([stat.sheet_format(width=col_widths[0]-2, colors=colors) for stat in self.physical])
        social = '\n'.join([stat.sheet_format(width=col_widths[1]-1, colors=colors) for stat in self.social])
        mental = '\n'.join([stat.sheet_format(width=col_widths[2]-1, colors=colors) for stat in self.mental])
        section.append(self.columns([physical, social, mental], width=width))
        return '\n'.join(unicode(line) for line in section)


class Skills(StatSection):
    name = 'Skills'
    list_order = 15

    def load(self):
        self.entries = self.handler.stats.skills


class Specialties(StatSection):
    name = 'Specialties'
    list_order = 16

    def load(self):
        self.choices = [stat for stat in self.handler.stats_dict.values() if 'special' in stat.features]
        self.specialized = [stat for stat in self.handler.stats_dict.values() if stat.specialties.count() > 0]

    def sheet_render(self, width=80):
        colors = self.colors
        specialized = self.specialized
        if not specialized:
            return
        section = list()
        skill_display = list()
        section.append(self.header(self.name, width=width))
        for stat in specialized:
            skill_display += stat.sheet_specialties(colors=colors)
        skill_table = tabular_table(skill_display, field_width=23, line_length=width-2)
        section.append(self.border(skill_table, width=width))
        return '\n'.join(unicode(line) for line in section)


class MeritSection(SheetSection):
    name = 'DefaultMerit'
    list_order = 20
    existing = tuple()

    def load(self):
        self.existing = sorted([merit for merit in self.owner.storyteller.merits.all() if merit.kind.key == self.kind],
                               key=lambda mer: str(mer))

    def render(self, width=80):
        if not self.existing:
            return
        colors = self.colors
        section = list()
        merit_section = list()
        section.append(self.header(self.name, width=width))
        short_list = [merit for merit in self.existing if len(str(merit)) <= 30]
        long_list = [merit for merit in self.existing if len(str(merit)) > 30]
        short_format = [merit.sheet_format(colors=colors, width=36) for merit in short_list]
        long_format = [merit.sheet_format(width=width-4, colors=colors) for merit in long_list]
        if short_list:
            merit_section.append(tabular_table(short_format, field_width=36, line_length=width-4))
        if long_list:
            merit_section.append('\n'.join(long_format))
        section.append(self.border('\n'.join(merit_section), width=width))
        return '\n'.join(unicode(line) for line in section)


class AdvantageStatSection(SheetSection):
    name = 'DefaultAdvStat'
    list_order = 30

    def load(self):
        self.powers = [power for power in self.owner.storyteller.powers.all() if power.power.kind.key == self.kind]

    def render(self, width=80):
        powers = self.powers
        if not powers:
            return
        section = list()
        colors = self.colors
        section.append(self.header(self.name, width=width))
        skill_display = [power.sheet_format(width=23, colors=colors, mode='stat') for power in powers]
        skill_table = tabular_table(skill_display, field_width=23, line_length=width-2)
        section.append(self.border(skill_table, width=width))
        return '\n'.join(unicode(line) for line in section)


class AdvantageWordSection(AdvantageStatSection):
    name = 'DefaultAdvPower'
    list_order = 50

    def render(self, width=80):
        powers = self.powers
        if not powers:
            return
        section = list()
        colors = self.colors
        section.append(self.header(self.name, width=width))
        skill_display = [power.sheet_format(width=23, colors=colors, mode='word') for power in powers]
        skill_table = tabular_table(skill_display, field_width=23, line_length=width-2)
        section.append(self.border(skill_table, width=width))
        return '\n'.join(unicode(line) for line in section)


class TemplateSection(SheetSection):
    name = 'Template'
    list_order = 0

    def render(self, width=80):
        return None
        servername = unicode(settings.SERVERNAME)
        colors = self.colors
        line1 = '  {%s.%s.{n' % (colors['border'], '-' * (width-6))
        line2 = ' {%s/{n%s{n{%s\\{n' % (colors['border'], servername.center(width-4), colors['border'])
        line3 = self.header(width=width)
        name = self.owner.key
        power = self.handler.stats_dict['essence']
        powername = 'Essence'
        column_1 = ['Name']
        column_1 += self.owner.storyteller.sheet_column_1
        column_2 = [powername]
        column_2 += self.owner.storyteller.sheet_column_2
        column_1_len = max([len(entry) for entry in column_1])
        column_2_len = max([len(entry) for entry in column_2])
        column_1_prep = list()
        column_2_prep = list()
        for entry in column_1:
            if entry == 'Name':
                display = '%s: %s' % ('Name'.rjust(column_1_len), name)
            else:
                display = '%s: %s' % (entry.rjust(column_1_len), self.owner.storyteller.get(entry))
            column_1_prep.append(display)
        for entry in column_2:
            if entry == powername:
                display = '%s: %s' % (powername.rjust(column_2_len), int(power))
            else:
                display = '%s: %s' % (entry.rjust(column_2_len), self.owner.storyteller.get(entry))
            column_2_prep.append(display)
        line4 = self.sheet_two_columns(['\n'.join(column_1_prep), '\n'.join(column_2_prep)], width=width)
        return '\n'.join(unicode(line) for line in [line1, line2, line3, line4])