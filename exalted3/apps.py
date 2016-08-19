from django.apps import AppConfig

class Ex3Config(AppConfig):
    name = 'storyteller.exalted3'

    def ready(self):
        pass
        #import world.database.storyteller.signals