from athanor.systems import System
from evennia.utils.utils import class_from_module, callables_from_module


class StorytellerSystem(System):
    name = "storyteller"

    def at_init(self):
        from storyteller import TEMPLATES
        from django.conf import settings

        for p in settings.STORY_TEMPLATE_PATHS:
            for k, v in callables_from_module(p).items():
                if not hasattr(v, "get_name"):
                    continue
                TEMPLATES[v.get_name()] = v


class ExaltedSystem(System):
    name = "exbase"

    def at_init(self):
        from django.conf import settings

        if settings.EXALTED_LOST_LUNAR_CASTES:
            from storyteller.exbase.templates import Lunar
            Lunar.sub_types = ["Full Moon", "Waxing Moon", "Half Moon", "Waning Moon", "No Moon"]

        if settings.EXALTED_POOL_MAX_WILL:
            from storyteller.exbase import templates as t
            t.get_willpower = t.get_willpower_max


class Exalted2System(System):
    name = "exalted2"

    def at_init(self):
        from django.conf import settings

        if settings.EXALTED_SHARDS:
            from storyteller.exbase.stats import _ABILITIES
            _ABILITIES.extend(["Firearms", "Drive"])
            # Todo: add the other things for Shards.

        if settings.EXALTED_POOL_MAX_VIRTUES:
            from storyteller.exalted2 import templates as t
            t.get_virtues = t.get_virtues_max
