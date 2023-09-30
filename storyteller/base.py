import typing
from athanor.utils import partial_match
from storyteller.storybase.models import TemplateInfo


class Template:
    """
    The base class for a Storyteller 'Template', such as Mortal, Vampire, Mage, Werewolf,
    Solar, Lunar, etc.
    """
    # The fields relevant to the template.
    # For a Vampire that could be its Clan, Bloodline, and Coterie.
    # for a Solar, it might be their Caste.
    # these are supposed to be strings.
    fields = []
    field_defaults = {}
    field_choices = {}
    power_stat = None
    game = "Storyteller"

    @property
    def name(self):
        return self.__class__.__name__

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<{self.game} Template: {self.name}>"

    def change(self, target: "DefaultCharacter"):
        """
        Change target to be this type of Template.
        """
        target.stdb_fields.all().delete()
        tinfo, created = TemplateInfo.objects.get_or_create(character=target)
        if created:
            tinfo.save()
        target.stdb_template.template = self.name
        target.stdb_template.save(update_fields=["template"])

        for field, value in self.field_defaults.items():
            self.do_set_field(target, field, value)

    def set_field(self, target: "DefaultCharacter", field: str, value: str):
        """
        Set a target's template field to the given value.
        """
        found_field = partial_match(field, self.fields)
        if not found_field:
            raise ValueError(f"No field found matching '{field}'. Choices are: {', '.join(self.fields)}")
        if (choices := self.field_choices.get(found_field, list())):
            if not (choice := partial_match(value, choices)):
                raise ValueError(f"No choice found matching '{value}'. Choices are: {', '.join(choices)}")
            value = choice
        else:
            value = str(value)
        self.do_set_field(target, found_field, value)

    def do_set_field(self, target: "DefaultCharacter", name: str, value: str):
        field, created = target.stdb_fields.get_or_create(field=name)
        field.value = value
        field.save()



class StatNode:
    """
    A category of stats, such as Attributes, Abilities, or Merits.
    This serves as a wrapper for accessing the Stat models with game rules in mind.
    """

    def __init__(self, name: str, parent: typing.Optional["StatNode"] = None):
        self.name = name
        self.parent = parent
        self.options = set()
        self.nodes: list[StatNode] = []
        self.stats: list[str] = []
        self.min_value = 0
        self.max_value = 10
        self.handler_name: str = None

    def __str__(self):
        return self.name

    def get_nodes(self, target: "DefaultCharacter"):
        """
        Returns a list of StatCategory subclasses which are the subcategories of this category.

        Returns:
            list[StatCategory]: A list of StatCategory subclasses.
        """
        return list(self.nodes)

    def get_stats(self, target: "DefaultCharacter"):
        """
        Returns a list of Strings which are the names of all the stats that can branch off this category.

        Returns:
            list[str]: A list of strings.
        """
        return list(self.stats)

    def set(self, user: "DefaultCharacter", target: "DefaultCharacter", path: list[str], value: str):
        raise NotImplemented

    def add(self, user: "DefaultCharacter", target: "DefaultCharacter", path: list[str], value: str):
        raise NotImplemented

    def remove(self, user: "DefaultCharacter", target: "DefaultCharacter", path: list[str], value: str):
        raise NotImplemented

    def tag(self, user: "DefaultCharacter", target: "DefaultCharacter", path: list[str], value: str):
        raise NotImplemented
