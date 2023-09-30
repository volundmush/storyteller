import typing
import storyteller
from django.conf import settings
from athanor.utils import partial_match, validate_name
from storyteller.utils import dramatic_capitalize
from .storybase.models import Stat, StatRank, Specialty


class TemplateHandler:
    choices = storyteller.TEMPLATES

    def __init__(self, owner):
        self.owner = owner
        if not hasattr(owner, "stdb_template"):
            temp = self.choices.get(settings.STORYTELLER_DEFAULT_TEMPLATE)
            temp.change(owner)

    def get(self):
        return self.choices.get(self.owner.stdb_template.template, None)

    def get_field(self, field: str) -> typing.Optional[str]:
        return self.owner.attributes.get(category="template", key=field)

    def set_field(self, field: str, value: str):
        self.get().set_field(self.owner, field, value)

    def set_template(self, name: str):
        templates = self.choices.values()
        template = partial_match(name, templates)
        if not template:
            raise ValueError(f"No template found matching '{name}'. Choices are: {', '.join(templates)}")
        template.change(self.owner)


class BaseHandler:
    handler_name = None

    def __init__(self, owner):
        self.owner = owner


class StatHandler(BaseHandler):
    choices: list[str] = None
    stat_category: str = None
    plural_name = None
    singular_name = None
    remove_zero = False
    min_value = 0
    max_value = 10

    def get_choice(self, entry: str) -> str:
        if not entry:
            raise ValueError(f"No {self.singular_name} name given.")
        if not (choice := partial_match(entry, self.choices)):
            raise ValueError(
                f"No {self.singular_name} found matching '{entry}'. Choices are: {', '.join(self.choices)}")
        return choice

    def all(self):
        return {srank.stat.name: srank for srank in
                self.owner.stdb_stats.filter(stat__category=self.stat_category)}

    def check_rating(self, value: int):
        # now coerce value to an int...
        if not isinstance(value, int) and not value:
            raise ValueError(f"No value given for {value} {self.singular_name}.")
        try:
            rating = int(value) if not isinstance(value, int) else value
        except ValueError:
            raise ValueError(f"Value '{value}' is not an integer.")

        if rating < self.min_value:
            raise ValueError(f"Value '{rating}' is less than the minimum value of {self.min_value}.")
        if rating > self.max_value:
            raise ValueError(f"Value '{rating}' is greater than the maximum value of {self.max_value}.")
        return rating

    def get_stat(self, name: str) -> Stat:
        choice = self.get_choice(name)
        stat, created = Stat.objects.get_or_create(category=self.stat_category, name=choice)
        return stat

    def set_rank(self, name: str, value: int) -> tuple[str, int, int, StatRank]:
        choice = self.get_choice(name)
        rating = self.check_rating(value)
        stat = self.get_stat(choice)

        srank, srank_created = self.owner.stdb_stats.get_or_create(stat=stat)
        before = srank.value

        if self.remove_zero and rating == 0:
            srank.delete()
            return choice, before, rating, srank

        srank.value = rating
        return choice, before, rating, srank

    def add_rank(self, name: str, value: int):
        pass

    def remove_rank(self, name: str, value: int):
        pass

    def set_tag(self, name: str, tag: str):
        pass

    def remove_tag(self, name: str, tag: str):
        pass


class AdvantageHandler(StatHandler):
    choices = settings.STORYTELLER_ADVANTAGES
    stat_category = "Advantages"
    plural_name = "Advantages"
    singular_name = "Advantage"

    def get_choice(self, entry: str) -> str:
        choice = super().get_choice(entry)
        if choice == "Power":
            return self.owner.st_template.get_attribute().power_stat
        return choice


class AttributeHandler(StatHandler):
    choices = settings.STORYTELLER_ATTRIBUTES
    stat_category = "Attributes"
    plural_name = "Attributes"
    singular_name = "Attribute"


class SpecialtyHandler(StatHandler):
    choices = settings.STORYTELLER_SKILLS
    stat_category = "Specialties"
    plural_name = "Specialties"
    singular_name = "Specialty"
    max_value = 1
    remove_zero = True

    def set_rank(self, stat_name: str, name: str, value: int) -> tuple[str, int, int, StatRank]:
        stat_name = self.get_choice(stat_name)
        choice = validate_name(name, thing_type=f"{self.singular_name} name")
        rating = self.check_rating(value)

        stat = self.get_stat(stat_name)

        if not (srank := self.owner.stdb_specialties.filter(stat=stat, name__iexact=choice).first()):
            srank, srank_created = self.owner.stdb_specialties.get_or_create(stat=stat, name=choice)
        else:
            srank.name = choice
        before = srank.value

        if self.remove_zero and rating == 0:
            srank.delete()
            return choice, before, rating, srank

        srank.value = rating
        return choice, before, rating, srank

    def all(self):
        return {(srank.stat.name, srank.name): srank for srank in self.owner.stdb_specialties.all()}
