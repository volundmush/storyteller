import re

_RE_CAP = re.compile(r"\b[a-zA-Z0-9]+('\w)?\b")
# List of words to keep in lowercase
_lowercase_words = {"of", "the", "a", "and", "in"}


def dramatic_capitalize(capitalize_string=""):
    def capitalize_word(match):
        word = match.group(0)

        # Check if the word is preceded by an apostrophe and followed by 's
        if word.lower() in _lowercase_words:
            return word.lower()
        elif word.endswith("'s"):
            return word.capitalize()
        elif word.endswith("'S"):
            return word[:-2].capitalize() + "'s"
        else:
            return word.capitalize()

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
