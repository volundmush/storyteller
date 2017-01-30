from __future__ import unicode_literals
from storyteller.base.templates import Template
from storyteller.exbase.splats import ALL_MORTAL_X, ALL_SOLAR_X, ALL_TERRESTRIAL_X, ALL_ABYSSAL_X, ALL_INFERNAL_X
from storyteller.exbase.splats import ALL_SIDEREAL_X, ALL_ALCHEMICAL_X, ALL_LUNAR_X, ALL_SPIRIT_X, ALL_BLOODED_X
from storyteller.exbase.splats import ALL_JADEBORN_X, ALL_JADEBORN_Y, ALL_DRAGONKING_X, ALL_RAKSHA_X, ALL_RAKSHA_Y
from storyteller.exbase.splats import ALL_LIMINAL_X


class Mortal(Template):
    id = 1
    name = 'Mortal'
    x_name = 'Profession'
    x_classes = ALL_MORTAL_X
    willpower = 3


class _Exalt(Template):
    willpower = 5
    x_name = 'Caste'


class Solar(_Exalt):
    id = 2
    name = 'Solar'
    x_classes = ALL_SOLAR_X


class Abyssal(_Exalt):
    id = 3
    name = 'Abyssal'
    x_classes = ALL_ABYSSAL_X


class Infernal(_Exalt):
    id = 4
    name = 'Infernal'
    x_classes = ALL_INFERNAL_X


class Terrestrial(_Exalt):
    id = 5
    name = 'Terrestrial'
    x_name = 'Aspect'
    x_classes = ALL_TERRESTRIAL_X


class Sidereal(_Exalt):
    id = 6
    name = 'Sidereal'
    x_classes = ALL_SIDEREAL_X


class Alchemical(_Exalt):
    id = 7
    name = 'Alchemical'
    x_classes = ALL_ALCHEMICAL_X


class Lunar(_Exalt):
    id = 8
    name = 'Lunar'
    x_classes = ALL_LUNAR_X


class Spirit(_Exalt):
    id = 9
    name = 'Spirit'
    x_classes = ALL_SPIRIT_X


class GodBlooded(_Exalt):
    id = 10
    name = 'God-Blooded'
    x_classes = ALL_BLOODED_X


class Jadeborn(_Exalt):
    id = 11
    name = 'Jadeborn'
    x_classes = ALL_JADEBORN_X
    y_classes = ALL_JADEBORN_Y


class DragonKing(_Exalt):
    id = 12
    name = 'Dragon-King'
    x_name = 'Breed'
    x_classes = ALL_DRAGONKING_X


class Raksha(_Exalt):
    id = 13
    name = 'Raksha'
    x_name = 'Ascendant Grace'
    y_name = 'Shadowed Grace'
    x_classes = ALL_RAKSHA_X
    y_classes = ALL_RAKSHA_Y


# 3e Templates start here!
class Liminal(_Exalt):
    id = 20
    name = 'Liminal'
    x_name = 'Aspect'
    x_classes = ALL_LIMINAL_X


class Exigent(_Exalt):
    id = 21
    name = 'Exigent'