from storyteller.exbase import templates as t
from storyteller.templates import TemplateHandler as old_th


def get_virtues_normal(target):
    out = 0
    for stat in target.story_stats.filter(stat__name_1="Virtues"):
        out += stat.stat_value
    return out


def get_virtues_max(target):
    return 20


get_virtues = get_virtues_normal


class _Solaroid:

    def pool_personal_max(self):
        out = 0
        c = self.handler.owner
        out += t.get_essence(c) * 3
        out += t.get_willpower(c)

    def pool_peripheral_max(self):
        out = 0
        c = self.handler.owner
        out += t.get_essence(c) * 7
        out += t.get_willpower(c)
        out += get_virtues(c)


class Solar(_Solaroid, t.Solar):
    pass


class Abyssal(_Solaroid, t.Abyssal):
    pass


class Infernal(_Solaroid, t.Abyssal):
    sub_types = ["Slayer", "Malefactor", "Defiler", "Scourge", "Fiend"]


class Lunar(t.Lunar):
    pass
