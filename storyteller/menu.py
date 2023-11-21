from athanor.menu import (
    MenuCmdSet,
    AthanorMenuCommand,
    CmdMenu as _CmdMenu,
    CmdExit as _CmdExit,
)
from athanor.utils import partial_match


class CmdMenu(_CmdMenu):
    pass


class CmdExit(_CmdExit):
    pass


class _EditorMenuCommand(AthanorMenuCommand):
    def parse(self):
        super().parse()
        self.target = self.caller.attributes.get(
            "target", category="cg_menu", default=None
        )
        self.mode = self.caller.attributes.get(
            "mode", category="cg_menu", default="Game"
        )
        self.story = self.target.h.story
        self.handler = self.story.handlers_dict.get(self.mode, None)


class StoryMenuCommand(_EditorMenuCommand, AthanorMenuCommand):
    def access(self, srcobj, access_type="cmd", default=False):
        if access_type == "cmd":
            if not (
                target := srcobj.attributes.get(
                    "target", category="cg_menu", default=None
                )
            ):
                return False
            mode = srcobj.attributes.get("mode", category="cg_menu", default="Game")
            story = target.h.story
            if not (handler := story.handlers_dict.get(mode, None)):
                return False
            return self.key in handler.options
        return self.lockhandler.check(srcobj, access_type, default=default)

    def func(self):
        syntax = self.handler.options_syntax.get(self.key, getattr(self, "syntax", ""))
        use_equals = "=" in syntax
        if use_equals:
            if not (self.lhs and self.rhs):
                self.msg(f"Usage: {syntax}")
                return
            path = [item.strip() for item in self.lhs.split("/")]
            value = self.rhs
        else:
            if not self.args:
                self.msg(f"Usage: {syntax}")
                return
            path = []
            value = self.args

        op = self.operation(
            target=self.handler,
            operation=self.key,
            kwargs={"path": path, "value": value},
        )
        op.execute()
        self.op_message(op)

        if op.results.get("redisplay_menu", False):
            self.true_cmdset.render_menu()


class CmdMode(_EditorMenuCommand):
    key = "mode"
    syntax = "mode <mode>"
    desc = "Change Menu Mode"
    menu_sort = 99999

    def func(self):
        available = [handler for handler in self.story.handlers if handler.menu_access]
        if not self.args:
            self.msg(f"Available modes: {', '.join([str(x) for x in available])}")
            return

        if not (mode := partial_match(self.args, available)):
            self.msg(
                f"No such mode. Available modes: {', '.join([str(x) for x in available])}"
            )
            return

        self.caller.attributes.add("mode", str(mode), category="cg_menu")
        self.true_cmdset.render_menu()


class CmdSet(StoryMenuCommand):
    key = "set"


class CmdTier(StoryMenuCommand):
    key = "tier"


class CmdContext(StoryMenuCommand):
    key = "context"


class CmdRank(StoryMenuCommand):
    key = "rank"


class CmdTag(StoryMenuCommand):
    key = "tag"


class CmdUntag(StoryMenuCommand):
    key = "untag"


class CmdMod(StoryMenuCommand):
    key = "mod"


class CmdUnMod(StoryMenuCommand):
    key = "unmod"


class CmdDescribe(StoryMenuCommand):
    key = "describe"


class CmdCreate(StoryMenuCommand):
    key = "create"

    @property
    def use_equals(self):
        return (
            self.handler.min_path_length_operation.get(
                self.key, self.handler.min_path_length
            )
            - 1
        ) > 0


class CmdDelete(StoryMenuCommand):
    key = "delete"

    def use_equals(self):
        return (
            self.handler.min_path_length_operation.get(
                self.key, self.handler.min_path_length
            )
            - 1
        ) > 0


class StorytellerEditorMenu(MenuCmdSet):
    help_category = "Storyteller Editor Menu"
    command_classes = [
        CmdMenu,
        CmdExit,
        CmdSet,
        CmdDelete,
        CmdCreate,
        CmdMod,
        CmdUnMod,
        CmdTag,
        CmdUntag,
        CmdRank,
        CmdTier,
        CmdMode,
        CmdDescribe,
        CmdContext,
    ]

    def end_menu(self):
        super().end_menu()
        self.cmdsetobj.attributes.clear(category="cg_menu")

    def at_pre_cmd(self, cmd):
        if not (
            target := self.cmdsetobj.attributes.get(
                "target", category="cg_menu", default=None
            )
        ):
            self.cmdsetobj.msg("Target has become invalid.")
            self.end_menu()
            return True

    def render_menu(self):
        obj = self.cmdsetobj
        account = obj.account

        mode = obj.attributes.get("mode", category="cg_menu", default="Game")
        target = obj.attributes.get("target", category="cg_menu", default=None)
        story = target.h.story

        self.msg(account.styled_header(f"Storyteller '{mode}' Menu for: {target}"))
        if handler := story.handlers_dict.get(mode, None):
            self.msg(handler.format_menu_help(obj))
        modes = ", ".join([str(x) for x in story.handlers if x.menu_access])
        self.msg(account.styled_separator("Mode Select"))
        self.msg(f"|wAvailable Modes:|n {modes}")

        t = account.rich_table("Command", "Syntax", "Description", title="Commands")

        for command in self.get_commands():
            if not command.access(obj, "cmd"):
                continue
            t.add_row(
                command.key,
                handler.options_syntax.get(command.key, getattr(command, "syntax", "")),
                handler.options_display.get(command.key, getattr(command, "desc", "")),
            )

        self.msg(rich=t)
