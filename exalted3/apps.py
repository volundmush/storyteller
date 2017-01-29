from django.apps import AppConfig

class Ex3Config(AppConfig):
    name = 'storyteller.exalted3'

    def ready(self):
        #import storyteller.exalted3.signals
        pass