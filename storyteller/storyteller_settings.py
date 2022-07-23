# Settings for the Storyteller Module. Remember, just change these in your settings.py, not here!

from athanor.settings import *

INSTALLED_APPS.extend(
    [
        'storyteller.apps.Storyteller'
    ]
)

STORY_TEMPLATE_PATHS = []

SYSTEMS.extend([
    "storyteller.systems.StorytellerSystem"
])