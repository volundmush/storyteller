GAMES = {}


def init(settings, plugins):
    settings.AT_SERVER_STARTSTOP_MODULE.append("storyteller.startup_hooks")

    settings.STORYTELLER_MODULES = dict()

    settings.INSTALLED_APPS.append("storyteller")

    settings.STORYTELLER_ATTRIBUTE_OPTIONS = ("set", "tag")
    settings.STORYTELLER_SKILL_OPTIONS = ("set", "tag")

    settings.CMD_MODULES_CHARACTER.append("storyteller.commands")

    settings.STORYTELLER_DEFAULT_MODULE = None
