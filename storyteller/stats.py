import re
from storyteller.exceptions import StoryDBException
from storyteller.utils import dramatic_capitalize
from storyteller.models import StorytellerStat


class StatManager:
    ops = []

    def __init__(self, owner):
        self.owner = owner

    def stat_row(self, path: list[str], creator=None):
        if len(path) > 4:
            raise StoryDBException(f"Database depth limit is 4, got {path}")
        names = dict()
        for i, n in enumerate(path):
            names[f"name_{i+1}"] = dramatic_capitalize(n)
        stat, created = StorytellerStat.objects.get_or_create(**names)
        if created:
            stat.save()
        return stat

    def good_name(self, in_name, name_for: str = "stat", max_length: int=80) -> str:
        dc = dramatic_capitalize(in_name)
        if not dc:
            raise StoryDBException(f"Must enter a name for the {name_for}.")
        if len(dc) > max_length:
            raise StoryDBException(f"'{dc} is too long a name for a {name_for}.")
        return dc

    def add(self, user, target, path: list[str], value: int=1):
        pass

    def rem(self, user, target, path: list[str], value: int=1):
        pass

    def set(self, user, target, path: list[str], value: int=1):
        pass

    def set_base(self, target, stat_row, value: int=1) -> ("cstat", int):
        try:
            value = int(value)
        except ValueError as err:
            raise StoryDBException(f"Must enter a whole number 0 or greater!")
        if value < 0:
            raise StoryDBException(f"Must enter a whole number 0 or greater!")
        cstat, created = target.story_stats.get_or_create(stat=stat_row)
        return cstat, value

    def set_int(self, target, stat_row, value: int=1):
        cstat, value = self.set_base(target, stat_row, value=value)
        cstat.stat_value = value
        cstat.save()

    def set_flag_1(self, target, stat_row, value: int=1):
        cstat, value = self.set_base(target, stat_row, value=value)
        cstat.stat_flag_1 = value
        cstat.save()

    def set_flag_2(self, target, stat_row, value: int=1):
        cstat, value = self.set_base(target, stat_row, value=value)
        cstat.stat_flag_2 = value
        cstat.save()
