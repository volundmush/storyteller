import typing
import storyteller
from django.conf import settings
from athanor.utils import partial_match, validate_name, format_for_nobody, staff_alert
from .utils import dramatic_capitalize
from .models import (
    Stat,
    StatRank,
    Power,
    PowerRank,
    StatPowerRank,
    CustomPower,
)

_OP_MAP = {
    "set": "set",
    "rank": "rank",
    "add": "add",
    "remove": "remove",
    "tag": "add_tag",
    "untag": "remove_tag",
    "delete": "delete",
    "describe": "describe",
    "rename": "rename",
}


class BaseHandler:
    plural_name = None
    singular_name = None
    remove_zero = False
    min_value = 0
    max_value = 10
    system_name = "SHEET"
    choices: list[str] = None
    options: tuple[str] = tuple()
    name: str = "Handler"
    operation_map = _OP_MAP
    dynamic_choices = False
    use_context = False
    enforce_context = False

    def __init__(self, owner):
        self.owner = owner

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name} ({self.owner})>"

    def render_purchases(self, number) -> str:
        return f"Purchase{'' if number == 1 else 's'}"

    def get_choices(self) -> list[str]:
        return list(self.choices)

    def get_choice(self, entry: str) -> str:
        if self.dynamic_choices:
            return dramatic_capitalize(
                validate_name(entry, thing_type=self.singular_name)
            )
        if not (choices := self.get_choices()):
            raise ValueError(f"No {self.singular_name} choices found.")
        if not entry:
            raise ValueError(f"No {self.singular_name} name given.")
        if not (choice := partial_match(entry, choices)):
            raise ValueError(
                f"No {self.singular_name} found matching '{entry}'. Choices are: {', '.join(choices)}"
            )
        return choice

    def check_context(self, name: str, context: str) -> str:
        context = context.strip()
        if context:
            context = validate_name(context, thing_type=f"{self.singular_name} Context")
        return context

    def check_tag(self, name: str, context: str, tag: str) -> str:
        tag = validate_name(tag, thing_type=f"{self.singular_name} Tag")
        return dramatic_capitalize(tag)

    def parse_context(self, name: str) -> tuple[str, str]:
        """
        Given a name such as "Artifact" or "Artifact: Grand Daiklave", splits it into a tuple like ["Artifact", ""] or
        ["Artifact", "Grand Daiklave"].

        Args:
            name: The name to parse.

        Returns:
            A tuple of [category, context]
        """
        if not name:
            raise ValueError(f"No {self.singular_name} name given.")

        if ":" in name and not (self.use_context or self.enforce_context):
            raise ValueError(f"{self.singular_name} cannot have a context.")

        if ":" in name:
            category, context = [n.strip() for n in name.split(":", 1)]
        else:
            if self.enforce_context:
                raise ValueError(f"{self.singular_name} must have a context.")
            category = name
            context = ""
        category = validate_name(category, thing_type=self.singular_name)
        if context:
            context = self.check_context(category, context)

        return category, context

    def check_rating(self, name: str, context: str, value: int):
        # now coerce value to an int...
        if not isinstance(value, int) and not value:
            raise ValueError(f"No value given for {name} {self.singular_name}.")
        try:
            rating = int(value) if not isinstance(value, int) else value
        except ValueError:
            raise ValueError(f"Value '{value}' is not an integer.")

        if rating < self.min_value:
            if self.remove_zero and rating == 0:
                rating = 0
            else:
                raise ValueError(
                    f"Value '{rating}' is less than the minimum value of {self.min_value}."
                )
        if rating > self.max_value:
            raise ValueError(
                f"Value '{rating}' is greater than the maximum value of {self.max_value}."
            )
        return rating

    def prepare_args(self, path, value, method) -> list:
        return []

    def prepare_kwargs(self, path, value, method) -> dict:
        return {}

    def do_operation(
        self,
        user: "DefaultCharacter",
        path: list[str],
        value: str,
        operation: str,
        do_announce: bool = True,
    ):
        try:
            if not (method := self.operation_map.get(operation, None)):
                raise Exception(f"Invalid operation: {operation}.")
            call_method = getattr(self, method)
            args = self.prepare_args(path, value, operation)
            kwargs = self.prepare_kwargs(path, value, operation)
            result = call_method(*args, **kwargs)
        except ValueError as err:
            self.error(user, str(err))
            return
        except Exception as err:
            self.error(user, str(err))
            self.error(user, f"Something went very wrong. Please alert staff.")
            return

        if do_announce:
            self.announce(user, f"$Your() {result}")

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


class TemplateHandler(BaseHandler):
    options = ("set",)
    name = "Templates"
    operation_map = {"set": "set_template"}

    def __init__(self, owner):
        super().__init__(owner)
        if not hasattr(owner, "stdb_template"):
            temp = self.choices.get(settings.STORYTELLER_DEFAULT_TEMPLATE)
            temp.change(owner)

    def get_choices(self) -> list[str]:
        return list(storyteller.TEMPLATES.values())

    def get(self):
        return self.choices.get(self.owner.stdb_template.template, None)

    def get_field(self, field: str) -> typing.Optional[str]:
        if found := self.owner.stdb_fields.filter(field__iexact=field).first():
            return found.value
        return None

    def set_field(self, field: str, value: str):
        field_name, value_formatted = self.get().set_field(self.owner, field, value)
        return f"{self.get()} {field_name} was set to: {value_formatted}"

    def set_template(self, name: str):
        template = self.get_choice(name)
        t = template.change(self.owner)
        return f"Template was changed to: {t}"

    def prepare_args(self, path, value, method) -> list:
        return [value]


class FieldHandler(TemplateHandler):
    name = "Fields"
    operation_map = {"set": "set_field"}

    def prepare_args(self, path, value, method) -> list:
        if not len(path) == 1:
            raise ValueError(f"Invalid path for {self.singular_name}. Need <field>.")
        return path + [value]


class StatHandler(BaseHandler):
    stat_category: str = None

    def all(self):
        return {
            (srank.stat.name, srank.context): srank
            for srank in self.owner.stdb_stats.filter(stat__category=self.stat_category)
        }

    def get_stat(self, name: str) -> Stat:
        choice = self.get_choice(name)
        stat, created = Stat.objects.get_or_create(
            category=self.stat_category, name=choice
        )
        return stat

    def get_srank(self, stat: Stat, context: str, partial: bool = False) -> StatRank:
        if partial:
            candidates = self.owner.stdb_stats.filter(stat__category=self.stat_category)
            if context:
                candidates = candidates.exclude(context="")
                if not candidates:
                    raise ValueError(
                        f"No {self.singular_name} found matching '{context}'."
                    )
                if not (srank := partial_match(context, candidates)):
                    raise ValueError(
                        f"No {self.singular_name} found matching '{context}'. Choices are: {', '.join(candidates)}"
                    )
                return srank
            else:
                candidates = candidates.filter(context="")
                if not candidates:
                    raise ValueError(
                        f"No {self.singular_name} found matching '{stat}'."
                    )
                if not (srank := candidates.first()):
                    raise ValueError(
                        f"No {self.singular_name} found matching '{stat}'."
                    )
                return srank

        if not (
            srank := self.owner.stdb_stats.filter(
                stat=stat, context__iexact=context
            ).first()
        ):
            srank, srank_created = self.owner.stdb_stats.get_or_create(
                stat=stat, context=context
            )
        else:
            srank.context = context
        return srank

    def should_delete(self, srank) -> bool:
        return True

    def render_new_value(self, srank: StatRank, before: int) -> str:
        return f"{srank} {self.singular_name} is now rated at: {srank.value} (was {before})"

    def render_remove_stat(self, srank: StatRank, before: int) -> str:
        return f"{srank} {self.singular_name} was removed (was {before})"

    def prepare_args(self, path, value, operation: str) -> list:
        # The first path element is the name of the stat.
        stat_name_full = "" if not path else path[0]
        stat_name, context = self.parse_context(stat_name_full)
        if operation in ("set", "rank", "tag", "add"):
            stat_found = self.get_choice(stat_name)
            value_check = (
                self.check_rating(stat_found, context, value)
                if operation in ("set", "rank")
                else self.check_tag(stat_found, context, value)
            )

            # When using this path, the stat is to be created if it doesn't exist.
            partial = (
                False
                if operation in ("set", "add")
                else True
                if self.dynamic_choices
                else False
            )
            stat = self.get_stat(stat_found) if not partial else stat_found
            srank = self.get_srank(stat, context, partial=partial)
            return [srank, value_check]
        else:
            # all other operations can only be done on things which definitely exist.
            srank = self.get_srank(stat_name, context, partial=True)
            if operation in ("delete"):
                return [srank]
            value_check = (
                self.check_rating(srank.stat.name, context, value)
                if operation in ("set", "rank")
                else self.check_tag(srank.stat.name, context, value)
                if operation in ("tag",)
                else value
            )
            return [srank, value_check]

    def set(self, srank: StatRank, value: int) -> str:
        before = srank.value

        if self.remove_zero and value <= 0 and self.should_delete(srank):
            return self.delete(srank)

        srank.value = value
        srank.save()
        return self.render_new_value(srank, before)

    rank = set

    def remove(self, srank: StatRank, value: int) -> str:
        return self.set(srank, srank.value - value)

    def add(self, srank: StatRank, value: int) -> str:
        return self.set(srank, srank.value + value)

    def add_tag(self, srank: StatRank, tag: str) -> str:
        tags = srank.data.get("tags", list())
        if tag in tags:
            raise ValueError(f"{self.render_rank(srank)} already has the tag: {tag}")
        tags.append(tag)
        srank.data["tags"] = tags
        srank.save()
        return f"{self.render_rank(srank)} {self.singular_name} is now tagged: {tag}"

    def remove_tag(self, srank: StatRank, tag: str) -> str:
        tags = srank.data.get("tags", list())
        if tag not in tags:
            raise ValueError(f"{self.render_rank(srank)} does not have the tag: {tag}")
        tags.remove(tag)
        srank.data["tags"] = tags
        srank.save()
        return (
            f"{self.render_rank(srank)} {self.singular_name} is no longer tagged: {tag}"
        )

    def rename(self, srank: StatRank, context: str) -> str:
        if not context:
            raise ValueError(f"No new name given for {srank}.")
        opposing = self.owner.stdb_stats.filter(
            stat=srank.stat, context__iexact=context
        ).first()
        if opposing and opposing != srank:
            raise ValueError(
                f"{self.render_rank(srank)} cannot be renamed to {context} because {self.render_rank(opposing)} already has that context."
            )
        old_name = srank.context
        srank.context = context
        srank.save()
        return f"{self.render_rank(srank)} context changed to to {context}"

    def delete(self, srank: StatRank) -> str:
        if not self.should_delete(srank):
            raise ValueError(f"{srank} cannot be deleted.")
        message = f"{self.render_rank(srank)} was deleted"
        srank.delete()
        return message

    def describe(self, srank: StatRank, text: str) -> str:
        old_text = srank.data.get("describe", "")
        srank.data["describe"] = text
        srank.save()
        return f"{self.render_rank(srank)} description changed from '{old_text}' to '{text}'"


class AdvantageHandler(StatHandler):
    choices = settings.STORYTELLER_ADVANTAGES
    stat_category = "Advantages"
    plural_name = "Advantages"
    singular_name = "Advantage"
    name = "Advantages"
    options = ("set",)

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
