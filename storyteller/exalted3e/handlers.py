from storyteller.handlers import BaseHandler, StatHandler
from django.conf import settings
from athanor.utils import partial_match, validate_name
from storyteller.utils import dramatic_capitalize
from .models import Charm, CharmRank, StatCharm, StatCharmRank, Merit, MeritRank, Evocation


class AbilityHandler(StatHandler):
    choices = settings.STORYTELLER_ABILITIES
    stat_category = "Abilities"
    plural_name = "Abilities"
    singular_name = "Ability"
    remove_zero = True


class StyleHandler(StatHandler):
    stat_category = "Styles"
    plural_name = "Martial Arts Styles"
    singular_name = "Martial Arts Style"
    remove_zero = True

    def get_choice(self, entry: str) -> str:
        name = validate_name(entry, thing_type=self.singular_name)
        return dramatic_capitalize(name)


class _ContextHandler(BaseHandler):
    pass


class MeritHandler(_ContextHandler):
    attribute_category = "merits"


class FlawHandler(_ContextHandler):
    attribute_category = "flaws"


class _WordPowerHandler(BaseHandler):
    plural_name = None
    singular_name = None
    categories = {}

    def render_name(self):
        return "Name"

    def render_cat_name(self, category: str) -> str:
        return f"{category}"

    def render_subcat_name(self, category: str, subcategory: str) -> str:
        return f"{category} {subcategory}"

    def render_thing_name(self, category: str, subcategory: str, name: str) -> str:
        return f"{category} {subcategory} {self.singular_name}"

    def get_category(self, name: str) -> str:
        if not name:
            raise ValueError(f"No {self.render_name()} category given.")
        if not (category := partial_match(name, self.categories.keys())):
            raise ValueError(
                f"No {self.render_name()} category found matching '{name}'. Choices are: {', '.join(self.categories.keys())}")
        return category

    def get_subcategory(self, category: str, name: str) -> str:
        if not name:
            raise ValueError(f"No {self.render_cat_name(category)} category given.")
        choices = self.categories[category]

        # deal with that pesky Martial Arts category.
        if callable(choices):
            choices = choices(self.owner)

        if not (subcategory := partial_match(name, choices)):
            raise ValueError(
                f"No {category} {self.plural_name} subcategory found matching '{name}'. Choices are: {', '.join(choices)}")

        return subcategory

    def add(self, category: str, subcategory: str, name: str, value: int = 1):
        return self.do_base(category, subcategory, name, value, self.do_add)

    def remove(self, category: str, subcategory: str, name: str, value: int = 1):
        return self.do_base(category, subcategory, name, value, self.do_remove)

    def make_key(self, category: str, subcategory: str) -> str:
        return f"{category}:{subcategory}"

    def check_name(self, category: str, subcategory: str, name: str) -> str:
        name = validate_name(name, thing_type=f"{category} {subcategory} {self.plural_name}")
        return dramatic_capitalize(name)

    def do_base(self, category: str, subcategory: str, name: str, value: int, method: callable):
        found_category = self.get_category(category)
        found_subcategory = self.get_subcategory(found_category, subcategory)
        found_name = self.check_name(found_category, found_subcategory, name)
        try:
            value = int(value)
        except ValueError:
            raise ValueError(f"Value '{value}' is not an integer.")
        return method(found_category, found_subcategory, found_name, value)

    def do_add(self, category: str, subcategory: str, name: str, value: int):
        wpower, created = Charm.objects.get_or_create(category=category, subcategory=subcategory, name=name)
        rank, rank_created = self.owner.stdb_charms.get_or_create(charm=wpower)
        before = rank.value
        rank.value += value
        rank.save()
        return rank, before

    def do_remove(self, category: str, subcategory: str, name: str, value: int):
        wpower, created = Charm.objects.get_or_create(category=category, subcategory=subcategory, name=name)
        rank, rank_created = self.owner.stdb_charms.get_or_create(charm=wpower)
        before = rank.value
        rank.value -= value
        if rank.value <= 0:
            rank.delete()
            if not wpower.ranks.all().count():
                wpower.delete()
            return None, before, value
        else:
            rank.save()
            return rank, before, value


_EXIGENT_CHARMS = ["Offensive", "Defensive", "Social", "Mobility and Travel"]


class CharmHandler(_WordPowerHandler):
    category = "Charms"
    plural_name = "Charms"
    singular_name = "Charm"
    categories = {
        "Solar": settings.STORYTELLER_ABILITIES,
        "Abyssal": settings.STORYTELLER_ABILITIES,
        "Infernal": settings.STORYTELLER_ABILITIES,
        "Dragon-Blooded": settings.STORYTELLER_ABILITIES,
        "Sovereign": settings.STORYTELLER_ABILITIES,
        "Sidereal": settings.STORYTELLER_ABILITIES + ["Journeys", "Battles", "Secrets", "Endings", "Serenity"],
        "Lunar": settings.STORYTELLER_ATTRIBUTES + ["Universal"],
        "Alchemical": settings.STORYTELLER_ATTRIBUTES,
        "Getimian": settings.STORYTELLER_ATTRIBUTES,
        "Architect": settings.STORYTELLER_ATTRIBUTES,
        "Dream-Souled": ["Illusion and Transformation"] + _EXIGENT_CHARMS,
        "Hearteater": ["Pawn"] + _EXIGENT_CHARMS + ["Mysticism"],
        "Umbral": ["Penumbra", "Darkness"] + _EXIGENT_CHARMS + ["Mysticism"],
        "Exigent": settings.STORYTELLER_ATTRIBUTES + settings.STORYTELLER_ABILITIES + _EXIGENT_CHARMS
                   + ["Mysticism", "Universal", "Essence"],
        "Spirit": ["Universal"] + _EXIGENT_CHARMS + ["Essence", "Mysticism", "Eclipse"],
        "Martial Arts": lambda x: list(x.st_styles.all().keys()),
    }

    def render_name(self):
        return "Charms"

    def render_cat_name(self, category: str) -> str:
        return f"{category} Charms"

    def render_subcat_name(self, category: str, subcategory: str) -> str:
        return f"{category} {subcategory} Charms"

    def render_thing_name(self, category: str, subcategory: str, name: str) -> str:
        return f"{category} {subcategory} Charm: {name}"


class EvocationHandler(_WordPowerHandler):
    attribute_category = "evocations"

    def render_name(self):
        return "Evocation"

    def render_cat_name(self, category: str) -> str:
        return f"Evocations"

    def render_subcat_name(self, category: str, subcategory: str) -> str:
        return f"{subcategory} Evocations"

    def render_thing_name(self, category: str, subcategory: str, name: str) -> str:
        return f"{subcategory} Evocation: {name}"

    def get_category(self, name: str) -> str:
        return "evocations"

    def get_subcategory(self, category: str, name: str) -> str:
        choices = self.owner.st_merits.all(category="Artifact")
        if not (subcategory := partial_match(name, choices)):
            raise ValueError(
                f"No Artifact found matching '{name}'. Choices are: {', '.join(choices)}")
        return subcategory

    def make_key(self, category: str, subcategory: str) -> str:
        return subcategory

    def add(self, subcategory: str, name: str, value: int = 1):
        return self.do_base("evocations", subcategory, name, value, self.do_add)

    def remove(self, subcategory: str, name: str, value: int = 1):
        return self.do_base("evocations", subcategory, name, value, self.do_remove)


class SpellHandler(_WordPowerHandler):
    category = "Spells"
    categories = {
        "Sorcery": ["Terrestrial", "Celestial", "Solar"],
        "Necromancy": ["Ivory", "Shadow", "Void"]
    }
