from django.apps import AppConfig


class Storyteller(AppConfig):
    name = 'storyteller'

    def ready(self):
        pass
        #import world.database.fclist.signals