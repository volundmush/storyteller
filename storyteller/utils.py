import re


_RE_CAP_1 = re.compile(r"(?:^|(?<=[_\/\-\|\s()\+]))(?P<name1>[a-z]+)")
_RE_CAP_2 = re.compile(r"(^|(?<=[(\|\/]))(of|the|a|and|in)")
_RE_CAP_3 = re.compile(r"(^|(?<=[(\|\/]))(of|the|a|and|in)")


def dramatic_capitalize(capitalize_string=""):
    capitalize_string = _RE_CAP_1.sub(
        lambda find: find.group("name1").capitalize(), capitalize_string.strip().lower()
    )
    capitalize_string = _RE_CAP_2.sub(
        lambda find: find.group(1).lower(), capitalize_string
    )
    capitalize_string = _RE_CAP_3.sub(
        lambda find: find.group(1) + find.group(2).capitalize(), capitalize_string
    )
    for token in (" ", "-"):
        split_string = capitalize_string.split(token)
        capitalize_string = token.join(split_string)
    return capitalize_string


def get_story(character, load=True):
    if not character.ndb.story:
        from .handlers import GameHandler

        character.ndb.story = GameHandler(character)

    handler = character.ndb.story

    if load:
        try:
            handler.load()
        except ValueError as err:
            character.msg(err)

    return handler
