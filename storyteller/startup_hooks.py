"""
Server startstop hooks

This module contains functions called by Evennia at various
points during its startup, reload and shutdown sequence. It
allows for customizing the server operation as desired.

This module must contain at least these global functions:

at_server_init()
at_server_start()
at_server_stop()
at_server_reload_start()
at_server_reload_stop()
at_server_cold_start()
at_server_cold_stop()

"""


def at_server_init():
    """
    This is called first as the server is starting up, regardless of how.
    """
    pass


def at_server_start():
    """
    This is called every time the server starts up, regardless of
    how it was shut down.
    """
    from django.conf import settings
    from evennia.utils import class_from_module, callables_from_module
    import storyteller

    try:
        for k, v in settings.STORYTELLER_MODULES:
            path = None
            name = None
            key = None
            if not (isinstance(v, (list, tuple)) and len(v) >= 2):
                raise ValueError("Invalid storyteller module definition.")
            path = v[0]
            name = v[1]
            if len(v) >= 3:
                key = v[2]

            located = class_from_module(path)
            game = located(k, name, key=key)
            storyteller.GAMES[k] = game
    except Exception as err:
        print(err)


def at_server_stop():
    """
    This is called just before the server is shut down, regardless
    of it is for a reload, reset or shutdown.
    """
    pass


def at_server_reload_start():
    """
    This is called only when server starts back up after a reload.
    """
    pass


def at_server_reload_stop():
    """
    This is called only time the server stops before a reload.
    """
    pass


def at_server_cold_start():
    """
    This is called only when the server starts "cold", i.e. after a
    shutdown or a reset.
    """
    # Cleanup all AthanorPlayerCharacters that are online...
    # but can't be, because we crashed. This should put them all
    # into storage and update all time trackers.
    from athanor.typeclasses.characters import AthanorPlayerCharacter

    for obj in AthanorPlayerCharacter.objects.get_by_tag(
        key="puppeted", category="account"
    ):
        obj.at_post_unpuppet(last_logout=obj.db.last_online, shutdown=True)


def at_server_cold_stop():
    """
    This is called only when the server goes down due to a shutdown or
    reset.
    """
    pass
