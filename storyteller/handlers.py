"""
This module holds the StorytellerHandler base classes which do the heavy lifting of manipulating the sheet data.

Each Game object maintains its own list of handlers, which are usually loaded on its init via setup_handlers().

The Handlers are loaded and accessed directly by the sheet commad's edit and display features.

The handlers here are base implementations styled after World of Darkness and Exalted, though with some creativity they
could likely be used for many other things.
"""
import typing
import storyteller
import math
from collections import defaultdict
from django.conf import settings
from evennia.utils.ansi import ANSIString
from athanor.utils import (
    partial_match,
    validate_name,
    format_for_nobody,
    staff_alert,
    Operation,
)
from .utils import dramatic_capitalize
from .models import (
    SheetInfo,
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

    This is an Abstract base class. Do not use directly.
    """

    api_access = True
    sheet_render = True
    system_name = "SHEET"
    name: str = "Handler"
    options: set[str] = set()
    min_path_length = 1
    path_format = ""
    load_order = 0
    context_delim = ":"
    context_delim_display = ": "

    def __init__(self, owner, game, base):
        self.owner = owner
        self.game = game
        self.base = base

    def __str__(self):
        """
        Handlers all have names, which is how they can be identified for the partial match search in the sheet editor.

        Returns:
            The name of the handler.
        """
        return self.name

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name} ({self.owner})>"

    def msg(self, message: str, from_obj=None):
        self.owner.system_send(self.system_name, message, mapping={}, from_obj=from_obj)

    def permission_check(self, operation: Operation):
        # TODO: Implement permission checks.
        pass

    def modify_path(self, path):
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
            self.modify_path(path)
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

    def at_template_change(self):
        pass

    def at_game_enter(self):
        pass

    def at_game_leave(self):
        pass

    def send_message(self, operation, message):
        actor = operation.actor

        self.owner.msg(f"Your {message}", from_obj=actor)

        if actor != self.owner:
            actor.msg(f"{self.owner}'s {message}", from_obj=actor)
            staff_alert(f"{self.owner}'s {message}", senders=actor)

        # operation.results["message"] = f"{self.owner}'s {message}"

    def render_context(self, name, context):
        return f"{name}: {context}" if context else name

    def render_help_extra(self, lines: list[str]):
        self.render_help_choices(lines)

    def render_help_choices(self, lines):
        if (get := getattr(self, "get_choices", None)) and callable(get):
            if choices := get():
                lines.append(f"  |wChoices|n: {', '.join([str(x) for x in choices])}")

    def render_help_header(self, lines: list[str]):
        lines.append(f"|c{self.name}:|n")

    def render_help(self, lines: list[str]):
        self.render_help_header(lines)
        lines.append(f"  |wOperations|n: {', '.join(self.options)}")
        self.render_help_extra(lines)

    def render_sheet(self, viewer, width: int, lines: list[ANSIString]):
        pass

    def get_color(self, color):
        t = self.template()
        colors = getattr(t, "colors", dict()).copy()
        overrides = getattr(t, "color_overrides", dict())
        colors.update(overrides)
        return colors.get(color, "n")

    def get_symbol(self, tier):
        t = self.template()
        symbols = getattr(t, "tier_symbols", dict()).copy()
        overrides = getattr(t, "tier_symbol_overrides", dict())
        symbols.update(overrides)
        return symbols.get(tier, "+")

    def render_sheet_header(self, viewer, width, lines, name=None):
        available_width = width - 2
        t = self.template()
        border = self.get_color("border")
        if not name:
            lines.append(ANSIString(f"|{border}" + "}" + "-" * available_width + "{|n"))
            return
        slash = self.get_color("slash")
        title = self.get_color("title")
        center = f"|{slash}/|n" + f"|{title}{name}|n" + f"|{slash}/|n"

        available_width -= len(ANSIString(center))
        divided = available_width / 2
        left_len = math.floor(divided)
        right_len = math.ceil(divided)

        left = ("-" * left_len) + "|n"
        right = "-" * right_len
        combined = f"|{border}" + "}" + left + center + f"|{border}" + right + "{|n"
        lines.append(ANSIString(combined))

    def tri_split_width(self, width) -> tuple[int]:
        available_width = width
        divided = available_width / 3
        left_len = math.floor(divided)
        right_len = math.ceil(divided)
        center_len = available_width - left_len - right_len
        return left_len, center_len, right_len

    def render_sheet_triheader(self, viewer, width, lines, names):
        if not names:
            self.render_sheet_header(viewer, width, lines)
            return
        if not len(names) == 3:
            return
        title = self.get_color("title")
        slash = self.get_color("slash")
        rendered_names = [
            ANSIString(f"|{slash}/|n|{title}{name}|n|{slash}/|n") for name in names
        ]
        widths = self.tri_split_width(width - 2)
        combined_names = list()
        border = self.get_color("border")
        for i, name in enumerate(rendered_names):
            divided = (widths[i] - len(name)) / 2
            left_len = math.floor(divided)
            right_len = math.ceil(divided)
            left = ANSIString(f"|{border}" + ("-" * left_len) + "|n")
            right = ANSIString(f"|{border}" + ("-" * right_len) + "|n")
            combined_names.append(ANSIString("").join([left, name, right]))
        combined = (
            ANSIString(f"|{border}" + "}")
            + ANSIString("").join(combined_names)
            + ANSIString(f"|{border}" + "{|n")
        )
        lines.append(combined)

    def render_sheet_tricolumns(self, viewer, width, lines, columns):
        if not columns:
            return
        if not len(columns) == 3:
            return
        widths = self.tri_split_width(width - 4)
        border = self.get_color("border")

        # The number of total lines equals the max() of max() of all columns.
        max_lines = max([len(column) for column in columns])

        # Pad the columns to simplify our logic. This should make every column
        # have the same number of lines.
        for i, col in enumerate(columns):
            while len(col) < max_lines:
                col.append(ANSIString(" " * widths[i]))

        border = self.get_color("border")

        for i in range(max_lines):
            b = f"|{border}|||n"
            left = columns[0][i]
            center = columns[1][i]
            right = columns[2][i]
            lines.append(b + b.join([left, center, right]) + b)

    def render_sheet_tabular(
        self,
        viewer,
        width,
        lines,
        items: list[ANSIString],
        element_width=23,
        left_pad=0,
        between_pad=1,
    ):
        """
        This is meant to render a series of items and generate a display sorta like this.

        | +Awareness..........*** +Bureaucracy........*** +Craft............*****    |
        |  Integrity..........*** +Investigation......*** +Linguistics........***    |
        | +Lore.............***** +Medicine...........*** +Occult...........*****    |
        | +Presence............** +Survival...........***                            |

        """
        fits = [item for item in items if len(item) <= element_width]
        no_fit = [item for item in items if item not in fits]

        available_width = width - 2 - left_pad
        elements_per_line = 1
        for possible_elements in range(1, 11):
            elements_per_line = possible_elements
            pad_needed = possible_elements - 1 * between_pad
            if (possible_elements * element_width) + pad_needed > available_width:
                elements_per_line -= 1
                break

        # Let's gather fits into a list of lists, where each list is a line.
        # It's fine if the last line has fewer than elements_per_line elements.
        lines_of_fits = list()
        while fits:
            lines_of_fits.append(fits[:elements_per_line])
            fits = fits[elements_per_line:]

        border = self.get_color("border")

        # Now we'll use ANSIString's join method to join each line of fits into a single line.
        for line_items in lines_of_fits:
            line = ANSIString(" " * between_pad).join(line_items)
            filler = ANSIString(" " * (available_width - len(line)))
            out_line = (
                ANSIString(f"|{border}|||n")
                + ANSIString(" " * left_pad)
                + line
                + filler
                + ANSIString(f"|n|{border}|||n")
            )
            lines.append(out_line)

        for item in no_fit:
            filler = ANSIString(" " * (element_width - len(item)))
            out_line = (
                ANSIString(f"|{border}|||n")
                + item
                + filler
                + ANSIString(f"|n|{border}|||n")
            )
            lines.append(out_line)

    def render_sheet_stat(
        self, viewer, width, stat, tiers=False, context_delim=": ", item_width=23
    ) -> ANSIString:
        available_width = item_width

        tier_color = self.get_color(f"tier_{stat.tier}")

        tier_symbol = ANSIString(
            f"|{tier_color}{self.get_symbol(stat.tier)}|n"
            if tiers and stat.tier
            else " "
            if tiers
            else ""
        )

        stat_color = self.get_color("stat")

        stat_name = ANSIString(
            f"|{stat_color}" + context_delim.join([stat.stat.name, stat.context])
            if stat.context
            else stat.stat.name + "|n"
        )

        tier_name = (
            ANSIString("").join([tier_symbol, stat_name])
            if tiers
            else ANSIString(stat.stat.name)
        )

        available_width -= len(tier_name)
        available_width -= stat.value
        stars = ""

        if available_width <= 0:
            available_width += stat.value
            stars = str(stat.value)
            available_width -= len(stars)
        else:
            stars = "*" * stat.value

        star_color = self.get_color("star")

        stars = ANSIString(f"|{star_color}{stars}|n")

        dot_color = self.get_color("dot")

        dots = ANSIString(f"|{dot_color}{'.' * available_width}|n")

        return tier_name + dots + stars

    def render_sheet_stats(
        self,
        viewer,
        width,
        lines,
        stats,
        name=None,
        context_delim=": ",
        item_width=23,
    ):
        self.render_sheet_header(viewer, width, lines, name or self.name)

        items = list()

        tiers = "tier" in self.options

        for stat in stats:
            items.append(
                self.render_sheet_stat(
                    viewer,
                    width,
                    stat,
                    tiers=tiers,
                    context_delim=self.context_delim_display,
                    item_width=item_width,
                )
            )

        self.render_sheet_tabular(
            viewer, width, lines, items, between_pad=1, left_pad=1
        )


class GameHandler(RawHandler):
    """
    The GameHandler is a special handler that is used to change the Game of a character.
    It is usually found on character.ndb.story, and is accessed by storyteller.utils.get_story(character)
    which handles a get-or-create approach to the handler.

    The GameHandler still considers itself as a Handler despite being the 'root'.

    Note that while a character's game CAN be changed in-play, doing so is highly destructive, it
    necessitates cleaning a sheet.
    """

    name = "Game"
    options = ("set",)
    min_path_length = 0
    load_order = -999999999

    def render_help_header(self, lines: list[str]):
        lines.append(f"|c{self.name}:|n (Currently: |w{self.game}|n)")

    def render_help_extra(self, lines: list[str]):
        super().render_help_extra(lines)
        lines.append(
            f"  |rWARNING|n: Changing a character's game will wipe their sheet!"
        )

    def __init__(self, owner):
        super().__init__(owner, None, self)
        self.handlers = [self]
        self.handlers_dict = {self.name: self}
        self.loaded = False

    def reload(self):
        self.loaded = False
        self.game = None
        self.load(reloading=True)

    def load(self, reloading=False):
        if self.loaded:
            return
        self.loaded = True
        created = False
        if not hasattr(self.owner, "sheet"):
            self.game = storyteller.GAMES.get(settings.STORYTELLER_DEFAULT_GAME, None)
            if not self.game:
                raise ValueError("No default game module found!")
            sheet = SheetInfo.objects.create(
                character=self.owner,
                game=self.game.key,
                template=self.game.default_template,
            )
            sheet.save()
            created = True
        else:
            self.game = storyteller.GAMES.get(self.owner.sheet.game, None)
            if not self.game:
                raise ValueError("No module found for this game!")
        if not (handlers := self.game.get_handlers(self.owner)):
            raise ValueError("No handlers for this game!")
        if reloading:
            for handler in self.handlers:
                handler.at_game_leave()
        self.handlers.clear()
        self.handlers.append(self)
        self.handlers.extend(
            [handler(self.owner, self.game, self) for handler in handlers]
        )
        self.handlers.sort(key=lambda x: x.load_order)
        self.handlers_dict = {handler.name: handler for handler in self.handlers}

        template = self.template()
        if not template:
            raise ValueError("No template found for this game!")
        if created or reloading:
            template.change(self.owner)

        for handler in self.handlers:
            handler.at_load()

        if created or reloading:
            for handler in self.handlers:
                handler.at_game_enter()
            for handler in self.handlers:
                handler.at_template_change()

    def get(self, handler: str):
        if not (handler := partial_match(handler, self.handlers)):
            raise ValueError(
                f"No handler found matching '{handler}'. Choices are: {', '.join(self.handlers)}"
            )
        return handler

    def get_choices(self):
        return list(storyteller.GAMES.values())

    def op_set(self, operation: Operation):
        v = operation.variables
        if not (choices := self.get_choices()):
            raise operation.ex(f"No game choices found.")
        if not (game := partial_match(operation.variables["value"], choices)):
            raise operation.ex(
                f"No game found matching '{operation.variables['value']}'. Choices are: {', '.join([str(x) for x in choices])}"
            )
        if game.key == self.game.key:
            raise operation.ex(f"{self.owner} is already in the {game} game.")
        v["game_before"] = self.game
        v["template_before"] = self.template()
        message = f"Game was changed from {self.game} to: {game}."
        self.send_message(operation, message)
        sheet = self.owner.sheet
        sheet.game = game.key
        sheet.template = game.default_template
        sheet.save()
        self.reload()

    def render_sheet_top(self, viewer, width, lines):
        available_width = width - 6
        divided = available_width / 2
        left_len = math.floor(divided)
        right_len = math.ceil(divided)
        border = self.get_color("border")
        left = ANSIString("  " + f"|{border}" + "." + ("-" * left_len))
        right = ANSIString(("-" * right_len) + ".|n")
        lines.append(left + right)

        available_width = width - 4 - len(settings.SERVERNAME)
        divided = available_width / 2
        left_len = math.floor(divided)
        right_len = math.ceil(divided)
        center = (" " * left_len) + settings.SERVERNAME + (" " * right_len)
        lines.append(ANSIString(f" |{border}/|n" + center + f"|{border}\\|n"))

    def render_sheet_info(self, viewer, width, lines):
        t = self.template()
        available_width = width - 2
        divided = available_width / 2
        widths = [math.floor(divided), math.ceil(divided)]
        columns = t.get_sheet_columns(self.owner)

        max_lines = max([len(column) for column in columns])
        for i, col in enumerate(columns):
            while len(col) < max_lines:
                col.append(" ")

        column_widths = defaultdict(list)
        for i, col in enumerate(columns):
            for line in col:
                if isinstance(line, str):
                    continue
                column_widths[i].append(len(line[0]))

        # Gather the max_column_widths, which will be used to justify text.
        max_column_widths = [max(column_widths[i]) for i in range(len(column_widths))]

        border = self.get_color("border")

        for i in range(max_lines):
            left = columns[0][i]
            if isinstance(left, str):
                left_display = left
            else:
                left_display = left[0].rjust(max_column_widths[0]) + ": " + left[1]
            left_display = left_display.ljust(widths[0])

            right = columns[1][i]
            if isinstance(right, str):
                right_display = right
            else:
                right_display = right[0].rjust(max_column_widths[1]) + ": " + right[1]
            right_display = right_display.ljust(widths[1])
            lines.append(
                ANSIString(
                    f"|{border}|||n" + left_display + right_display + f"|{border}|||n"
                )
            )

        border = self.get_color("border")

    def render_sheet(self, viewer, width: int, lines: list[ANSIString]):
        self.render_sheet_top(viewer, width, lines)
        self.render_sheet_header(viewer, width, lines)
        self.render_sheet_info(viewer, width, lines)


class BaseHandler(RawHandler):
    """
    Abstract base class used to provide a great deal of support utilities for other handlers.
    """

    singular_name = "Stat"
    plural_name = "Stat"

    def format_rank(self, rank):
        return f"|w{rank}|n |c{self.singular_name}|n"

    def should_delete(self, rank) -> bool:
        return False

    def at_post_operation(self, operation):
        v = operation.variables
        if rank := v.get("rank", None):
            if v.get("delete", False):
                rank.delete()
            else:
                rank.save()

    def announce_op_set(self, operation: Operation):
        v = operation.variables
        rank = v["rank"]
        delete = v.get("delete", False)

        if delete:
            message = f"{self.format_rank(rank)} was |wdeleted|n."
        else:
            message = f"{self.format_rank(rank)} was set to: |w{rank.value}|n. (Was |w{v.get('value_before', 0)}|n)"
        self.send_message(operation, message)

    announce_op_rank = announce_op_set

    def check_tag(self, operation, tag: str) -> str:
        tag = validate_name(tag, thing_type="Tag", ex_type=operation.ex)
        return tag.lower()

    def _op_tag(self, operation: Operation, rank, tag):
        v = operation.variables
        tag = self.check_tag(operation, tag)
        if tag in rank.tags:
            raise operation.ex(f"{rank} already has the tag: |w{tag}|n.")
        v["rank"] = rank
        v["tags_before"] = list(rank.tags)
        v["tag_added"] = tag
        rank.tags.append(tag)
        self.announce_op_tag(operation)

    def announce_op_tag(self, operation: Operation):
        v = operation.variables
        rank = v["rank"]
        tag = v["tag_added"]
        message = f"{self.format_rank(rank)} was tagged: |w{tag}|n."
        self.send_message(operation, message)

    def _op_untag(self, operation: Operation, rank, tag):
        v = operation.variables
        tag = self.check_tag(operation, tag)
        if tag not in rank.tags:
            raise operation.ex(
                f"{self.format_rank(rank)} does not have the tag: |w{tag}|n."
            )
        v["rank"] = rank
        v["tags_before"] = list(rank.tags)
        v["tag_removed"] = tag
        rank.tags.remove(tag)
        self.announce_op_untag(operation)

    def announce_op_untag(self, operation: Operation):
        v = operation.variables
        rank = v["rank"]
        tag = v["tag_removed"]
        message = f"{self.format_rank(rank)} was untagged: |w{tag}|n."
        self.send_message(operation, message)

    def _op_tier(self, operation: Operation, rank, tier):
        v = operation.variables
        try:
            tier = int(tier)
        except ValueError:
            raise operation.ex(f"Tier must be an integer.")
        v["rank"] = rank
        v["tier_before"] = rank.tier
        rank.tier = tier
        self.announce_op_tier(operation)

    def announce_op_tier(self, operation: Operation):
        v = operation.variables
        rank = v["rank"]
        before = v["tier_before"]
        message = f"{self.format_rank(rank)} was set to Tier: |w{rank.tier}|n. (Was |w{before}|n)"
        self.send_message(operation, message)

    def check_module(self, operation: Operation, rank, mod):
        mod = validate_name(mod, thing_type="Module", ex_type=operation.ex)
        return dramatic_capitalize(mod)

    def _op_mod(self, operation: Operation, rank, mod):
        v = operation.variables
        v["rank"] = rank
        mod = self.check_module(operation, rank, mod)
        v["mod"] = mod
        if mod in rank.modules:
            v["value_before"] = rank.modules[mod]
            rank.modules[mod] += 1
        else:
            v["value_before"] = 0
            rank.modules[mod] = 1
        self.announce_op_mod(operation)

    def announce_op_mod(self, operation: Operation):
        v = operation.variables
        rank = v["rank"]
        before = v["value_before"]
        mod = v["mod"]
        if before == 0:
            message = f"{self.format_rank(rank)} had a module added: |w{mod}|n."
        else:
            message = f"{self.format_rank(rank)} purchased module again: |w{mod}|n. (Was |w{before}|n)"
        self.send_message(operation, message)

    def _op_unmod(self, operation: Operation, rank, mod):
        v = operation.variables
        v["rank"] = rank
        mod = self.check_module(operation, rank, mod)
        v["mod"] = mod
        if mod not in rank.modules:
            raise operation.ex(f"{rank} does not have the module: |w{mod}|n.")
        v["value_before"] = rank.modules[mod]
        rank.modules[mod] -= 1
        if rank.modules[mod] <= 0:
            del rank.modules[mod]
        self.announce_op_unmod(operation)

    def announce_op_unmod(self, operation: Operation):
        v = operation.variables
        rank = v["rank"]
        before = v["value_before"]
        mod = v["mod"]
        if before == 1:
            message = f"{self.format_rank(rank)} had a module removed: |w{mod}|n."
        else:
            message = f"{self.format_rank(rank)} removed a module: |w{mod}|n. (Was |w{before}|n)"
        self.send_message(operation, message)

    def _op_value(self, operation: Operation, rank, value):
        v = operation.variables
        v["rank"] = rank
        v["value_before"] = rank.value
        rank.value = value
        v["delete"] = self.should_delete(rank)
        if announce := getattr(self, f"announce_op_{operation.operation}", None):
            announce(operation)

    def _op_delete(self, operation: Operation, rank):
        v = operation.variables
        v["value_before"] = rank.value
        rank.value = 0
        if not self.should_delete(rank):
            rank.value = v["value_before"]
            raise operation.ex(f"Entry cannot be deleted.")
        v["delete"] = True
        v["rank"] = rank
        self.announce_op_set(operation)


class _TemplateHandler(RawHandler):
    options = ("set",)
    min_path_length = 0
    sheet_render = False

    def get_choices(self):
        return list(self.game.templates.values())

    def get(self):
        return self.game.templates.get(self.owner.sheet.template, None)

    def get_field(self, field: str) -> typing.Optional[str]:
        if found := self.owner.sheet.fields.filter(field__iexact=field).first():
            return found.value
        return None


class TemplateHandler(_TemplateHandler):
    """
    The TemplateHandler is a bit different from most Handlers. It has one option, "set", which changes the character's
    Template. That being the case, it doesn't need a "path" variable.
    """

    name = "Templates"
    load_order = -1000

    def render_help_header(self, lines: list[str]):
        lines.append(f"|c{self.name}:|n (Currently: |w{self.template()}|n)")

    def render_help_extra(self, lines: list[str]):
        super().render_help_extra(lines)
        lines.append(
            f"  |rWARNING|n: Changing a character's Template may clear sections of their sheet!"
        )

    def at_load(self):
        pass

    def op_set(self, operation: Operation):
        v = operation.variables
        value = v["value"]
        if not (templates := self.get_choices()):
            operation.status = operation.st.HTTP_400_BAD_REQUEST
            raise operation.ex(f"No templates found.")
        if not (template := partial_match(value, templates)):
            operation.status = operation.st.HTTP_400_BAD_REQUEST
            raise operation.ex(
                f"No template found matching '{value}'. Choices are: {', '.join([str(x) for x in templates])}"
            )

        if template.name == self.owner.sheet.template:
            raise operation.ex(f"{self.owner} is already a {template}.")

        v["template_before"] = self.owner.sheet.template
        v["template"] = template.change(self.owner)
        for handler in self.base.handlers:
            handler.at_template_change()
        self.announce_op_set(operation)

    def announce_op_set(self, operation):
        v = operation.variables
        t_b = v["template_before"]
        t = v["template"]
        message = f"|cTemplate|n was changed from |w{t_b}|n to: |w{t}|n."
        self.send_message(operation, message)


class FieldHandler(_TemplateHandler):
    """
    The FieldHandler is used to handle the various fields that a Template can have, and setting them.

    'Fields' is a catch-all term for text fields that are not stats, powers, or merits, which often have a huge
    impact on the character's overall design. For example, a Vampire's Clan, or a Werewolf's Tribe.

    In Exalted, Castes and Aspects are fields, as is a Lunar's Spirit Shape/Totem Animal.

    What fields are available, and what they can be set to, as well as their defaults, are defined on the Template.
    """

    name = "Fields"
    path_format = "<field>"
    load_order = -500

    def render_help_extra(self, lines: list[str]):
        t = self.template()
        lines.append(f"  |wChoices|n:")
        for choice in self.get_choices():
            available = t.get_field_choices(self.owner, choice)
            available_msg = (
                "<anything>" if available is None else f"{', '.join(available)}"
            )
            lines.append(f"    |w{choice}|n: {available_msg}")
            currently = self.get_field(choice)
            if currently:
                lines.append(f"      Currently: |w{currently}|n")

    def get_choices(self):
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
        v["field"] = field
        value = self.check_field_choice(operation, field, value)
        v["value_before"] = self.get_field(field)
        v["value"] = value

        t = self.get()
        t.do_set_field(self.owner, field, value)
        self.announce_op_set(operation)

    def announce_op_set(self, operation):
        v = operation.variables
        field = v["field"]
        value = v["value"]
        value_before = v["value_before"]
        message = f"|c{field}|n was set to: |w{value}|n. (Was |w{value_before}|n)"
        self.send_message(operation, message)


class StatHandler(BaseHandler):
    stat_category: str = None
    stat_model = Stat
    rank_model = StatRank
    reverse_relation = "stats"
    custom_relations: list[str] = list()
    options = ("set",)
    # If remove_zero is True, then a value of 0 will be deleted, unless it has customs.
    # This is used for the set/rank operations.
    remove_zero = False
    # The minimum and maximum values allowed by set/rank operations.
    min_value = 0
    max_value = 10
    # If dynamic_choices is True, then stat/merit names are picked by the player entering them.
    # If not, the available choices are pulled from the get_choices() method, which defaults to
    # self.choices.
    dynamic_choices = False
    # Context is used primarily by the Merit system to distinguish different purchases.
    # But, it can also be used for specialties and similar situations where we need an 'additional field'
    # to distinguish the purchase, like Artifact: The Distaff, or Melee: Swords.
    use_context = False
    # If enforce_context is True, then the context field is required.
    enforce_context = False

    singular_name = None

    def render_help_header(self, lines: list[str]):
        lines.append(f"|c{self.name}:|n (Type: |wStat|n)")

    def render_help_choices(self, lines):
        if self.dynamic_choices:
            lines.append(f"  |wChoices|n: <anything>")
        else:
            lines.append(
                f"  |wChoices|n: {', '.join([str(x) for x in self.get_choices()])}"
            )

    def render_help_extra(self, lines: list[str]):
        super().render_help_extra(lines)
        if self.use_context or self.enforce_context:
            lines.append(
                f"  |wContext|n: {'Required' if self.enforce_context else 'Optional'}"
            )

    def render_sheet(self, viewer, width: int, lines: list[ANSIString]):
        if not (stats := self.all()):
            return
        self.render_sheet_stats(viewer, width, lines, stats)

    @property
    def name(self):
        return self.stat_category

    @property
    def plural_name(self):
        return self.stat_category

    def _get_reverse(self):
        return getattr(self.owner.sheet, self.reverse_relation)

    def clear(self):
        self._get_reverse().filter(stat__category__iexact=self.stat_category).delete()

    def at_game_leave(self):
        self.clear()

    def all(self):
        return self._get_reverse().filter(stat__category__iexact=self.stat_category)

    def get(self, name: str, context: str = "") -> StatRank:
        return (
            self.all().filter(stat__name__iexact=name, context__iexact=context).first()
        )

    def get_choices(self) -> list[str]:
        return getattr(self, "choices", list())

    def get_choice(self, operation, entry: str) -> str:
        if self.dynamic_choices:
            return dramatic_capitalize(
                validate_name(
                    entry, thing_type=self.singular_name, ex_type=operation.ex
                )
            )
        if not (choices := self.get_choices()):
            raise operation.ex(f"No {self.singular_name} choices found.")
        if not entry:
            raise operation.ex(f"No {self.singular_name} name given.")
        if not (choice := partial_match(entry, choices)):
            raise operation.ex(
                f"Nothing found matching '{entry}'. Choices are: {', '.join(choices)}"
            )
        return choice

    def check_context(self, operation, name: str, context: str) -> str:
        context = context.strip()
        if context:
            context = validate_name(
                context,
                thing_type=f"{self.singular_name} Context",
                ex_type=operation.ex,
            )
        return context

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
            raise operation.ex(f"No name given.")

        if ":" in name and not (self.use_context or self.enforce_context):
            raise operation.ex(f"{self.plural_name} cannot have a context.")

        if ":" in name:
            category, context = [n.strip() for n in name.split(":", 1)]
        else:
            if self.enforce_context:
                raise operation.ex(f"{self.plural_name} must have a context.")
            category = name
            context = ""
        category = validate_name(
            category, thing_type=self.singular_name, ex_type=operation.ex
        )
        if context:
            context = self.check_context(operation, category, context)

        return category, context

    def check_rating(self, operation, name: str, context: str, value: int) -> int:
        # now coerce value to an int...
        if not isinstance(value, int) and not value:
            raise operation.ex(
                f"No value given for {self.render_context(name, context)}."
            )
        try:
            rating = int(value) if not isinstance(value, int) else value
        except operation.ex:
            raise operation.ex(f"Value '{value}' is not an integer.")

        if rating < self.min_value:
            raise operation.ex(
                f"Value '{rating}' is less than the minimum value of {self.min_value}."
            )
        if rating > self.max_value:
            raise operation.ex(
                f"Value '{rating}' is greater than the maximum value of {self.max_value}."
            )
        return rating

    def op_set(self, operation: Operation):
        v = operation.variables
        path = v["path"]
        value = v["value"]

        stat_name, context = self.parse_context(operation, path[0])
        rating = self.check_rating(operation, stat_name, context, value)
        srank = self.check_srank(operation, stat_name, context)

        self._op_value(operation, srank, rating)

    def op_rank(self, operation: Operation):
        v = operation.variables
        path = v["path"]
        value = v["value"]

        stat_name, context = self.parse_context(operation, path[0])
        rating = self.check_rating(operation, stat_name, context, value)
        srank = self.check_srank(
            operation, stat_name, context, partial=True, create=False
        )
        self._op_value(operation, srank, rating)

    def op_context(self, operation: Operation):
        v = operation.variables
        path = v["path"]
        value = v["value"]

        stat_name, context = self.parse_context(operation, path[0])
        srank = self.check_srank(
            operation, stat_name, context, partial=True, create=False
        )
        v["rank"] = srank

        new_context = self.check_context(operation, stat_name, value)

        opposing = (
            self._get_reverse()
            .filter(stat=srank.stat, context__iexact=new_context)
            .first()
        )
        if opposing and opposing != srank:
            raise operation.ex(
                f"{self.render_context(stat_name, context)} cannot be renamed to {new_context} because {opposing} already has that context."
            )
        v["context_before"] = srank.context
        v["format_before"] = self.format_rank(srank)
        srank.context = new_context

        self.announce_op_context(operation)

    def announce_op_context(self, operation: Operation):
        v = operation.variables
        rank = v["rank"]
        before = v["context_before"]
        f_before = v["format_before"]
        message = f"{f_before} was renamed to {self.render_context(rank.stat.name, rank.context)}.)"
        self.send_message(operation, message)

    def op_describe(self, operation: Operation):
        v = operation.variables
        path = v["path"]
        value = v["value"]

        stat_name, context = self.parse_context(operation, path[0])
        srank = self.check_srank(
            operation, stat_name, context, partial=True, create=False
        )
        v["rank"] = srank
        v["description_before"] = srank.description

        srank.description = value

        self.announce_op_describe(operation)

    def announce_op_describe(self, operation: Operation):
        v = operation.variables
        rank = v["rank"]
        before = v["description_before"]
        message = f"{self.format_rank(rank)} was described: |w{rank.description}|n. (Was |w{before}|n)"
        self.send_message(operation, message)

    def get_choices(self) -> list[str]:
        return list()

    def _get_stat(self, name: str):
        stat, created = self.stat_model.objects.get_or_create(
            category=self.stat_category, name=name
        )
        return stat

    def check_stat(self, operation, name: str):
        choice = self.get_choice(operation, name)
        return self._get_stat(choice)

    def check_srank(
        self,
        operation,
        stat: str,
        context: str,
        partial: bool = False,
        create: bool = True,
    ) -> StatRank:
        r = self._get_reverse()
        if create:
            partial = False

        if partial:
            candidates = r.filter(stat__category=self.stat_category)
            if context:
                candidates = candidates.exclude(context="")
                if not candidates:
                    raise operation.ex(f"No entry found matching '{context}'.")
                if not (srank := partial_match(context, candidates)):
                    raise operation.ex(
                        f"No entry found matching '{context}'. Choices are: {', '.join(candidates)}"
                    )
                return srank
            else:
                candidates = candidates.filter(context="")
                if not candidates:
                    raise operation.ex(f"No entry found matching '{stat}'.")
                if not (srank := candidates.first()):
                    raise operation.ex(f"No entry found matching '{stat}'.")
                return srank

        stat_dict = {"category": self.stat_category, "name": stat}

        if not (
            srank := r.filter(
                context__iexact=context,
                **{f"stat__{k}__iexact": v for k, v in stat_dict.items()},
            ).first()
        ):
            if create:
                stat = self.check_stat(operation, stat)
                srank, created = r.get_or_create(stat=stat, context=context)
            else:
                raise operation.ex(
                    f"No entry found matching '{self.render_context(stat, context)}'."
                )
        else:
            srank.context = context
        return srank

    def has_customs(self, rank) -> bool:
        for rel in self.custom_relations:
            if getattr(rank, rel).count():
                return True
        return False

    def should_delete(self, rank) -> bool:
        return rank.value <= 0 and self.remove_zero and not self.has_customs(rank)

    def op_tier(self, operation: Operation):
        v = operation.variables
        path = v["path"]
        value = v["value"]

        stat_name, context = self.parse_context(operation, path[0])
        srank = self.check_srank(
            operation, stat_name, context, partial=True, create=False
        )
        self._op_tier(operation, srank, value)

    def op_tag(self, operation: Operation):
        v = operation.variables
        path = v["path"]
        value = v["value"]

        stat_name, context = self.parse_context(operation, path[0])
        srank = self.check_srank(
            operation, stat_name, context, partial=True, create=False
        )
        self._op_tag(operation, srank, value)

    def op_untag(self, operation: Operation):
        v = operation.variables
        path = v["path"]
        value = v["value"]

        stat_name, context = self.parse_context(operation, path[0])
        srank = self.check_srank(
            operation, stat_name, context, partial=True, create=False
        )
        self._op_untag(operation, srank, value)

    def op_mod(self, operation: Operation):
        v = operation.variables
        path = v["path"]
        value = v["value"]

        stat_name, context = self.parse_context(operation, path[0])
        srank = self.check_srank(
            operation, stat_name, context, partial=True, create=False
        )
        self._op_mod(operation, srank, value)

    def op_unmod(self, operation: Operation):
        v = operation.variables
        path = v["path"]
        value = v["value"]

        stat_name, context = self.parse_context(operation, path[0])
        srank = self.check_srank(
            operation, stat_name, context, partial=True, create=False
        )
        self._op_unmod(operation, srank, value)

    def render_sheet_tri_categories(
        self, viewer, width, lines, psm, category, name_category=True
    ):
        r = self._get_reverse()
        category = category.lower()
        psm_lower = [p.lower() for p in psm]

        gathered = [
            r.filter(
                stat__category__iexact=self.stat_category,
                stat__name__in=getattr(self.game, f"{p}_{category}"),
            )
            for p in psm_lower
        ]

        if any(gathered):
            names = [
                f"{n.capitalize()} {category.capitalize()}"
                if name_category
                else f"{n.capitalize()}"
                for n in psm
            ]
            self.render_sheet_triheader(
                viewer,
                width,
                lines,
                names=names,
            )

            widths = self.tri_split_width(width - 4)
            rendered_columns = list()
            tiers = "tier" in self.options
            for i, column in enumerate(gathered):
                items = list()
                for stat in column:
                    items.append(
                        self.render_sheet_stat(
                            viewer, width, stat, item_width=widths[i], tiers=tiers
                        )
                    )
                rendered_columns.append(items)

            self.render_sheet_tricolumns(viewer, width, lines, rendered_columns)


class AdvantageHandler(StatHandler):
    """
    The AdvantageHandler is meant to handle what Storyteller often calls Advantages.

    The permanent Willpower stat. Essence in Exalted, Generation/Blood Potency for Vampires, Arete/Gnosis for Mages, etc.

    The list of available Advantages usually differs by Template, so by default this handler checks template.advantages.
    """

    sheet_render = False
    stat_category = "Advantages"
    singular_name = "Advantage"
    options = ("set",)
    load_order = -50

    def get_choices(self) -> list[str]:
        return getattr(self.template(), "advantages", list())

    def get_choice(self, operation, entry: str) -> str:
        choice = super().get_choice(operation, entry)
        if choice == "Power":
            return self.owner.st_template.get().power_stat
        return choice

    def at_template_change(self):
        r = self._get_reverse()

        t = self.template()

        current = self.all()
        for rank in current:
            if rank.stat.name not in t.advantages:
                rank.delete()

        for name in t.advantages:
            stat = self._get_stat(name)
            rank, created = r.get_or_create(stat=stat)
            if created:
                rank.save()
            d = t.advantages_defaults.get(name, 1)
            if rank.value < d:
                rank.value = d
                rank.save()


class AttributeHandler(StatHandler):
    """
    The AttributeHandler is meant to handle what Storyteller often calls Attributes.
    Strength, Dexterity, Stamina, Charisma, etc.

    The list of available Attributes usually differs by Game, so by default this handler checks game.attributes.
    """

    stat_category = "Attributes"
    singular_name = "Attribute"
    options = (
        "set",
        "rank",
    )
    load_order = 0

    def get_choices(self) -> list[str]:
        return getattr(self.game, "attributes", list())

    def at_game_enter(self):
        """
        With rare exceptions, Attributes all start at 1.
        """
        r = self._get_reverse()
        for name in self.get_choices():
            stat = self._get_stat(name)
            rank, created = r.get_or_create(stat=stat)
            if rank.value < 1:
                rank.value = 1
                rank.save()

    def render_sheet(self, viewer, width: int, lines: list[ANSIString]):
        self.render_sheet_tri_categories(
            viewer, width, lines, ["physical", "social", "mental"], "attributes"
        )


class AbilityHandler(StatHandler):
    """
    Each Game has a list of Abilities, which are usually the same across all Templates.

    These are things such as Melee, Brawl, Firearms, Survival, Animal Ken, Streetwise, Stealth, etc.
    """

    stat_category = "Abilities"
    singular_name = "Ability"
    options = (
        "set",
        "rank",
    )
    load_order = 10

    def get_choices(self) -> list[str]:
        return self.game.abilities


class MeritHandler(StatHandler):
    """
    Merits are different from Stats in that they usually can be purchased multiple times for different sitautions.
    For instance, the Merit "Artifact" in Exalted can be purchased multiple times for different artifacts.

    To handle this, Merits have a 'context' field, which is used to differentiate between different purchases.
    Example - Artifact: Grand Daiklave
    """

    stat_category = "Merits"
    singular_name = "Merit"
    options = ("set", "delete", "rank", "rename", "describe")
    use_context = True
    dynamic_choices = True
    load_order = 30


class SpecialtyHandler(MeritHandler):
    """
    Most of the WoD games allow for specialties. Sometimes these add bonus dice to a roll,
    at other times they alter the dice roll rules.

    Most of the time, you just purchase the specialty and have it. Exalted 2e allows you to purchase a specialty
    up to +3, though.
    """

    stat_category = "Specialties"
    singular_name = "Specialty"
    max_value = 1
    remove_zero = True
    options = ("set", "remove", "rank", "delete", "rename")
    enforce_context = True
    load_order = 20
    context_delim = "/"
    context_delim_display = "/"

    def get_choices(self) -> list[str]:
        """
        Usually, specialties branch off of an Ability, so we need to know what abilities are available.
        In Exalted 2e, Lunars with a specific Charm can get Specialties for their Attributes.
        """
        return self.game.abilities


class FlawHandler(MeritHandler):
    """
    Not every game uses Flaws, but they work like Merits when they do.
    """

    stat_category = "Flaws"
    singular_name = "Flaw"
    load_order = 40


class BackgroundHandler(MeritHandler):
    """
    Sometimes Merits and Backgrounds are the same thing depending on game, sometimes they're different systems.
    Either way, they both work like 'Merits' do.
    """

    stat_category = "Backgrounds"
    singular_name = "Background"
    load_order = 50


class PowerHandler(BaseHandler):
    """
    The PowerHandler is meant to handle complex categorized powers.

    The primary example is Charms and Spells from Exalted, which can be categorized as such:

    (in order of: family, category, subcategory, name)
    ("Charms", "Solar", "Melee", "Fire and Stones Strike")
    ("Charms", "Lunar", "Intelligence", "Counting the Elephant's Wrinkles")
    ("Spells", "Sorcery", "Terrestrial", "Demon of the First Circle")
    ("Spells", "Necromancy", "Shadowlands", "Summon Ghost")

    Werewolf Gifts are also doable.
    ("Gifts", "Ragabash", "1", "Open Seal")

    This is an abstract base class which cannot be used directly.

    It requires a family to be set, and customization to the get_ operations to determine
    possible choices at each stage, and relevant announce_  operations defined.
    """

    options = ("add", "remove", "delete", "tag", "untag", "tier", "mod", "unmod")
    family = None
    min_path_length = 2
    path_format = "<category>,<subcategory>"
    power_model = Power
    reverse_relation = "powers"
    singular_name = "power"
    dynamic_category = False
    dynamic_subcategory = False
    load_order = 50

    def clear(self):
        self._get_reverse().filter(power__family__iexact=self.family).delete()

    @property
    def name(self):
        return self.family

    @property
    def plural_name(self):
        return self.family

    def render_help_header(self, lines: list[str]):
        lines.append(f"|c{self.name}:|n (Type: |wPower|n)")

    def render_category(self, category, plural=True):
        return f"|c{category} {self.plural_name if plural else self.singular_name}|n"

    def render_subcategory(self, category, subcategory, plural=True):
        return f"|c{category} {subcategory} {self.plural_name if plural else self.singular_name}|n"

    def format_rank(self, rank):
        return f"{self.render_subcategory(rank.power.category, rank.power.subcategory, plural=False)}|c:|n |w{rank.power.name}|n"

    def _get_reverse(self):
        return getattr(self.owner.sheet, self.reverse_relation)

    def at_game_leave(self):
        self._get_reverse().all().delete()

    def get_category_choices(self, operation: Operation) -> list[str]:
        return self.get_choices()

    def get_choices(self):
        return list()

    def get_category(self, operation: Operation, name: str) -> str:
        if not name:
            raise operation.ex(f"No {self.family} category given.")
        if self.dynamic_category:
            category = validate_name(name, thing_type=self.family)
            return dramatic_capitalize(category)

        if not (choices := self.get_category_choices(operation)):
            raise operation.ex(f"No {self.family} categories found.")

        # deal with weird generative choices.
        if callable(choices):
            choices = choices(self.owner)

        if not choices:
            raise operation.ex(f"No categories found.")

        if not (category := partial_match(name, choices)):
            raise operation.ex(
                f"No {self.family} category found matching '{name}'. Choices are: {', '.join(choices)}"
            )
        return category

    def get_subcategory_choices(self, operation: Operation, category: str):
        return list()

    def get_subcategory(self, operation: Operation, category: str, name: str) -> str:
        if not name:
            raise operation.ex(
                f"No {self.render_category(category)} sub-category given."
            )

        if self.dynamic_subcategory:
            category = validate_name(name, thing_type=self.render_category(category))
            return dramatic_capitalize(category)

        if not (choices := self.get_subcategory_choices(operation, category)):
            raise operation.ex(
                f"No {self.render_category(category)} sub-categories found."
            )

        # deal with weird generative choices.
        if callable(choices):
            choices = choices(self.owner)

        if not choices:
            raise operation.ex(
                f"No {self.render_category(category)} sub-categories found."
            )

        if not (subcategory := partial_match(name, choices)):
            raise ValueError(
                f"No {self.render_category(category)} sub-categories found matching '{name}'. Choices are: {', '.join(choices)}"
            )

        return subcategory

    def get_name(
        self, operation: Operation, category: str, subcategory: str, name: str
    ) -> str:
        name = validate_name(
            name,
            thing_type=self.render_subcategory(category, subcategory, plural=False),
            ex_type=operation.ex,
        )
        return dramatic_capitalize(name)

    def get_power(
        self, operation: Operation, category: str, subcategory: str, name: str
    ) -> Power:
        if not (
            power := self.power_model.objects.filter(
                family__iexact=self.family,
                category__iexact=category,
                subcategory__iexact=subcategory,
                name__iexact=name,
            ).first()
        ):
            power = self.power_model.objects.create(
                family=self.family,
                category=category,
                subcategory=subcategory,
                name=name,
            )
        return power

    def get_power_rank(
        self,
        operation: Operation,
        category: str,
        subcategory: str,
        name: str,
        create=True,
    ) -> PowerRank:
        rev = self._get_reverse()
        power_dict = {
            "family": self.family,
            "category": category,
            "subcategory": subcategory,
            "name": name,
        }

        if not (
            rank := rev.filter(
                **{
                    f"power__{k}__iexact": v
                    for k, v in power_dict.items()
                    if v is not None
                },
            ).first()
        ):
            if create:
                power = self.power_model.objects.create(**power_dict)
                rank = rev.create(power=power)
            else:
                power_dict.pop("name", None)
                if not (choices := rev.filter(**power_dict)):
                    raise operation.ex(
                        f"No {self.render_subcategory(category, subcategory)} found matching '{name}'."
                    )
                if not (rank := partial_match(name, choices)):
                    raise operation.ex(
                        f"No {self.render_subcategory(category, subcategory)} found matching '{name}'. Choices are: "
                        f"{', '.join([str(x) for x in choices])}"
                    )
        return rank

    def op_add(self, operation: Operation):
        v = operation.variables
        path = v["path"]
        value = v["value"]

        # Family is known due to self.family.
        # the path should be [category, subcategory]
        # name is value

        category = self.get_category(operation, path[0])
        subcategory = self.get_subcategory(operation, category, path[1])
        name = self.get_name(operation, category, subcategory, value)
        rank = self.get_power_rank(operation, category, subcategory, name)
        v["rank_before"] = rank.value
        rank.value += 1
        v["rank"] = rank
        self.announce_op_set(operation)

    def at_post_operation(self, operation):
        if rank := operation.variables.get("rank", None):
            if rank.value <= 0:
                rank.delete()
            else:
                rank.save()

    def op_remove(self, operation: Operation):
        v = operation.variables
        path = v["path"]
        value = v["value"]

        # Family is known due to self.family.
        # the path should be [category, subcategory]
        # name is value

        category = self.get_category(operation, path[0])
        subcategory = self.get_subcategory(operation, category, path[1])
        name = self.get_name(operation, category, subcategory, value)
        rank = self.get_power_rank(operation, category, subcategory, name, create=False)
        v["rank_before"] = rank.value
        rank.value -= 1
        v["delete"] = self.should_delete(rank)
        v["rank"] = rank
        self.announce_op_set(operation)

    def should_delete(self, rank) -> bool:
        return rank.value <= 0

    def op_delete(self, operation: Operation):
        v = operation.variables
        path = v["path"]
        value = v["value"]

        # Family is known due to self.family.
        # the path should be [category, subcategory]
        # name is value

        category = self.get_category(operation, path[0])
        subcategory = self.get_subcategory(operation, category, path[1])
        name = self.get_name(operation, category, subcategory, value)
        rank = self.get_power_rank(operation, category, subcategory, name, create=False)
        self._op_delete(operation, rank)

    def op_tag(self, operation: Operation):
        """
        This works very similarly to op_add, but the path length is 3 for (category, subcategory, name)
        and value is a string tag that will be added to the rank.data["tags"] set. Created if it doesn't exist.
        """
        v = operation.variables
        path = v["path"]
        value = v["value"]

        # Family is known due to self.family.
        # the path should be [category, subcategory, name]
        # value is the tag

        category = self.get_category(operation, path[0])
        subcategory = self.get_subcategory(operation, category, path[1])
        if not len(path) >= 3:
            raise operation.ex(f"No power name given.")
        name = self.get_name(operation, category, subcategory, path[2])
        rank = self.get_power_rank(operation, category, subcategory, name, create=False)
        self._op_tag(operation, rank, value)

    def op_untag(self, operation: Operation):
        """
        This works very similarly to op_remove, but the path length is 3 for (category, subcategory, name)
        and value is a string tag that will be removed from the rank.data["tags"] set.
        """
        v = operation.variables
        path = v["path"]
        value = v["value"]

        # Family is known due to self.family.
        # the path should be [category, subcategory, name]
        # value is the tag

        category = self.get_category(operation, path[0])
        subcategory = self.get_subcategory(operation, category, path[1])
        if not len(path) >= 3:
            raise operation.ex(f"No power name given.")
        name = self.get_name(operation, category, subcategory, path[2])
        rank = self.get_power_rank(operation, category, subcategory, name, create=False)
        self._op_untag(operation, rank, value)

    def op_mod(self, operation: Operation):
        """
        This works very similarly to op_add, but the path length is 3 for (category, subcategory, name)
        and value is a string mod that will be added to the rank.data["mods"] set. Created if it doesn't exist.
        """
        v = operation.variables
        path = v["path"]
        value = v["value"]

        # Family is known due to self.family.
        # the path should be [category, subcategory, name]
        # value is the mod

        category = self.get_category(operation, path[0])
        subcategory = self.get_subcategory(operation, category, path[1])
        if not len(path) >= 3:
            raise operation.ex(f"No power name given.")
        name = self.get_name(operation, category, subcategory, path[2])
        if not (
            rank := self.get_power_rank(
                operation, category, subcategory, name, create=False
            )
        ):
            raise operation.ex(f"Entry not found to mod.")
        self._op_mod(operation, rank, value)

    def op_unmod(self, operation: Operation):
        """
        This works very similarly to op_remove, but the path length is 3 for (category, subcategory, name)
        and value is a string mod that will be removed from the rank.data["mods"] set.
        """
        v = operation.variables
        path = v["path"]
        value = v["value"]

        # Family is known due to self.family.
        # the path should be [category, subcategory, name]
        # value is the mod

        category = self.get_category(operation, path[0])
        subcategory = self.get_subcategory(operation, category, path[1])
        if not len(path) >= 3:
            raise operation.ex(f"No power name given.")
        name = self.get_name(operation, category, subcategory, path[2])
        if not (
            rank := self.get_power_rank(
                operation, category, subcategory, name, create=False
            )
        ):
            raise operation.ex(f"Entry not found to unmod.")
        self._op_unmod(operation, rank, value)

    def op_tier(self, operation: Operation):
        """
        This works very similarly to op_add, but the path length is 3 for (category, subcategory, name)
        and value is an integer that will be added to the rank.data["tiers"] set. Created if it doesn't exist.
        """
        v = operation.variables
        path = v["path"]
        value = v["value"]

        # Family is known due to self.family.
        # the path should be [category, subcategory, name]
        # value is the tier

        category = self.get_category(operation, path[0])
        subcategory = self.get_subcategory(operation, category, path[1])
        if not len(path) >= 3:
            raise operation.ex(
                f"No {self.render_subcategory(category, subcategory)} name given."
            )
        name = self.get_name(operation, category, subcategory, path[2])
        if not (
            rank := self.get_power_rank(
                operation, category, subcategory, name, create=False
            )
        ):
            raise operation.ex(
                f"{self.render_subcategory(category, subcategory, plural=False)} not found to tier."
            )
        self._op_tier(operation, rank, value)


class CustomPowerHandler(BaseHandler):
    """
    CustomPowers are usually branched off context-stat combinations.

    This is primarily used in Exalted 3rd Edition to cover Artifact Evocations.

    An example, the character would have the merit, "Artifact: The Distaff", and
    their custom power is the evocation, "Poppet-Knitting Practice". Since Evocations are
    unique, they are simply stored alongside the purchase because there's
    no point in creating a normalized database of them.

    This is an Abstract base Class. it cannot be used directly.

    To use it, specify the proper stat_category and stat that it would target.
    For example, stat_category="Merits", stat="Artifact"
    """

    stat_category: str = None
    stat: str = None
    options = ("add", "remove", "delete", "tag", "untag")
    reverse_relation = "stats"
    rank_reverse_relation = "customs"
    min_path_length = 1
    load_order = 100

    def _get_reverse(self):
        return getattr(self.owner.sheet, self.reverse_relation)

    def _get_rank_reverse(self, rank):
        return getattr(rank, self.rank_reverse_relation)

    def get_context(self, operation: Operation, name: str):
        context = validate_name(
            name,
            thing_type=f"Context",
            ex_type=operation.ex,
        )
        r = self._get_reverse()
        if not (
            choices := r.filter(
                stat__category__iexact=self.stat_category, stat__name__iexact=self.stat
            ).exclude(context="")
        ):
            raise operation.ex(f"No choices found.")
        if not (context := partial_match(context, choices, key=lambda x: x.context)):
            raise operation.ex(
                f"No context found matching '{context}'. Choices are: {', '.join([x.context for x in choices])}"
            )

        return context

    def get_power(self, operation: Operation, rank, name: str, create=True):
        name = validate_name(
            name,
            thing_type=f"Name",
            ex_type=operation.ex,
        )
        name = dramatic_capitalize(name)

        r = self._get_rank_reverse(rank)

        if not (power := r.filter(name__iexact=name).first()):
            if not create:
                if not (choices := r.all()):
                    raise operation.ex(f"No choices found.")
                if not (power := partial_match(name, choices)):
                    raise operation.ex(
                        f"No power found matching '{name}'. Choices are: {', '.join([x.name for x in choices])}"
                    )
                return power
            power = r.create(name=name)
        return power

    def op_add(self, operation: Operation):
        v = operation.variables
        path = v["path"]
        value = v["value"]

        # in this case, the path should be just [context], and value is the power name.
        rank = self.get_stat_rank(operation, path[0])
        power = self.get_power(operation, rank, value)
        v["power_before"] = power.value
        v["power"] = power
        power.value += 1
        self.announce_op_add(operation)

    def announce_op_add(self, operation: Operation):
        pass

    def op_remove(self, operation: Operation):
        v = operation.variables
        path = v["path"]
        value = v["value"]

        # in this case, the path should be just [context], and value is the power name.
        rank = self.get_stat_rank(operation, path[0])
        power = self.get_power(operation, rank, value, create=False)
        v["power_before"] = power.value
        v["power"] = power
        power.value -= 1
        self.announce_op_remove(operation)

    def announce_op_remove(self, operation: Operation):
        pass

    def op_delete(self, operation: Operation):
        v = operation.variables
        path = v["path"]
        value = v["value"]

        # in this case, the path should be just [context], and value is the power name.
        rank = self.get_stat_rank(operation, path[0])
        power = self.get_power(operation, rank, value, create=False)
        v["power_before"] = power.value
        v["power"] = power
        power.value = 0
        self.announce_op_delete(operation)

    def announce_op_delete(self, operation: Operation):
        pass

    def get_power_tag(self, operation: Operation, rank, tag: str):
        tag = validate_name(tag, thing_type=f"Tag", ex_type=operation.ex)
        return tag.lower()

    def op_tag(self, operation: Operation):
        v = operation.variables
        path = v["path"]
        value = v["value"]

        # in this case, the path should be just [context, power_name], and value is the power name.
        rank = self.get_stat_rank(operation, path[0])
        if not len(path) >= 2:
            raise operation.ex(f"No power name given.")
        power = self.get_power(operation, rank, path[1], create=False)
        tag = self.get_power_tag(operation, rank, value)
        v["power_before"] = power.value
        v["power"] = power
        tags = power.data.get("tags", list())
        if tag not in tags:
            v["tag_added"] = tag
            tags.append(tag)
        power.data["tags"] = tags
        self.announce_op_tag(operation)

    def announce_op_tag(self, operation: Operation):
        pass

    def op_untag(self, operation: Operation):
        v = operation.variables
        path = v["path"]
        value = v["value"]

        # in this case, the path should be just [context, power_name], and value is the power name.
        rank = self.get_stat_rank(operation, path[0])
        if not len(path) >= 2:
            raise operation.ex(f"No power name given.")
        power = self.get_power(operation, rank, path[1], create=False)
        tag = self.get_power_tag(operation, rank, value)
        v["power_before"] = power.value
        v["power"] = power
        tags = power.data.get("tags", list())
        if tag in tags:
            v["tag_removed"] = tag
            tags.remove(tag)
        power.data["tags"] = tags
        self.announce_op_untag(operation)

    def announce_op_untag(self, operation: Operation):
        pass


class StatPowerHandler(BaseHandler):
    """
    Stat Powers are usually branched off of Stats. For instance, in Exalted, you can purchase Charms
    based off of Martial Arts Styles. In that case, the StyleHandler would be a StatHandler that handles
    purchasing dots in each Style, and the MartialArtsCharmHandler would be a CustomPowerHandler that handles
    purchasing Charms for each Style.
    """

    stat_category: str = None
    singular_name: str = None
    options = ("add", "remove")
    load_order = 1000

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


class FooterHandler(RawHandler):
    api_access = False
    sheet_render = True
    load_order = 999999999999

    def render_sheet(self, viewer, width: int, lines: list[ANSIString]):
        self.render_sheet_bottom(viewer, width, lines)

    def render_sheet_bottom(self, viewer, width, lines):
        self.render_sheet_header(viewer, width, lines)
        border = self.get_color("border")
        t = self.template()

        available_width = width - 4 - len(t.sheet_footer)
        divided = available_width / 2
        left_len = math.floor(divided)
        right_len = math.ceil(divided)
        center = (" " * left_len) + t.sheet_footer + (" " * right_len)
        lines.append(ANSIString(f" |{border}\\|n" + center + f"|{border}/|n"))

        available_width = width - 6
        divided = available_width / 2
        left_len = math.floor(divided)
        right_len = math.ceil(divided)

        left = ANSIString("  " + f"|{border}" + "'" + ("-" * left_len))
        right = ANSIString(("-" * right_len) + "'|n")
        lines.append(left + right)
