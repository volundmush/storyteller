from storyteller.base import StatNode
from athanor.utils import partial_match, validate_name


class DotStat:

    def set(self, user: "DefaultCharacter", target: "DefaultCharacter", path: list[str], value: str):
        try:
            if not path:
                raise ValueError(f"No {self.singular_name} Name given.")
            handler = getattr(target, self.handler_name)
            name, before, after, attr = handler.set_rank(path[0], value)
        except ValueError as err:
            pass
        except Exception as err:
            pass

        # if we got here, the operation was successful and needs to be reported.

    def tag(self, user: "DefaultCharacter", target: "DefaultCharacter", path: list[str], value: str):
        try:
            if not path:
                raise ValueError(f"No {self.singular_name} name given.")
            handler = getattr(target, self.handler_name)
            tag, before, after, attr = handler.set_tag(path[0], value)
        except ValueError as err:
            pass
        except Exception as err:
            pass


class Advantages(DotStat, StatNode):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.options = ("set",)
        self.singular_name = "Advantage"


class Attributes(DotStat, StatNode):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.options = ("set", "tag")
        self.singular_name = "Attribute"
        self.handler_name = "st_attributes"


class Abilities(DotStat, StatNode):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.options = ("set", "tag", "remove_zero")
        self.singular_name = "Ability"
        self.handler_name = "st_abilities"


class Styles(DotStat, StatNode):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.options = ("set", "flexible", "remove_zero")
        self.singular_name = "Martial Art Style"
        self.handler_name = "st_styles"


class _WordPowerNode(StatNode):

    def add(self, user: "DefaultCharacter", target: "DefaultCharacter", path: list[str], value: str):
        try:
            if not path:
                raise ValueError(f"No {self.singular_name} Name given.")
            # Charms and Spells need a path of <category>/<subcategory>=<name> so we need a path of 2 items.
            if len(path) != 2:
                raise ValueError(f"Invalid path for {self.singular_name}. Need <category>/<subcategory>.")

            handler = getattr(target, self.handler_name)
            results = handler.add(path[0], path[1], value)
        except ValueError as err:
            # TODO: Add alerts
            return
        except Exception as err:
            # TODO: Add alerts
            return

        # if we got here, the operation was successful and needs to be reported.

    def tag(self, user: "DefaultCharacter", target: "DefaultCharacter", path: list[str], value: str):
        try:
            if not path:
                raise ValueError(f"No {self.singular_name} Name given.")
            # Charms and Spells need a path of <category>/<subcategory>/<name>=<value> so we need a path of 3 items.
            if len(path) != 3:
                raise ValueError(f"Invalid path for {self.singular_name}. Need <category>/<subcategory>/<name>.")

            handler = getattr(target, self.handler_name)
            results = handler.add(path[0], path[1], value)
        except ValueError as err:
            # TODO: Add alerts
            return
        except Exception as err:
            # TODO: Add alerts
            return


class Charms(_WordPowerNode):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handler_name = "st_charms"


class Native(Charms):

    def get_native(self, target: "DefaultCharacter") -> str:
        native = target.st_template.get().native_charms
        if not native:
            raise ValueError(f"{target} does not have a native Charm category.")
        return native

    def add(self, user: "DefaultCharacter", target: "DefaultCharacter", path: list[str], value: str):
        try:
            if not len(path) == 1:
                raise ValueError(f"Invalid path for {self.singular_name}. Need <category>.")
            native = self.get_native(target)
        except ValueError as err:
            # TODO: Add alerts
            return

        path.insert(0, native)
        return super().add(user, target, path, value)

    def tag(self, user: "DefaultCharacter", target: "DefaultCharacter", path: list[str], value: str):
        try:
            if not len(path) == 2:
                raise ValueError(f"Invalid path for {self.singular_name}. Need <category>/<subcategory>.")
            native = self.get_native(target)
        except ValueError as err:
            # TODO: Add alerts
            return

        path.insert(0, native)
        return super().tag(user, target, path, value)


class Martial(Native):

    def get_native(self, target: "DefaultCharacter") -> str:
        return "Martial Arts"


class Spells(_WordPowerNode):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handler_name = "st_spells"


class Template(StatNode):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.options = ("set",)

    def set(self, user: "DefaultCharacter", target: "DefaultCharacter", path: list[str], value: str):
        """
        Set the target's Template to the given value.
        """
        templates = list(self.parent.templates.values())
        if not value:
            raise ValueError(f"No template given. Choices are: {', '.join(templates)}")
        if not (template_found := partial_match(value, templates)):
            raise ValueError(f"Template {value} not found. Choices are: {', '.join(templates)}")
        template_found.change(target)

    def find_node(self, target: "DefaultCharacter", path: list[str]) -> tuple["StatNode", list[str]]:
        return self, []


class Fields(StatNode):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.options = ("set",)

    def set(self, user: "DefaultCharacter", target: "DefaultCharacter", path: list[str], value: str):
        """
        Set the target's Template to the given value.
        """
        template = target.template
        if not value:
            raise ValueError(f"No field given. Choices are: {', '.join(template.fields)}")
        if not (field_found := partial_match(value, template.fields)):
            raise ValueError(f"Field {value} not found. Choices are: {', '.join(template.fields)}")
        template.set_field(target, field_found, value)

    def find_node(self, target: "DefaultCharacter", path: list[str]) -> tuple["StatNode", list[str]]:
        return self, []


class Evocations(StatNode):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handler_name = "st_evocations"


class Root(StatNode):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.nodes = [
            Template("Template"),
            Fields("Fields"),
            Advantages("Advantages"),
            Attributes("Attributes"),
            Abilities("Abilities"),
            Styles("Styles"),
            Charms("Charms"),
            Native("Native"),
            Martial("Martial"),
            Spells("Spells"),
            Evocations("Evocations")
        ]
