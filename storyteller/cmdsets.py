from evennia import CmdSet
from .commands import CmdSheet


class StorytellerCmdSet(CmdSet):

    def at_cmdset_creation(self):
        super().at_cmdset_creation()
        self.add(CmdSheet)
