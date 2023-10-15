from athanor.utils import partial_match
from athanor.commands import AthanorCommand, AthanorAccountCommand


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
        "rename",
    )
    locks = "cmd:all()"
    help_category = "Storyteller"

    def func(self):
        if self.switches and self.caller.is_admin():
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
        self.msg(target.sheet.render(self.caller))

    def do_switches(self):
        switch = self.switches[0].lower().strip()

        path = self.lhs.split("|")

        if len(path) < 2:
            self.msg("You must provide a path to a character and a node.")
            return

        if not (target := self.caller.search(path[0])):
            self.msg("No such character.")
            return

        if not (handlers := getattr(target, "get_story_handlers", None)):
            self.msg(f"{target} is not a Storyteller Character.")
            return

        choices = handlers()

        if not (node := partial_match(path[1], choices)):
            self.msg(
                f"No such handler. Choices are: {', '.join([str(c) for c in choices])}"
            )
            return

        if switch not in node.options:
            self.msg(f"No such switch option. Choices are: {', '.join(node.options)}")
            return

        if not self.rhs:
            self.msg("You must provide a value.")
            return

        node.do_operation(self.caller, path[2:], self.rhs, switch)
