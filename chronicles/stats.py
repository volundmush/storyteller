from __future__ import unicode_literals
from storyteller.base import PhysicalAttribute, SocialAttribute, MentalAttribute, PhysicalSkill, SocialSkill
from storyteller.base import MentalSkill, PowerStat, Willpower as OldWillpower, Stat

# Advantages
class BloodPotency(PowerStat):
    name = 'Blood Potency'


class PrimalUrge(PowerStat):
    name = 'Primal Urge'


class Gnosis(PowerStat):
    name = 'Gnosis'


class Wyrd(PowerStat):
    name = 'Wyrd'


# Attributes

class Strength(PhysicalAttribute):
    id = 3
    name = 'Strength'
    list_order = 1


class Dexterity(PhysicalAttribute):
    id = 4
    name = 'Dexterity'
    list_order = 2


class Stamina(PhysicalAttribute):
    id = 5
    name = 'Stamina'
    list_order = 3


class Presence(SocialAttribute):
    id = 6
    name = 'Presence'
    list_order = 1


class Manipulation(SocialAttribute):
    id = 7
    name = 'Manipulation'
    list_order = 2


class Composure(SocialAttribute):
    id = 8
    name = 'Composure'
    list_order = 3


class Intelligence(MentalAttribute):
    id = 9
    name = 'Intelligence'
    list_order = 1


class Wits(MentalAttribute):
    id = 10
    name = 'Wits'
    list_order = 2


class Resolve(MentalAttribute):
    id = 11
    name = 'Resolve'
    list_order = 3

ALL_ATTRIBUTES = (Strength, Stamina, Dexterity, Presence, Manipulation, Composure, Intelligence, Wits, Resolve)

# Skills
# Mental

class Academics(MentalSkill):
    id = 12
    name = 'Academics'
    list_order = 0


class Computer(MentalSkill):
    id = 13
    name = 'Computer'
    list_order = 5


class Crafts(MentalSkill):
    id = 14
    name = 'Crafts'
    list_order = 10


class Investigation(MentalSkill):
    id = 15
    name = 'Investigation'
    list_order = 15


class Medicine(MentalSkill):
    id = 16
    name = 'Medicine'
    list_order = 20


class Occult(MentalSkill):
    id = 17
    name = 'Occult'
    list_order = 25


class Politics(MentalSkill):
    id = 18
    name = 'Politics'
    list_order = 30


class Science(MentalSkill):
    id = 19
    name = 'Science'
    list_order = 35


MENTAL_SKILLS = (Academics, Computer, Crafts, Investigation, Medicine, Occult, Politics, Science)

#Physical
class Athletics(PhysicalSkill):
    id = 20
    name = 'Athletics'
    list_order = 0


class Brawl(PhysicalSkill):
    id = 21
    name = 'Brawl'
    list_order = 5


class Drive(PhysicalSkill):
    id = 22
    name = 'Drive'
    list_order = 10


class Firearms(PhysicalSkill):
    id = 23
    name = 'Firearms'
    list_order = 15


class Larceny(PhysicalSkill):
    id = 24
    name = 'Larceny'
    list_order = 20


class Stealth(PhysicalSkill):
    id = 25
    name = 'Stealth'
    list_order = 25


class Survival(PhysicalSkill):
    id = 30
    name = 'Survival'
    list_order = 30


class Weaponry(PhysicalSkill):
    id = 35
    name = 'Weaponry'
    list_order = 35


PHYSICAL_SKILLS = (Athletics, Brawl, Drive, Firearms, Larceny, Stealth, Survival, Weaponry)

# Social
class AnimalKen(SocialSkill):
    id = 36
    name = 'Animal Ken'
    list_order = 0


class Empathy(SocialSkill):
    id = 37
    name = 'Empathy'
    list_order = 5


class Expression(SocialSkill):
    id = 38
    name = 'Expression'
    list_order = 10


class Intimidation(SocialSkill):
    id = 39
    name = 'Intimidation'
    list_order = 15


class Persuasion(SocialSkill):
    id = 40
    name = 'Persuasion'
    list_order = 20


class Socialize(SocialSkill):
    id = 41
    name = 'Socialize'
    list_order = 25


class Streetwise(SocialSkill):
    id = 42
    name = 'Streetwise'
    list_order = 30


class Subterfuge(SocialSkill):
    id = 43
    name = 'Subterfuge'
    list_order = 35


SOCIAL_SKILLS = (AnimalKen, Empathy, Expression, Intelligence, Persuasion, Socialize, Streetwise, Subterfuge)


ALL_SKILLS = (Academics, Computer, Crafts, Investigation, Medicine, Occult, Politics, Science,
              Athletics, Brawl, Drive, Firearms, Larceny, Stealth, Survival, Weaponry,
              AnimalKen, Empathy, Expression, Intelligence, Persuasion, Socialize, Streetwise, Subterfuge)


# Disciplines
class Discipline(Stat):
    category = 'Discipline'
    default = 0
    id = 1000


class Animalism(Discipline):
    name = 'Animalism'
    id = 1000


class Auspex(Discipline):
    name = 'Auspex'
    id = 1001

class Celerity(Discipline):
    name = 'Celerity'
    id = 1002


class Dominate(Discipline):
    name = 'Dominate'
    id = 1003


class Majesty(Discipline):
    name = 'Majesty'
    id = 1004


class Nightmare(Discipline):
    name = 'Nightmare'
    id = 1005


class Obfuscate(Discipline):
    name = 'Obfuscate'
    id = 1006


class Protean(Discipline):
    name = 'Protean'
    id = 1007


class Resilience(Discipline):
    name = 'Resilience'
    id = 1008


class Vigor(Discipline):
    name = 'Vigor'
    id = 1009


class ThebanSorcery(Discipline):
    name = 'ThebanSorcery'
    id = 1010


class Cruac(Discipline):
    name = 'Cruac'
    id = 1011


ALL_DISCIPLINES = (Animalism, Auspex, Celerity, Dominate, Majesty, Nightmare, Obfuscate, Protean, Resilience, Vigor,
                   ThebanSorcery, Cruac)


# Arcana

class Arcana(Stat):
    category = 'Arcana'
    id = 2000


class Death(Arcana):
    name = 'Death'
    id = 2000


class Fate(Arcana):
    name = 'Fate'
    id = 2001


class Forces(Arcana):
    name = 'Forces'
    id = 2002


class Life(Arcana):
    name = 'Life'
    id = 2003


class Matter(Arcana):
    name = 'Matter'
    id = 2004


class Mind(Arcana):
    name = 'Mind'
    id = 2005


class Prime(Arcana):
    name = 'Prime'
    id = 2006


class Space(Arcana):
    name = 'Space'
    id = 2007


class Spirit(Arcana):
    name = 'Spirit'
    id = 2008


class Time(Arcana):
    name = 'Time'
    id = 2009

ALL_ARCANA = (Death, Fate, Forces, Life, Matter, Mind, Prime, Space, Spirit, Time)

ALL_VAMPIRE = (BloodPotency,) + ALL_DISCIPLINES

ALL_MAGE = (Gnosis,) + ALL_ARCANA

ALL_STATS = ALL_ATTRIBUTES + ALL_SKILLS