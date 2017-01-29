from __future__ import unicode_literals
from storyteller.base.customs import CustomSet

class Crafts(CustomSet):
    category_id = 1
    name = 'Crafts'


class Styles(CustomSet):
    category_id = 2
    name = 'Styles'


ALL_CUSTOMS = (Crafts, Styles,)