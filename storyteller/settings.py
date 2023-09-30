# Settings for the Storyteller Module. Remember, just change these in your settings.py, not here!

from athanor.settings import *

AT_SERVER_STARTSTOP_MODULE.append("storyteller.startup_hooks")

STORYTELLER_DEFAULT_TEMPLATE = "Mortal"

STORYTELLER_TEMPLATE_MODULES = []

INSTALLED_APPS.append("storyteller.storybase")
