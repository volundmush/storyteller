import typing
import storyteller
from django.conf import settings
from athanor.utils import (
    partial_match,
    validate_name,
    format_for_nobody,
    staff_alert,
    Operation,
)
from .utils import dramatic_capitalize
from .models import (
    Stat,
    StatRank,
    Power,
    PowerRank,
    StatPowerRank,
    CustomPower,
)


class RawHandler:
    """
    The Storyteller Handlers are modular components that deal with various bits of the Storyteller sheet data.
    They are called by the Storyteller Character sheet to do things like set stats, add powers, etc.

    They are designed to work with the athanor.utils.Operation class.
    """

    system_name = "SHEET"
    name: str = "Handler"
    options: set[str] = set()
    min_path_length = 1
    path_format = ""
    load_order = 0

    def __init__(self, owner, game):
        self.owner = owner
        self.game = game

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name} ({self.owner})>"

    def msg(self, message: str, from_obj=None):
        self.owner.system_send(self.system_name, message, mapping={}, from_obj=from_obj)

    def permission_check(self, operation: Operation):
        pass

    def at_pre_operation(self, operation: Operation):
        self.permission_check(operation)

        if self.min_path_length > 0:
            if (path := operation.kwargs.get("path", None)) is None:
                operation.status = operation.st.HTTP_400_BAD_REQUEST
                raise operation.ex(f"No path given.")
            if not isinstance(path, (list, set)):
                operation.status = operation.st.HTTP_400_BAD_REQUEST
                raise operation.ex(f"Path must be a list or set.")
            if len(path) < self.min_path_length:
                operation.status = operation.st.HTTP_400_BAD_REQUEST
                raise operation.ex(
                    f"Invalid path given. ( Requires at least {self.min_path_length} elements. {self.path_format})"
                )
            operation.variables["path"] = path

        if (value := operation.kwargs.get("value", None)) is None:
            operation.status = operation.st.HTTP_400_BAD_REQUEST
            raise operation.ex(f"No value given.")
        value = value.strip()
        if not value:
            operation.status = operation.st.HTTP_400_BAD_REQUEST
            raise operation.ex(f"No value given.")
        operation.variables["value"] = value

    def at_load(self):
        pass

    def template(self):
        return self.game.templates.get(self.owner.sheet.template, None)


class GameHandler(RawHandler):
    name = "Game"

    def __init__(self, owner):
        super().__init__(owner, None)
        self.game_module = None
        self.handlers = list()
        self.sorted_handlers = list()
        self.loaded = False

    def check_load(self):
        if not self.loaded:
            self.load()

    def load(self, module=None):
        game_name = None
        if not module:
            if not hasattr(self.owner, "sheet"):
                raise ValueError("No Game set!")
            game_name = self.owner.sheet.game
        if not module:
            self.game = storyteller.GAMES.get(game_name, None)
        if not self.game:
            raise ValueError("No module found for this game!")
        if not (handlers := self.game.get_handlers(self.owner)):
            raise ValueError("No handlers for this game!")
        self.handlers.clear()
        self.handlers.append(self)
        self.handlers.extend([handler(self.owner, self.game) for handler in handlers])
        self.handlers.sort(key=lambda x: x.load_order)
        self.loaded = True

        for handler in self.handlers:
            handler.at_load()

    def get(self, handler: str):
        self.check_load()
        if not (handler := partial_match(handler, self.handlers)):
            raise ValueError(
                f"No handler found matching '{handler}'. Choices are: {', '.join(self.handlers)}"
            )
        return handler

    def get_game(self):
        self.check_load()
        return self.game_module

    def op_set(self, operation: Operation):
        pass


class BaseHandler(RawHandler):
    plural_name = None
    singular_name = None
    remove_zero = False
    min_value = 0
    max_value = 10
    system_name = "SHEET"
    choices: list[str] = list()
    dynamic_choices = False
    use_context = False
    enforce_context = False

    def render_purchases(self, number) -> str:
        return f"Purchase{'' if number == 1 else 's'}"

    def get_choices(self) -> list[str]:
        return list(self.choices)

    def get_choice(self, operation, entry: str) -> str:
        if self.dynamic_choices:
            return dramatic_capitalize(
                validate_name(entry, thing_type=self.singular_name)
            )
        if not (choices := self.get_choices()):
            raise operation.ex(f"No {self.singular_name} choices found.")
        if not entry:
            raise operation.ex(f"No {self.singular_name} name given.")
        if not (choice := partial_match(entry, choices)):
            raise operation.ex(
                f"No {self.singular_name} found matching '{entry}'. Choices are: {', '.join(choices)}"
            )
        return choice

    def check_context(self, operation, name: str, context: str) -> str:
        context = context.strip()
        if context:
            context = validate_name(context, thing_type=f"{self.singular_name} Context")
        return context

    def check_tag(self, operation, name: str, context: str, tag: str) -> str:
        tag = validate_name(tag, thing_type=f"{self.singular_name} Tag")
        return dramatic_capitalize(tag)

    def parse_context(self, operation, name: str) -> tuple[str, str]:
        """
        Given a name such as "Artifact" or "Artifact: Grand Daiklave", splits it into a tuple like ["Artifact", ""] or
        ["Artifact", "Grand Daiklave"].

        Args:
            name: The name to parse.

        Returns:
            A tuple of [category, context]
        """
        if not name:
            raise operation.ex(f"No {self.singular_name} name given.")

        if ":" in name and not (self.use_context or self.enforce_context):
            raise operation.ex(f"{self.singular_name} cannot have a context.")

        if ":" in name:
            category, context = [n.strip() for n in name.split(":", 1)]
        else:
            if self.enforce_context:
                raise operation.ex(f"{self.singular_name} must have a context.")
            category = name
            context = ""
        category = validate_name(category, thing_type=self.singular_name)
        if context:
            context = self.check_context(operation, category, context)

        return category, context

    def check_rating(self, operation, name: str, context: str, value: int) -> int:
        # now coerce value to an int...
        if not isinstance(value, int) and not value:
            raise operation.ex(f"No value given for {name} {self.singular_name}.")
        try:
            rating = int(value) if not isinstance(value, int) else value
        except operation.ex:
            raise operation.ex(f"Value '{value}' is not an integer.")

        if rating < self.min_value:
            if self.remove_zero and rating == 0:
                rating = 0
            else:
                raise operation.ex(
                    f"Value '{rating}' is less than the minimum value of {self.min_value}."
                )
        if rating > self.max_value:
            raise operation.ex(
                f"Value '{rating}' is greater than the maximum value of {self.max_value}."
            )
        return rating

    def announce(self, user: "DefaultCharacter", message: str, mapping: dict = None):
        """
        Send messages to relevant parties about what happened.
        """
        if mapping is None:
            mapping = {}
        mapping["user"] = user
        mapping["target"] = self.owner

        user.system_send(self.system_name, message, mapping=mapping, from_obj=user)

        # If we are modifying ourselves, then there's no need to report further.
        # That could only happen for a character in chargen, or a staff member
        # editing themself for practice.
        if user == self.owner:
            return

        self.owner.system_send(
            self.system_name, message, mapping=mapping, from_obj=user
        )

        # send the message to the staff alert channel too.
        formatted = format_for_nobody(message, mapping)
        staff_alert(user, formatted)

    def error(self, user: "DefaultCharacter", message: str):
        """
        Send an error message to the user.
        """
        user.system_send(self.system_name, message, mapping={}, from_obj=user)


class TemplateHandler(RawHandler):
    """
    The TemplateHandler is a bit different from most Handlers. It has one option, "set", which changes the character's
    Template. That being the case, it doesn't need a "path" variable.
    """

    options = ("set",)
    name = "Templates"
    min_path_length = 0
    load_order = -1000

    def at_load(self):
        if not hasattr(self.owner, "sheet"):
            template = self.game.get_template(self.game.default_template)
            template.change(self.owner)
        for handler in self.game.handlers:
            handler.at_template_change(template)

    def at_template_change(self, template):
        pass

    def all_templates(self):
        return list(self.game.templates.values())

    def op_set(self, operation: Operation):
        value = operation.variables["value"]
        if not (template := partial_match(value, self.all_templates())):
            operation.status = operation.st.HTTP_400_BAD_REQUEST
            raise operation.ex(
                f"No template found matching '{value}'. Choices are: {', '.join(self.all_templates())}"
            )

        t = template.change(self.owner)
        if operation.actor != self.owner:
            self.msg(
                f"{operation.actor} changed your Template to: {t}",
                from_obj=operation.actor,
            )
            staff_alert(
                f"{operation.actor} changed {self.owner}'s Template to: {t}",
                senders=operation.actor,
            )
        operation.results["message"] = f"Template of {self.owner} was changed to: {t}"

    def get(self):
        return self.game.templates.get(self.owner.sheet.template, None)

    def get_field(self, field: str) -> typing.Optional[str]:
        if found := self.owner.sheet.fields.filter(field__iexact=field).first():
            return found.value
        return None


class FieldHandler(TemplateHandler):
    """
    The FieldHandler is used to handle the various fields that a Template can have, and setting them.

    'Fields' is a catch-all term for text fields that are not stats, powers, or merits, which often have a huge
    impact on the character's overall design. For example, a Vampire's Clan, or a Werewolf's Tribe.

    In Exalted, Castes and Aspects are fields, as is a Lunar's Spirit Shape/Totem Animal.

    What fields are available, and what they can be set to, as well as their defaults, are defined on the Template.
    """

    name = "Fields"
    path_format = "<field>"

    def field_choices(self):
        return self.get().get_fields(self.owner)

    def check_field(self, operation, field: str) -> str:
        field = field.strip()
        if not field:
            operation.status = operation.st.HTTP_400_BAD_REQUEST
            raise operation.ex(f"No field given.")
        t = self.get()
        if not (choices := t.get_fields(self.owner)):
            operation.status = operation.st.HTTP_400_BAD_REQUEST
            raise operation.ex(f"No field choices found.")
        if not (field := partial_match(field, choices)):
            operation.status = operation.st.HTTP_400_BAD_REQUEST
            raise operation.ex(
                f"No field found matching '{field}'. Choices are: {', '.join(choices)}"
            )
        return field

    def check_field_choice(self, operation: Operation, field: str, choice: str) -> str:
        choice = choice.strip()
        if not choice:
            operation.status = operation.st.HTTP_400_BAD_REQUEST
            raise operation.ex(f"No field value given.")
        t = self.get()
        choices = t.get_field_choices(self.owner, field)
        if choices:
            if not (choice := partial_match(choice, choices)):
                operation.status = operation.st.HTTP_400_BAD_REQUEST
                raise operation.ex(
                    f"No field value found matching '{choice}'. Choices are: {', '.join(choices)}"
                )
        return choice

    def op_set(self, operation: Operation):
        v = operation.variables
        path = v["path"]
        value = v["value"]

        field = self.check_field(operation, path[0])

        value = self.check_field_choice(operation, field, value)

        t = self.get()
        t.do_set_field(self.owner, field, value)

        if operation.actor != self.owner:
            self.msg(
                f"{operation.actor} changed your {t} {field} to: {value}",
                from_obj=operation.actor,
            )
            staff_alert(
                f"{operation.actor} changed {self.owner}'s {t} {field} to: {value}",
                senders=operation.actor,
            )
        operation.results[
            "message"
        ] = f"{t} {field} of {self.owner} was changed to: {value}"


class StatHandler(BaseHandler):
    min_value = 0
    max_value = 10
    stat_category: str = None
    stat_model = Stat
    rank_model = StatRank
    reverse_relation = "stats"
    options = ("set",)

    def _get_reverse(self):
        return getattr(self.owner.sheet, self.reverse_relation)

    def all(self):
        return {
            (srank.stat.name, srank.context): srank
            for srank in self._get_reverse().filter(stat__category=self.stat_category)
        }

    def op_set(self, operation: Operation):
        v = operation.variables
        path = v["path"]
        value = v["value"]

        stat_name, context = self.parse_context(operation, path[0])
        rating = self.check_rating(operation, stat_name, context, value)
        stat = self.check_stat(operation, stat_name)
        srank = self.check_srank(operation, stat, context)
        operation.variables["srank"] = srank
        operation.variables["srank_before"] = srank.value

        if self.remove_zero and value <= 0 and self.should_delete(srank):
            self.delete(operation, srank)
        else:
            srank.value = rating

        self.announce_op_set(operation)

    def announce_op_set(self, operation: Operation):
        pass

    def op_rank(self, operation: Operation):
        v = operation.variables
        path = v["path"]
        value = v["value"]

        stat_name, context = self.parse_context(operation, path[0])
        rating = self.check_rating(operation, stat_name, context, value)
        stat = self.check_stat(operation, stat_name)
        srank = self.check_srank(operation, stat, context, partial=True)
        operation.variables["srank"] = srank
        operation.variables["srank_before"] = srank.value

        if self.remove_zero and value <= 0 and self.should_delete(srank):
            self.delete(operation, srank)
        else:
            srank.value = rating

        self.announce_op_rank(operation)

    def announce_op_rank(self, operation: Operation):
        pass

    def op_context(self, operation: Operation):
        v = operation.variables
        path = v["path"]
        value = v["value"]

        stat_name, context = self.parse_context(operation, path[0])
        stat = self.check_stat(operation, stat_name)
        srank = self.check_srank(operation, stat, context, partial=True)
        operation.variables["srank"] = srank

        new_context = self.check_context(operation, stat_name, value)

        opposing = (
            self._get_reverse()
            .filter(stat=srank.stat, context__iexact=new_context)
            .first()
        )
        if opposing and opposing != srank:
            raise operation.ex(
                f"{self.render_rank(srank)} cannot be renamed to {new_context} because {self.render_rank(opposing)} already has that context."
            )
        operation.variables["context_before"] = srank.context
        srank.context = new_context

        self.announce_op_context(operation)

    def announce_op_context(self, operation: Operation):
        pass

    def op_describe(self, operation: Operation):
        v = operation.variables
        path = v["path"]
        value = v["value"]

        stat_name, context = self.parse_context(operation, path[0])
        stat = self.check_stat(operation, stat_name)
        srank = self.check_srank(operation, stat, context, partial=True)
        operation.variables["srank"] = srank
        operation.variables["description_before"] = srank.description

        srank.description = value

        self.announce_op_describe(operation)

    def announce_op_describe(self, operation: Operation):
        pass

    def delete(self, operation: Operation, srank: StatRank) -> str:
        if not self.should_delete(srank):
            raise operation.ex(f"{srank} cannot be deleted.")
        operation.variables["deleted"] = True

    def at_post_operation(self, operation):
        if srank := operation.variables.get("srank", None):
            if operation.variables.get("deleted", False):
                srank.delete()
            else:
                srank.save()

    def get_choices(self) -> list[str]:
        pass

    def check_stat(self, operation, name: str):
        choice = self.get_choice(operation, name)
        stat, created = self.stat_model.objects.get_or_create(
            category=self.stat_category, name=choice
        )
        return stat

    def check_srank(
        self, operation, stat, context: str, partial: bool = False
    ) -> StatRank:
        r = self._get_reverse()
        if partial:
            candidates = r.filter(stat__category=self.stat_category)
            if context:
                candidates = candidates.exclude(context="")
                if not candidates:
                    raise operation.ex(
                        f"No {self.singular_name} found matching '{context}'."
                    )
                if not (srank := partial_match(context, candidates)):
                    raise operation.ex(
                        f"No {self.singular_name} found matching '{context}'. Choices are: {', '.join(candidates)}"
                    )
                return srank
            else:
                candidates = candidates.filter(context="")
                if not candidates:
                    raise operation.ex(
                        f"No {self.singular_name} found matching '{stat}'."
                    )
                if not (srank := candidates.first()):
                    raise operation.ex(
                        f"No {self.singular_name} found matching '{stat}'."
                    )
                return srank

        if not (srank := r.filter(stat=stat, context__iexact=context).first()):
            srank, srank_created = r.get_or_create(stat=stat, context=context)
        else:
            srank.context = context
        return srank

    def should_delete(self, srank) -> bool:
        return True


class AdvantageHandler(StatHandler):
    choices = settings.STORYTELLER_ADVANTAGES
    stat_category = "Advantages"
    plural_name = "Advantages"
    singular_name = "Advantage"
    name = "Advantages"
    options = ("set",)

    def get_choice(self, operation, entry: str) -> str:
        choice = super().get_choice(operation, entry)
        if choice == "Power":
            return self.owner.st_template.get().power_stat
        return choice


class AttributeHandler(StatHandler):
    choices = settings.STORYTELLER_ATTRIBUTES
    stat_category = "Attributes"
    plural_name = "Attributes"
    singular_name = "Attribute"
    name = "Attributes"
    options = settings.STORYTELLER_ATTRIBUTE_OPTIONS


class MeritHandler(StatHandler):
    stat_category = "Merits"
    name = "Merits"
    options = ("set", "delete", "rank", "rename", "describe")
    use_context = True
    dynamic_choices = True


class SpecialtyHandler(MeritHandler):
    choices = settings.STORYTELLER_SKILLS
    stat_category = "Specialties"
    plural_name = "Specialties"
    singular_name = "Specialty"
    max_value = 1
    remove_zero = True
    name = "Specialties"
    options = ("set", "remove", "rank", "delete", "rename")


class FlawHandler(MeritHandler):
    stat_category = "Flaws"
    name = "Flaws"


class BackgroundHandler(MeritHandler):
    stat_category = "Backgrounds"
    name = "Backgrounds"


class PowerHandler(BaseHandler):
    plural_name = None
    singular_name = None
    options = (
        "add",
        "remove",
        "delete",
    )
    family = None

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
                f"No {self.render_name()} category found matching '{name}'. Choices are: {', '.join(self.categories.keys())}"
            )
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
                f"No {category} {self.plural_name} subcategory found matching '{name}'. Choices are: {', '.join(choices)}"
            )

        return subcategory

    def add(self, category: str, subcategory: str, name: str, value: int = 1):
        return self.do_base(category, subcategory, name, value, self.do_add)

    def remove(self, category: str, subcategory: str, name: str, value: int = 1):
        return self.do_base(category, subcategory, name, value, self.do_remove)

    def make_key(self, category: str, subcategory: str) -> str:
        return f"{category}:{subcategory}"

    def check_name(self, category: str, subcategory: str, name: str) -> str:
        name = validate_name(
            name, thing_type=f"{category} {subcategory} {self.plural_name}"
        )
        return dramatic_capitalize(name)

    def do_base(
        self, category: str, subcategory: str, name: str, value: int, method: callable
    ) -> str:
        found_category = self.get_category(category)
        found_subcategory = self.get_subcategory(found_category, subcategory)
        found_name = self.check_name(found_category, found_subcategory, name)
        try:
            value = int(value)
        except ValueError:
            raise ValueError(f"Value '{value}' is not an integer.")
        power, created = Power.objects.get_or_create(
            family=self.family,
            category=category,
            subcategory=subcategory,
            name=found_name,
        )
        rank, rank_created = self.owner.stdb_powers.get_or_create(power=power)
        return method(rank, value)

    def render_rank(self, rank: PowerRank) -> str:
        return f"{rank.power.category} {rank.power.subcategory} {self.singular_name}: {rank.power.name}"

    def render_new_value(self, rank: PowerRank, before: int) -> str:
        return f"{self.render_rank(rank)} is now rated at: {rank.value} {self.render_purchases(rank.value)} (was {before})"

    def render_delete(self, rank: PowerRank, before: int) -> str:
        return f"{self.render_rank(rank)} was removed (was {before} {self.render_purchases(before)})"

    def do_add(self, rank: PowerRank, value: int) -> str:
        before = rank.value
        rank.value += value
        rank.save()
        return self.render_new_value(rank, before)

    def do_remove(self, rank: PowerRank, value: int) -> str:
        before = rank.value
        rank.value -= value
        if rank.value <= 0:
            message = self.render_delete(rank, before)
            power = rank.power
            rank.delete()
            if not power.ranks.all().count():
                power.delete()
            return message
        else:
            rank.save()
            return self.render_new_value(rank, before)

    def prepare_args(self, path, value, method) -> list:
        if not len(path) == 2:
            raise ValueError(
                f"Invalid path for {self.singular_name}. Need <category>|<subcategory>."
            )
        return path + [value]


class CustomPowerHandler(BaseHandler):
    stat_category: str = None
    stat: str = None
    singular_name: str = None
    options = ("add", "remove")

    def add(
        self, stat_name: str, stat_context: str, power_name: str, value: int = 1
    ) -> str:
        return self.do_base(stat_name, stat_context, power_name, value, self.do_add)

    def remove(
        self, stat_name: str, stat_context: str, power_name: str, value: int = 1
    ) -> str:
        return self.do_base(stat_name, stat_context, power_name, value, self.do_remove)

    def check_name(self, stat_name: str) -> Stat:
        candidates = self.owner.stdb_stats.filter(
            stat__category=self.stat_category, stat__name=self.stat
        ).exclude(context="")
        if not (stat := partial_match(stat_name, candidates)):
            raise ValueError(
                f"No {self.singular_name} found matching '{stat_name}'. Choices are: {', '.join(candidates)}"
            )
        return stat

    def check_context(self, stat: Stat, stat_context: str) -> StatRank:
        if not stat_context:
            raise ValueError(f"No {self.singular_name} context given.")
        if not (
            candidates := self.owner.stdb_stats.filter(stat=stat).exclude(content="")
        ):
            raise ValueError(f"No {self.stat_category} variations found for {stat}.")
        if not (srank := partial_match(stat_context, candidates)):
            raise ValueError(
                f"No {self.singular_name} context found matching '{stat_context}'. Choices are: {', '.join(candidates)}"
            )
        return srank

    def do_base(
        self,
        stat_name: str,
        stat_context: str,
        power_name: str,
        value: int,
        method: callable,
    ) -> str:
        stat = self.check_name(stat_name)
        srank = self.check_context(stat, stat_context)
        power_name = validate_name(power_name, thing_type=self.singular_name)
        try:
            value = int(value)
        except ValueError:
            raise ValueError(f"Value '{value}' is not an integer.")
        if not (cpower := srank.powers.filter(name=power_name).first()):
            cpower, cpower_created = srank.powers.get_or_create(name=power_name)
        else:
            cpower.name = power_name
        return method(cpower, value)

    def render_rank(self, rank: CustomPower) -> str:
        return f"{rank.stat.context} {self.singular_name}: {rank.name}"

    def render_new_value(self, rank: CustomPower, before: int) -> str:
        return f"{self.render_rank(rank)} is now rated at: {rank.value} {self.render_purchases(rank.value)} (was {before})"

    def render_delete(self, rank: CustomPower, before: int) -> str:
        return f"{self.render_rank(rank)} was removed (was {before} {self.render_purchases(before)})"

    def do_add(self, cpower: CustomPower, value: int):
        before = cpower.value
        cpower.value += value
        cpower.save()
        return self.render_new_value(cpower, before)

    def do_remove(self, cpower: CustomPower, value: int):
        before = cpower.value
        cpower.value -= value
        if cpower.value <= 0:
            message = self.render_delete(cpower, before)
            cpower.delete()
            return message
        else:
            cpower.save()
            return self.render_new_value(cpower, before)


class StatPowerHandler(BaseHandler):
    stat_category: str = None
    singular_name: str = None
    options = ("add", "remove")

    def add(self, stat_name: str, power_name: str, value: int = 1) -> str:
        return self.do_base(stat_name, power_name, value, self.do_add)

    def remove(self, stat_name: str, power_name: str, value: int = 1) -> str:
        return self.do_base(stat_name, power_name, value, self.do_remove)

    def check_name(self, stat_name: str) -> Stat:
        candidates = Stat.objects.filter(category=self.stat_category)
        if not (stat := partial_match(stat_name, candidates)):
            raise ValueError(
                f"No {self.singular_name} found matching '{stat_name}'. Choices are: {', '.join(candidates)}"
            )
        return stat

    def do_base(
        self, stat_name: str, power_name: str, value: int, method: callable
    ) -> str:
        stat = self.check_name(stat_name)
        power_name = validate_name(power_name, thing_type=self.singular_name)
        try:
            value = int(value)
        except ValueError:
            raise ValueError(f"Value '{value}' is not an integer.")
        if not (spower := stat.powers.filter(name=power_name).first()):
            spower, spower_created = stat.powers.get_or_create(name=power_name)
        if not (cpower := spower.powers.filter(character=self.owner).first()):
            cpower, cpower_created = spower.powers.get_or_create(character=self.owner)
        return method(cpower, value)

    def render_rank(self, rank: StatPowerRank) -> str:
        return f"{rank.power.stat} {self.singular_name}: {rank.name}"

    def render_new_value(self, rank: StatPowerRank, before: int) -> str:
        return f"{self.render_rank(rank)} is now rated at: {rank.value} {self.render_purchases(rank.value)} (was {before})"

    def render_delete(self, rank: StatPowerRank, before: int) -> str:
        return f"{self.render_rank(rank)} was removed (was {before} {self.render_purchases(before)})"
