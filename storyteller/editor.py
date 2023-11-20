import re
from django.conf import settings
from athanor.utils import partial_match, Operation
from athanor.parser import AthanorParser
from .utils import get_story


class StorytellerMenu(AthanorParser):
    def __init__(self, obj, target):
        super().__init__(obj)
        self.target = target
        self.story = get_story(target)
        self.commands = dict()
        self.mode = "Game"
        self.prepare()
        self.render_help()

    def check_valid(self, caller, txt: str, **kwargs):
        return bool(self.target)

    @property
    def handlers(self):
        return [handler for handler in self.story.handlers if handler.menu_access]

    def regenerate_commands(self):
        if not (handler := self.story.handlers_dict.get(self.mode, None)):
            return
        handler.generate_menu_commands(self.commands)

    def prepare(self):
        self.commands.clear()
        self.regenerate_commands()
        self.commands["show"] = (self.do_show, "show", "Display current Sheet")
        self.commands["mode"] = (self.do_mode, "mode <mode>", "Change Menu mode")
        self.commands["help"] = (self.do_help, "help", "Display this help menu")
        self.commands["exit"] = (self.do_exit, "exit", "Exit the menu")

    def render_help(self):
        self.msg(
            self.obj.account.styled_header(
                f"Storyteller '{self.mode}' Menu for: {self.target}"
            )
        )
        if handler := self.story.handlers_dict.get(self.mode, None):
            self.msg(handler.format_menu_help(self.obj))
        modes = ", ".join([str(x) for x in self.handlers])
        self.msg(self.obj.account.styled_separator("Mode Select"))
        self.msg(f"|wAvailable Modes:|n {modes}")

        t = self.obj.account.rich_table(
            "Command", "Syntax", "Description", title="Commands"
        )
        for k, v in self.commands.items():
            if len(v) not in (3, 5):
                continue
            if len(v) == 3:
                t.add_row(k, v[1], v[2])
            else:
                t.add_row(k, v[2], v[4])
        t.add_row(
            f"{settings.ATHANOR_MENU_BYPASS}<command>",
            "!<command>",
            "Executes a normal command",
        )

        self.msg(rich=t)

    def at_post_execute(self, caller, txt: str, matches: re.Match, **kwargs):
        pass

    def error_no_match(self, caller, txt: str, **kwargs):
        if callable(self.msg):
            self.msg("Invalid command. Type 'help' for a list of commands.")

    def do_execute(self, caller, txt: str, matches: re.Match, **kwargs):
        mdict = matches.groupdict()
        self.msg(repr(mdict))
        if not (cmd := mdict.get("cmd", "")):
            self.msg("Invalid command.")
            return
        cmd = cmd.lower()

        if not (command := partial_match(cmd, self.commands.keys())):
            self.msg("Invalid command. Type 'help' for a list of commands.")
            return

        data = self.commands[command]

        if len(data) not in (3, 5):
            self.msg("Invalid command data, please contact staff.")
            return

        if len(data) == 3:
            data[0](caller, matches, **kwargs)
        elif len(data) == 5:
            op_kwargs = {
                "user": self.obj.account,
                "character": self.obj.puppet,
                "target": data[0],
                "operation": data[1],
            }

            if data[3]:
                op_kwargs["kwargs"] = {
                    "path": mdict.get("lsargs", "").split("/"),
                    "value": mdict.get("rsargs", ""),
                }
            else:
                op_kwargs["kwargs"] = {"path": [], "value": mdict.get("args", "")}

            self.msg(repr(op_kwargs))

            op = Operation(**op_kwargs)
            op.execute()
            if "message" in op.results:
                self.obj.msg(op.results["message"])

            if op.results.get("redisplay_menu", False):
                self.prepare()
                self.render_help()

    def do_exit(self, caller, matches: re.Match, **kwargs):
        self.obj.text_callable = None
        self.obj.msg("Exiting storyteller menu.")

    def do_show(self, caller, matches, **kwargs):
        for line in self.story.get_sheet(self.obj.puppet):
            self.msg(line)

    def do_mode(self, caller, matches: re.Match, **kwargs):
        if not (mode := partial_match(matches.group("args") or "", self.handlers)):
            self.msg("Invalid mode.")
            return
        self.mode = str(mode)
        self.prepare()
        self.render_help()

    def do_help(self, caller, matches, **kwargs):
        self.render_help()
