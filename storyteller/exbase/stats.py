from django.conf import settings

from storyteller.stats import StatManager
from storyteller.exceptions import StoryDBException

from athanor.utils import partial_match

_ATTRIBUTES = ["Strength", "Dexterity", "Stamina", "Charisma", "Manipulation", "Appearance", "Perception",
               "Intelligence", "Wits"]

_ATTRIBUTES_CAT = {
    "physical": ["Strength", "Dexterity", "Stamina"],
    "social": ["Charisma", "Manipulation", "Appearance"],
    "mental": ["Perception", "Intelligence", "Wits"]
}


class Attributes(StatManager):
    ops = ["set", "favor"]

    def get_attributes(self):
        return list(_ATTRIBUTES)

    def find_attr(self, target, path: list[str], op_name):
        if not len(path) >= 1:
            raise StoryDBException(f"No Attribute entered to {op_name}!")
        if not (found := partial_match(path[0], self.get_attributes())):
            raise StoryDBException(f"No Attribute called '{path[0]}'")
        return found

    def set(self, user, target, path: list[str], value: int = 1):
        found = self.find_attr(target, path, "set")
        row = self.stat_row(["Attributes", found])
        self.set_int(target, row, value=value)

    def favor(self, user, target, path, value: int = 1):
        # Todo: Only Lunars can Attribute favor. Put a restriction in.
        found = self.find_attr(target, path, "favor")
        row = self.stat_row(["Attributes", found])
        self.set_flag_1(target, row, value=value)


_ABILITIES = ["Archery", "Athletics", "Awareness", "Bureaucracy", "Craft", "Dodge", "Integrity", "Investigation",
              "Larceny", "Linguistics", "Lore", "Martial Arts", "Medicine", "Melee", "Occult", "Performance",
              "Presence", "Resistance", "Ride", "Sail", "Socialize", "Stealth", "Survival", "Thrown", "War"]


class Abilities(StatManager):
    ops = ["set", "favor"]
    not_settable = ["Craft", ]

    def get_abilities(self):
        return list(_ABILITIES)

    def find_abil(self, target, path: list[str], op_name):
        if not len(path) >= 1:
            raise StoryDBException(f"No Ability entered to {op_name}!")
        if not (found := partial_match(path[0], self.get_abilities())):
            raise StoryDBException(f"No Ability called '{path[0]}'")
        return found

    def set(self, user, target, path: list[str], value: int = 1):
        found = self.find_abil(target, path, "set")
        if found in self.not_settable:
            raise StoryDBException(f"{found} cannot be set directly as an Ability.")
        row = self.stat_row(["Abilities", found])
        self.set_int(target, row, value=value)

    def favor(self, user, target, path, value: int = 1):
        found = self.find_abil(target, path, "favor")
        row = self.stat_row(["Abilities", found])
        self.set_flag_1(target, row, value=value)


class Specialties(Abilities):
    ops = ["set"]

    def find_spec(self, target, path: list[str], op_name):
        if not len(path) >= 1:
            raise StoryDBException(f"No Stat entered to {op_name}!")
        available = self.get_abilities()
        # TODO: add support for Attribute specialties if character supports it.
        if not (found := partial_match(path[0], available)):
            raise StoryDBException(f"No specializable stat called '{path[0]}'")
        return found

    def set(self, user, target, path: list[str], value: int = 1):
        found = self.find_spec(target, path, "specialize")

        row = self.stat_row(["Specialties", found])
        self.set_int(target, row, value=value)