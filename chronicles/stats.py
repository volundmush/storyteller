from __future__ import unicode_literals
from storyteller.base import PhysicalAttribute, SocialAttribute, MentalAttribute, PhysicalSkill, SocialSkill
from storyteller.base import MentalSkill, PowerStat, Willpower as OldWillpower, Stat

# Advantages
class BloodPotency(PowerStat):
    key = 'Blood Potency'


class PrimalUrge(PowerStat):
    key = 'Primal Urge'


class Gnosis(PowerStat):
    key = 'Gnosis'


class Wyrd(PowerStat):
    key = 'Wyrd'


# Attributes

class Strength(PhysicalAttribute):
    id = 3
    key = 'Strength'
    list_order = 1


class Dexterity(PhysicalAttribute):
    id = 4
    key = 'Dexterity'
    list_order = 2


class Stamina(PhysicalAttribute):
    id = 5
    key = 'Stamina'
    list_order = 3


class Presence(SocialAttribute):
    id = 6
    key = 'Presence'
    list_order = 1


class Manipulation(SocialAttribute):
    id = 7
    key = 'Manipulation'
    list_order = 2


class Composure(SocialAttribute):
    id = 8
    key = 'Composure'
    list_order = 3


class Intelligence(MentalAttribute):
    id = 9
    key = 'Intelligence'
    list_order = 1


class Wits(MentalAttribute):
    id = 10
    key = 'Wits'
    list_order = 2


class Resolve(MentalAttribute):
    id = 11
    key = 'Resolve'
    list_order = 3

ALL_ATTRIBUTES = (Strength, Stamina, Dexterity, Presence, Manipulation, Composure, Intelligence, Wits, Resolve)

# Skills
# Mental

class Academics(MentalSkill):
    id = 12
    key = 'Academics'
    list_order = 0


class Computer(MentalSkill):
    id = 13
    key = 'Computer'
    list_order = 5


class Crafts(MentalSkill):
    id = 14
    key = 'Crafts'
    list_order = 10


class Investigation(MentalSkill):
    id = 15
    key = 'Investigation'
    list_order = 15


class Medicine(MentalSkill):
    id = 16
    key = 'Medicine'
    list_order = 20


class Occult(MentalSkill):
    id = 17
    key = 'Occult'
    list_order = 25


class Politics(MentalSkill):
    id = 18
    key = 'Politics'
    list_order = 30


class Science(MentalSkill):
    id = 19
    key = 'Science'
    list_order = 35


MENTAL_SKILLS = (Academics, Computer, Crafts, Investigation, Medicine, Occult, Politics, Science)

#Physical
class Athletics(PhysicalSkill):
    id = 20
    key = 'Athletics'
    list_order = 0


class Brawl(PhysicalSkill):
    id = 21
    key = 'Brawl'
    list_order = 5


class Drive(PhysicalSkill):
    id = 22
    key = 'Drive'
    list_order = 10


class Firearms(PhysicalSkill):
    id = 23
    key = 'Firearms'
    list_order = 15


class Larceny(PhysicalSkill):
    id = 24
    key = 'Larceny'
    list_order = 20


class Stealth(PhysicalSkill):
    id = 25
    key = 'Stealth'
    list_order = 25


class Survival(PhysicalSkill):
    id = 30
    key = 'Survival'
    list_order = 30


class Weaponry(PhysicalSkill):
    id = 35
    key = 'Weaponry'
    list_order = 35


PHYSICAL_SKILLS = (Athletics, Brawl, Drive, Firearms, Larceny, Stealth, Survival, Weaponry)

# Social
class AnimalKen(SocialSkill):
    id = 36
    key = 'Animal Ken'
    list_order = 0


class Empathy(SocialSkill):
    id = 37
    key = 'Empathy'
    list_order = 5


class Expression(SocialSkill):
    id = 38
    key = 'Expression'
    list_order = 10


class Intimidation(SocialSkill):
    id = 39
    key = 'Intimidation'
    list_order = 15


class Persuasion(SocialSkill):
    id = 40
    key = 'Persuasion'
    list_order = 20


class Socialize(SocialSkill):
    id = 41
    key = 'Socialize'
    list_order = 25


class Streetwise(SocialSkill):
    id = 42
    key = 'Streetwise'
    list_order = 30


class Subterfuge(SocialSkill):
    id = 43
    key = 'Subterfuge'
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
    key = 'Animalism'
    id = 1000


class Auspex(Discipline):
    key = 'Auspex'
    id = 1001

class Celerity(Discipline):
    key = 'Celerity'
    id = 1002


class Dominate(Discipline):
    key = 'Dominate'
    id = 1003


class Majesty(Discipline):
    key = 'Majesty'
    id = 1004


class Nightmare(Discipline):
    key = 'Nightmare'
    id = 1005


class Obfuscate(Discipline):
    key = 'Obfuscate'
    id = 1006


class Protean(Discipline):
    key = 'Protean'
    id = 1007


class Resilience(Discipline):
    key = 'Resilience'
    id = 1008


class Vigor(Discipline):
    key = 'Vigor'
    id = 1009


class ThebanSorcery(Discipline):
    key = 'ThebanSorcery'
    id = 1010


class Cruac(Discipline):
    key = 'Cruac'
    id = 1011


ALL_DISCIPLINES = (Animalism, Auspex, Celerity, Dominate, Majesty, Nightmare, Obfuscate, Protean, Resilience, Vigor,
                   ThebanSorcery, Cruac)


# Arcana

class Arcana(Stat):
    category = 'Arcana'
    id = 2000


class Death(Arcana):
    key = 'Death'
    id = 2000


class Fate(Arcana):
    key = 'Fate'
    id = 2001


class Forces(Arcana):
    key = 'Forces'
    id = 2002


class Life(Arcana):
    key = 'Life'
    id = 2003


class Matter(Arcana):
    key = 'Matter'
    id = 2004


class Mind(Arcana):
    key = 'Mind'
    id = 2005


class Prime(Arcana):
    key = 'Prime'
    id = 2006


class Space(Arcana):
    key = 'Space'
    id = 2007


class Spirit(Arcana):
    key = 'Spirit'
    id = 2008


class Time(Arcana):
    key = 'Time'
    id = 2009

ALL_ARCANA = (Death, Fate, Forces, Life, Matter, Mind, Prime, Space, Spirit, Time)

ALL_VAMPIRE = (BloodPotency,) + ALL_DISCIPLINES

ALL_MAGE = (Gnosis,) + ALL_ARCANA

ALL_STATS = ALL_ATTRIBUTES + ALL_SKILLS