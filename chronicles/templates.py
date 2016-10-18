from __future__ import unicode_literals
from storyteller.base import Template as OldTemplate, Splat
from storyteller.chronicles.stats import ALL_STATS, BloodPotency, Gnosis
from storyteller.chronicles.stats import ALL_VAMPIRE, ALL_MAGE, ALL_DISCIPLINES
from storyteller.chronicles.pools import Willpower, Mana, Vitae

# TEMPLATES
class Template(OldTemplate):
    stat_list = ALL_STATS


# Mortal
class Mortal(Template):
    key = 'Mortal'
    id = 1
    pool_list = (Willpower)
    stat_list = ALL_STATS
    extra_stats = ALL_DISCIPLINES


# Vampire
class Clan(Splat):
    pass

class Daeva(Clan):
    key = 'Daeva'
    id = 1


class Gangrel(Clan):
    key = 'Gangrel'
    id = 2


class Mekhet(Clan):
    key = 'Mekhet'
    id = 3


class Nosferatu(Clan):
    key = 'Nosferatu'
    id = 4


class Ventrue(Clan):
    key = 'Ventrue'
    id = 5


VAMPIRE_X = {1: Daeva, 2: Gangrel, 3: Mekhet, 4: Nosferatu, 5: Ventrue}


class Covenant(Splat):
    pass

class CarthianMovement(Covenant):
    key = 'Carthian Movement'
    id = 1


class CircleoftheCrone(Covenant):
    key = 'Circle of the Crone'
    id = 2


class Invictus(Covenant):
    key = 'Invictus'
    id = 3


class LanceaetSanctum(Covenant):
    key = 'Lancea et Sanctum'
    id = 4


class OrdoDracul(Covenant):
    key = 'Ordo Dracul'
    id = 5


VAMPIRE_Y = {1: CarthianMovement, 2: CircleoftheCrone, 3: Invictus, 4: LanceaetSanctum, 5: OrdoDracul}


class Vampire(Template):
    key = 'Vampire'
    id = 2
    pool_list = (Willpower, Vitae)
    extra_stats = ALL_VAMPIRE
    x_name = 'Clan'
    y_name = 'Covenant'
    x_choices = VAMPIRE_X
    y_choices = VAMPIRE_Y

# Mage

class Path(Splat):
    pass

class Acanthus(Path):
    key = 'Acanthus'
    id = 1


class Mastigos(Path):
    key = 'Mastigos'
    id = 2


class Moros(Path):
    key = 'Moros'
    id = 3


class Obrimos(Path):
    key = 'Obrimos'
    id = 4


class Thyrsus(Path):
    key = 'Thyrsus'
    id = 5


MAGE_X = {1: Acanthus, 2: Mastigos, 3: Moros, 4: Obrimos, 5: Thyrsus}


class Order(Splat):
    pass


class AdamantineArrow(Order):
    key = 'Adamantine Arrow'
    id = 1


class GuardiansoftheVeil(Order):
    key = 'Guardians of the Veil'
    id = 2


class Mysterium(Order):
    key = 'Mysterium'
    id = 3


class SilverLadder(Order):
    key = 'Silver Ladder'
    id = 4


class FreeCouncil(Order):
    key = 'Free Council'
    id = 5


class SeersoftheThrone(Order):
    key = 'Seers of the Throne'
    id = 6


MAGE_Y = {1: AdamantineArrow, 2: GuardiansoftheVeil, 3: Mysterium, 4: SilverLadder, 5: FreeCouncil, 6: SeersoftheThrone}


class Legacy(Splat):
    pass


class TheEleventhQuestion(Legacy):
    key = 'The Eleventh Question'
    id = 1

MAGE_Z = {1: TheEleventhQuestion, }


class Mage(Template):
    key = 'Mage'
    id = 4
    pool_list = (Willpower, Mana)
    stat_list = ALL_STATS
    extra_stats = ALL_MAGE
    x_choices = MAGE_X
    y_choices = MAGE_Y
    z_choices = MAGE_Z
    x_name = 'Path'
    y_name = 'Order'
    z_name = 'Legacy'

TEMPLATE_MAP = {1: Mortal, 4: Mage}