
class SheetRenderRequest:

    def __init__(self, viewer: "DefaultCharacter", target: "DefaultCharacter"):
        self.viewer = viewer
        self.target = target
        self.output = list()
        self.template = target.st_template.get()
        self.width = 78


class BaseSection:

    def render(self, request: SheetRenderRequest):
        pass
