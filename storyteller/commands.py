from athanor.utils import partial_match
from athanor.commands import AthanorCommand, AthanorAccountCommand
from .utils import get_story


class CmdSheet(AthanorCommand):
    key = "sheet"
    switch_options = (
        "add",
        "remove",
        "set",
        "delete",
        "describe",
        "tag",
        "untag",
        "context",
        "mod",
        "unmod",
        "tier",
        "help",
        "info",
    )
    locks = "cmd:all()"
    help_category = "Storyteller"

    def func(self):
        if self.switches:
            self.do_switches()
            return

        if not self.args:
            self.do_render(self.caller)
            return

        if not (target := self.caller.search(self.args)):
            self.msg("No such character.")
            return

        self.do_render(target)

    def do_render(self, target: "DefaultCharacter"):
        story = get_story(target)

        lines = list()
        for handler in story.handlers:
            if not handler.sheet_render:
                continue
            handler.render_sheet(self.caller, 78, lines)

        self.msg_lines(lines)

    def do_help(self):
        if not (target := self.caller.search(self.lhs) if self.lhs else self.caller):
            self.msg("No such character.")
            return

        story = get_story(target)

        lines = list()
        lines.append(self.styled_header(f"Sheet Help for {target}"))
        story.game.render_help(lines)
        for handler in story.handlers:
            handler.render_help(lines)
        story.game.render_help_end(lines)
        lines.append(self.styled_footer())
        self.msg_lines(lines)

    def do_switches(self):
        switch = self.switches[0].lower().strip()

        if switch == "help":
            self.do_help()
            return

        path = self.lhs.split("|")

        if len(path) < 2:
            self.msg("You must provide a path to a character and a node.")
            return

        if not (target := self.caller.search(path[0])):
            self.msg("No such character.")
            return

        story = get_story(target)

        if not (node := partial_match(path[1], story.handlers)):
            self.msg(
                f"No such handler. Choices are: {', '.join([str(c) for c in story.handlers])}"
            )
            return

        if not (operation := partial_match(switch, node.options)):
            self.msg(f"No such switch option. Choices are: {', '.join(node.options)}")
            return

        op = self.operation(
            target=node,
            operation=operation,
            kwargs={"path": path[2:], "value": self.rhs},
        )
        op.execute()
        self.op_message(op)
