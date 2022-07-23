from .exceptions import StoryDBException
from athanor.utils import partial_match
import typing
from storyteller import TEMPLATES


class Template:
    tem_colors = {}

    @classmethod
    def get_name(cls):
        return getattr(cls, "name", cls.__name__)

    def __str__(self):
        return getattr(self, "name", self.__class__.__name__)

    def __repr__(self):
        return '<Template: %s>' % str(self)

    def __init__(self, handler):
        self.handler = handler

    def initialize(self):
        pass


class TemplateHandler:

    def get_templates(self) -> dict[str, typing.Type[Template]]:
        return TEMPLATES

    def __init__(self, owner):
        self.owner = owner
        self.template = self.get_templates().get(self.owner.attributes.get(key="template", default="Mortal"), None)

    def __str__(self):
        return f"<{self.__class__.__name__}: {str(self.template)}>"

    def set(self, template_name: str):
        templates = self.get_templates()
        if not template_name:
            raise StoryDBException(f"Must enter a Template name!")
        if not (found := partial_match(template_name, templates.keys())):
            raise StoryDBException(f"No Template matches {template_name}.")
        self.template = templates[found](self)
        self.template.initialize()
