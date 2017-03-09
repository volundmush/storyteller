from __future__ import unicode_literals
from athanor.core.command import ModeCmdSet, ModeCommand, AthCommand
from athanor.utils.text import partial_match


class Editor(object):
    mode = None

    def __init__(self, actor, target):
        self.actor = actor
        self.character = target
        self.admin = actor.account.is_admin()
        self.choices = list()
        self.choices.append(target.story.template)
        self.choices.append(target.story.stats)
        self.choices += target.story.extras.extras

    def switch(self, choice=None):
        if not choice:
            raise ValueError("Nothing entered to switch modes to!")
        found = partial_match(choice, self.choices)
        if not found:
            raise ValueError("That is not a valid mode. Choices are: %s" % ', '.join([str(chc) for chc in self.choices]))
        self.mode = found
        return "Mode changed to: %s" % found

    def set(self, name=None, value=None):
        if not self.mode:
            raise ValueError("You are not in a mode!")
        if not self.mode.can_set:
            raise ValueError("This mode does not support set.")
        return self.mode.set(name, value)


class Chargen(AthCommand):
    key = 'chargen'
    system_name = 'CHARGEN'

    def func(self):
        self.character.ndb.story_edit = Editor(self.character, self.character)
        self.character.mode.switch(StoryEditCmds)
        self.character.execute_cmd('menu')


class StoryEditCommand(ModeCommand):

    def mode_display(self):
        if self.character.ndb.story_edit:
            if self.character.ndb.story_edit.mode:
                msg = self.character.ndb.story_edit.mode.menu_display(self.character)
                self.msg_lines(msg)
                return
        super(StoryEditCommand, self).mode_display()


class StoryEditSet(StoryEditCommand):
    key = 'set'
    mode_syntax = 'set <thing>=<value>'
    mode_explanation = 'Set value of a stat! Shitty placeholders.'
    display_post = False

    def func(self):
        if not self.character.ndb.story_edit:
            self.error("Unknown code error. Cannot continue.")
            return
        try:
            msg = self.character.ndb.story_edit.set(name=self.lhs, value=self.rhs)
        except ValueError as err:
            self.error(str(err))
            return
        self.sys_msg(msg)


class StoryEditMode(StoryEditCommand):
    key = 'mode'
    mode_syntax = 'mode <name>'
    mode_explanation = 'Change editing mode!'

    def func(self):
        if not self.character.ndb.story_edit:
            self.error("Unknown code error. Cannot continue.")
            return
        try:
            msg = self.character.ndb.story_edit.switch(choice=self.lhs)
        except ValueError as err:
            self.error(str(err))
            return
        self.sys_msg(msg)

class StoryEditCmds(ModeCmdSet):

    def at_cmdset_creation(self):
        super(StoryEditCmds, self).at_cmdset_creation()
        self.add(StoryEditSet)
        self.add(StoryEditMode)

