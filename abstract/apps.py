from django.apps import AppConfig


class StorytellerConfig(AppConfig):
    name = 'storyteller.abstract'

    def ready(self):
        pass
        #import world.database.fclist.signals