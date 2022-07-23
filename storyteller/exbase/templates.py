from storyteller.templates import Template as _Template
from athanor.utils import partial_match
from storyteller.exceptions import StoryDBException
from .stats import _ATTRIBUTES

_START_ADVANTAGES = {
    "Willpower": 5,
    "Essence": 1
}


def get_willpower_normal(target):
    if (will := target.story_stats.filter(stat__name_1="Advantages", stat__name_2="Essence").first()):
        return will.stat_value
    return 0


def get_willpower_max(target):
    return 10


get_willpower = get_willpower_normal


def get_essence(target):
    if (essence := target.story_stats.filter(stat__name_1="Advantages", stat__name_2="Essence").first()):
        return essence.stat_value
    return 1


class _Base(_Template):
    sub_types = []
    sub_name = "Caste"
    start_advantages = _START_ADVANTAGES

    def set_sub(self, entry: str):
        if not entry:
            raise StoryDBException(f"Must enter a Template name!")
        if not (found := partial_match(entry, self.sub_types)):
            raise StoryDBException(f"No {self.sub_name} matches {entry}.")
        self.handler.owner.db.template_subtype = found

    def initialize_attributes(self):
        c = self.handler.owner
        for a in _ATTRIBUTES:
            c.st_attributes.set(c, c, [a], value=1)

    def initialize_abilities(self):
        pass

    def initialize_advantages(self):
        c = self.handler.owner
        for k, v in self.start_advantages.items():
            c.st_advantages.set(c, c, [k], value=v)

    def initialize_template(self):
        if self.sub_types:
            self.handler.owner.db.template_subtype = self.sub_types[0]

    def initialize(self):
        self.initialize_template()
        self.initialize_attributes()
        self.initialize_abilities()
        self.initialize_advantages()

    def pool_personal_max(self):
        pass

    def pool_peripheral_max(self):
        pass

    def pool_overdrive_max(self):
        pass


_MORTAL_ADV = dict(_START_ADVANTAGES)
_MORTAL_ADV["Willpower"] = 3


class Mortal(_Base):
    sub_types = ["Warrior", "Priest", "Savant", "Criminal", "Broker"]
    start_advantages = _MORTAL_ADV


class Solar(_Base):
    sheet_colors = {'border': 'y'}
    sub_types = ["Dawn", "Zenith", "Twilight", "Night", "Eclipse"]


class Abyssal(_Base):
    sub_types = ["Dusk", "Midnight", "Daybreak", "Day", "Moonshadow"]


class DragonBlooded(_Base):
    name = "Dragon-Blooded"
    sub_types = ["Fire", "Water", "Air", "Earth", "Wood"]


class Sidereal(_Base):
    sub_types = ["Journeys", "Serenity", "Battles", "Secrets", "Endings"]


class Alchemical(_Base):
    sub_types = ["Orichalcum", "Moonsilver", "Jade", "Starmetal", "Soulsteel", "Adamant"]


class Lunar(_Base):
    sub_types = ["Full Moon", "Changing Moon", "No Moon", "Casteless"]
