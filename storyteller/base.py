from athanor.utils import partial_match
from storyteller.models import TemplateInfo


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
        return self

    def set_field(self, target: "DefaultCharacter", field: str, value: str):
        """
        Set a target's template field to the given value.
        """
        found_field = partial_match(field, self.fields)
        if not found_field:
            raise ValueError(
                f"No field found matching '{field}'. Choices are: {', '.join(self.fields)}"
            )
        if choices := self.field_choices.get(found_field, list()):
            if not (choice := partial_match(value, choices)):
                raise ValueError(
                    f"No choice found matching '{value}'. Choices are: {', '.join(choices)}"
                )
            value = choice
        else:
            value = str(value)
        self.do_set_field(target, found_field, value)
        return found_field, value

    def do_set_field(self, target: "DefaultCharacter", name: str, value: str):
        field, created = target.stdb_fields.get_or_create(field=name)
        field.value = value
        field.save()
