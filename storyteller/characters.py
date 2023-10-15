from athanor.typeclasses.characters import AthanorCharacter as _OldCharacter


class StorytellerCharacter(_OldCharacter):
    story_handlers = []

    def get_story_handlers(self):
        return [getattr(self, x) for x in self.story_handlers]
