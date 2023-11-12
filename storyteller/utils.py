import re

_RE_CAP = re.compile(r"(\b[a-zA-Z]+\b)")


def dramatic_capitalize(capitalize_string=""):
    def capitalize_word(match):
        word = match.group(0)
        # List of words to keep in lowercase
        lowercase_words = {"of", "the", "a", "and", "in"}
        # Capitalize word if not in lowercase_words, else keep it lower
        return (
            word.capitalize() if word.lower() not in lowercase_words else word.lower()
        )

    # Apply the function to each word
    return _RE_CAP.sub(capitalize_word, capitalize_string.lower())


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
