from evennia.utils.utils import callables_from_module
from athanor.utils import partial_match, Operation
import storyteller
from storyteller.models import SheetInfo


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
    colors = {"stat": "n", "border": "n", "dot": "n", "slash": "n", "title": "n"}
    tier_symbols = {0: " ", 1: "-", 2: "+", 3: "*"}
    advantages = list()
    advantages_defaults = dict()
    sheet_footer = "Storyteller"

    def __init__(self, game):
        self.game = game

    @property
    def name(self):
        return self.__class__.__name__

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<{self.game} Template: {self.name}>"

    def get_fields(self, target):
        return self.fields

    def get_field_choices(self, target, field):
        return self.field_choices.get(field, None)

    def change(self, target: "DefaultCharacter"):
        """
        Change target to be this type of Template.
        """
        target.sheet.fields.all().delete()
        tinfo, created = SheetInfo.objects.get_or_create(
            game=self.game, character=target
        )
        if created:
            tinfo.save()
        target.sheet.template = self.name
        target.sheet.save(update_fields=["template"])

        for field, value in self.field_defaults.items():
            self.do_set_field(target, field, value)
        return self

    def do_set_field(self, target: "DefaultCharacter", name: str, value: str):
        field, created = target.sheet.fields.get_or_create(field=name)
        field.value = value
        field.save()

    def field(self, target, field):
        """
        Get the value of a field for this template.
        """
        model = target.sheet.fields.filter(field__iexact=field).first()
        if not model:
            return ""
        return model.value

    def get_sheet_columns(
        self, target
    ) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
        """
        Get the left and right columns for the sheet.
        """
        return self.get_left_columns(target), self.get_right_columns(target)

    def get_left_columns(self, target) -> list[tuple[str, str]]:
        out = list()
        out.append(("Template", self.name))
        out.append(("Name", str(target)))
        out.append(("Sex", str(target.db.sex)))
        return out

    def get_right_columns(self, target) -> list[tuple[str, str]]:
        out = list()
        for field in self.get_fields(target):
            out.append((field, self.field(target, field)))
        return out


class Game:
    """
    Each character must have a Game assigned to them. A Game object is used to bundle up Templates and rules.
    A great deal of logic is supposed to be placed on Games, but this will vary from game to game.
    """

    def __init__(self, alias: str, name: str, key: str = None):
        self.alias = alias
        self.name = name
        self.key = key or alias
        self.templates = dict()
        self.handlers = list()
        self.default_template = "Mortal"

    def __str__(self):
        return self.key

    def setup_templates(self, path: str):
        for k, v in callables_from_module(path).items():
            template = v(self)
            self.templates[template.name] = template

    def setup_handlers(self, path: str):
        self.handlers.extend(callables_from_module(path).values())

    def get_handlers(self, character):
        return self.handlers

    def render_help(self, lines: list[str]):
        pass

    def render_help_end(self, lines: list[str]):
        pass
