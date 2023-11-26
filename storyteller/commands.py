from athanor.utils import partial_match
from athanor.commands import AthanorCommand, AthanorAccountCommand
from .utils import get_story


class _StoryCmd(AthanorCommand):
    help_category = "Storyteller"


class CmdCg(_StoryCmd):
    key = "cg"
    delim = "|"

    def do_info(self):
        if not (target := self.caller.search(self.lhs) if self.lhs else self.caller):
            self.msg("No such character.")
            return

        story = target.h.story

        lines = list()
        lines.append(self.styled_header(f"Sheet Info for {target}"))
        story.game.render_help(lines)
        for handler in story.handlers:
            if handler.api_access:
                handler.render_help(lines)
        story.game.render_help_end(lines)
        lines.append(self.styled_footer())
        self.msg_lines(lines)

    def do_target(self):
        if not (target := self.caller.search(self.lhs)):
            self.msg("No such character.")
            return

        self.caller.attributes.clear(category="cg_menu")
        self.caller.attributes.add("cg_target", category="storyteller", value=target)
        self.msg(f"CG Target set to {target}.")

    def do_edit(self):
        if not (target := self.caller.search(self.lhs)):
            self.msg("No such character.")
            return

        self.caller.attributes.add("target", category="cg_menu", value=target)
        self.caller.cmdset.add("storyteller.menu.StorytellerEditorMenu")
        self.execute_cmd("menu")

    def func(self):
        if "edit" in self.switches:
            self.do_edit()
            return

        if "target" in self.switches:
            self.do_target()
            return

        if "info" in self.switches:
            self.do_info()
            return

        if not (
            target := self.caller.attributes.get("cg_target", category="storyteller")
        ):
            self.msg("You must set a CG target.")
            return

        path = self.lhs.split(self.delim)

        if len(path) < 1:
            self.msg("You must provide a path to a node.")
            return

        story = get_story(target)

        if not self.switches and len(path) == 1:
            shortcuts = dict()
            for handler in story.handlers:
                handler.shortcut_dict(shortcuts)
            if not shortcuts:
                self.msg("No shortcuts available.")
                return
            if not (shortcut := partial_match(path[0], shortcuts.keys())):
                self.msg(f"No such choice. Choices are: {', '.join(shortcuts)}")
                return
            data = shortcuts[shortcut]
            op = self.operation(
                target=data[0],
                operation=data[1],
                kwargs={"path": data[2], "value": self.rhs},
            )
        else:
            if not (node := partial_match(path[0], story.handlers)):
                self.msg(
                    f"No such handler. Choices are: {', '.join([str(c) for c in story.handlers])}"
                )
                return

            switch = (
                self.switches[0].lower().strip()
                if self.switches
                else getattr(node, "default_operation", "set")
            )

            if not (operation := partial_match(switch, node.options)):
                self.msg(
                    f"No such switch option. Choices are: {', '.join(node.options)}"
                )
                return

            op = self.operation(
                target=node,
                operation=operation,
                kwargs={"path": path[1:], "value": self.rhs},
            )
        op.execute()
        self.op_message(op)


class CmdSheet(_StoryCmd):
    key = "sheet"
    locks = "cmd:all()"

    def func(self):
        if not (target := self.caller.search(self.args) if self.args else self.caller):
            self.msg("No such character.")
            return

        self.do_render(target)

    def do_render(self, target: "DefaultCharacter"):
        story = get_story(target)
        lines = story.get_sheet(self.caller, 78)
        self.msg_lines(lines)
