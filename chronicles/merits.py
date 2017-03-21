from storyteller.base.merits import Merit


class _Mental(Merit):
    book = 'Chronicles of Darkness'
    category = 'Merit'
    sub_category = 'Mental'


class _Physical(Merit):
    book = 'Chronicles of Darkness'
    category = 'Merit'
    sub_category = 'Physical'


class _Social(Merit):
    book = 'Chronicles of Darkness'
    category = 'Merit'
    sub_category = 'Social'


class _Supernatural(Merit):
    book = 'Chronicles of Darkness'
    category = 'Merit'
    sub_category = 'Supernatural'


class _Fighting(Merit):
    book = 'Chronicles of Darkness'
    category = 'Merit'
    sub_category = 'Fighting'


# Chronicles of Darkness - Mental Merits


class AreaOfExpertise(_Mental):
    id = 1
    name = 'Area of Expertise'
    req_stats = {11: 2}
    versions = (1,)

    def prereq_check(self, checker):
        # Resolve 2 and one Skill Specialty
        pass


class CommonSense(_Mental):
    id = 2
    name = 'Common Sense'
    versions = (3,)


class DangerSense(_Mental):
    id = 3
    name = 'Danger Sense'
    versions = (2,)


class DirectionSense(_Mental):
    id = 4
    name = 'Direction Sense'
    versions = (1,)


class EideticMemory(_Mental):
    id = 5
    name = 'Eidetic Memory'
    versions = (2,)


class EncyclopedicKnowledge(_Mental):
    id = 6
    name = 'Encyclopedic Knowledge'
    versions = (2,)


class EyefortheStrange(_Mental):
    id = 7
    name = 'Eye for the Strange'
    versions = (2,)
    req_stats = {11: 2, 17: 1}


class FastReflexes(_Mental):
    id = 8
    name = 'Fast Reflexes'
    versions = (1, 2, 3)
    req_stats = {10: 3, 4: 3}

    def prereq_check(self, checker):
        # Wits 3 or Dexterity 3
        pass


class GoodTimeManagement(_Mental):
    id = 9
    name = 'Good Time Management'
    versions = (1,)
    req_stats = {12: 2, 19: 2}

    def prereq_check(self, checker):
        # Academics 2 or Science 2
        pass


class HolisticAwareness(_Mental):
    id = 10
    name = 'Holstic Awareness'
    versions = (1,)


class Indomitable(_Mental):
    id = 11
    name = 'Indomitable'
    versions = (2,)
    req_stats = {11: 3}


class InterdisciplinarySpecialty(_Mental):
    id = 12
    name = 'Interdisciplinary Specialty'
    versions = (1,)

    def prereq_check(self, checker):
        pass  #Skill at 3 or higher with a Specialty.


class InvestigativeAide(_Mental):
    id = 13
    name = 'Investigative Aide'
    versions = (1,)

    def prereq_check(self, checker):
        pass #Skill at 3+.


class InvestigativeProdigy(_Mental):
    id = 14
    name = 'Investigative Prodigy'
    versions = (1, 2, 3, 4, 5)
    req_stats = {15: 3, 10: 3}


class Language(_Mental):
    id = 15
    name = 'Language'
    versions = (1,)


class Library(_Mental):
    id = 16
    name = 'Library'
    versions = (1, 2, 3)


class MeditativeMind(_Mental):
    id = 17
    name = 'Meditative Mind'
    versions = (1, 2, 4)


class Multilingual(_Mental):
    id = 18
    name = 'Multilingual'
    versions = (1,)


class Patient(_Mental):
    id = 19
    name = 'Patient'
    versions = (1,)


class ProfessionalTraining(_Mental):
    id = 20
    name = 'Professional Training'
    versions = (1, 2, 3, 4, 5)
    context_choices = ('Academic', 'Artist', 'Athlete', 'Cop', 'Criminal', 'Detective', 'Doctor', 'Engineer', 'Hacker',
                       'Hit Man', 'Journalist', 'Laborer', 'Occultist', 'Politician', 'Professional', 'Religious Leader',
                       'Scientist', 'Socialite', 'Stuntman', 'Survivalist', 'Soldier', 'Technician', 'Thug', 'Vagrant')


class ToleranceforBiology(_Mental):
    id = 21
    name = 'Tolerance for Biology'
    versions = (1,)
    req_stats = {11: 3}


class TrainedObserver(_Mental):
    id = 22
    name = 'Trained Observer'
    versions = (1, 3)
    req_stats = {10: 3, 8: 3}

    def prereq_check(self, checker):
        pass #Or check.


class ViceRidden(_Mental):
    id = 23
    name = 'Vice-Ridden'
    versions = (2,)


class Virtuous(_Mental):
    id = 24
    name = 'Virtuous'
    versions = (2,)


# Chronicles of Darkness - Physical Merits

class Ambidextrous(_Physical):
    id = 25
    name = 'Ambidextrous'
    versions = (3,)


class AutomotiveGenius(_Physical):
    id = 26
    name = 'Automotive Genius'
    versions = (1,)
    req_stats = {14: 3, 22: 1, 19: 1}


class CrackDriver(_Physical):
    id = 27
    name = 'Crack Driver'
    versions = (2, 3)
    req_stats = {22: 3}


class Demolisher(_Physical):
    id = 28
    name = 'Demolisher'
    versions = (1, 2, 3)
    req_stats = {3: 3, 9: 3}

    def prereq_check(self, checker):
        pass #or check


class DoubleJointed(_Physical):
    id = 29
    name = 'Double Jointed'
    versions = (2,)
    req_stats = {4: 3}


class FleetofFoot(_Physical):
    id = 30
    name = 'Fleet of Foot'
    versions = (1, 2, 3)
    req_stats = {20: 2}


class Giant(_Physical):
    id = 31
    name = 'Giant'
    versions = (3,)


class Hardy(_Physical):
    id = 32
    name = 'Hardy'
    versions = (1, 2, 3)
    req_stats = {5: 3}


class Greyhound(_Physical):
    id = 33
    name = 'Greyhound'
    versions = (1,)
    req_stats = {5: 3, 10: 3, 20: 3}


class IronStamina(_Physical):
    id = 34
    name = 'Iron Stamina'
    versions = (1, 2, 3)
    req_stats = {5: 3, 11: 3}
    # make it an or check.


class Parkour(_Physical):
    id = 35
    name = 'Parkour'
    versions = (1, 2, 3, 4, 5)
    req_stats = {4: 3, 20: 2}


class QuickDraw(_Physical):
    id = 36
    name = 'Quick Draw'
    versions = (1,)
    req_stats = {10: 3}


class Relentless(_Physical):
    id = 37
    name = 'Relentless'
    versions = (1,)
    req_stats = {20: 2, 5: 3}


class SeizingtheEdge(_Physical):
    id = 38
    name = 'Seizing the Edge'
    versions = (2,)
    req_stats = {10: 3, 8: 3}


class SleightofHand(_Physical):
    id = 39
    name = 'Sleight of Hand'
    versions = (2,)
    req_stats = {24: 3}


class SmallFramed(_Physical):
    id = 40
    name = 'Small-Framed'
    versions = (2,)


class StuntDriver(_Physical):
    id = 41
    name = 'Stunt Driver'
    versions = (1, 2, 3, 4)
    req_stats = {22: 3, 4: 3, 10: 3}


# Chronicles of Darkness - Social Merits


class Allies(_Social):
    id = 42
    name = 'Allies'
    versions = (1, 2, 3, 4, 5)


class AlternateIdentity(_Social):
    id = 43
    name = 'Alternate Identity'
    versions = (1, 2, 3)


class Anonymity(_Social):
    id = 44
    name = 'Anonymity'
    versions = (1, 2, 3, 4, 5)

    def prereq_check(self, checker):
        pass # cannot have fame


class Barfly(_Social):
    id = 45
    name = 'Barfly'
    versions = (2,)
    req_stats = {41: 2}


class ClosedBook(_Social):
    id = 46
    name = 'Closed Book'
    versions = (1, 2, 3, 4, 5)
    req_stats = {11: 3, 7: 3}


class Contacts(_Social):
    id = 47
    name = 'Contacts'
    versions = (1, 2, 3, 4, 5)


class Fame(_Social):
    id = 48
    name = 'Fame'
    versions = (1, 2, 3)

    def prereq_check(self, checker):
        pass # cannot have Anonymity


class FastTalking(_Social):
    id = 49
    name = 'Fast-Talking'
    versions = (1, 2, 3, 4, 5)
    req_stats = {7: 3, 43: 2}


class Fixer(_Social):
    id = 50
    name = 'Fixer'
    versions = (2,)
    req_stats = {10: 3}
    req_merits = {47: 2}


class HobbyistClique(_Social):
    id = 51
    name = 'Hobbyist Clique'
    versions = (2,)


class Inspiring(_Social):
    id = 52
    name = 'Inspiring'
    versions = (3,)
    req_stats = {6: 3}


class IronWill(_Social):
    id = 53
    name = 'Iron Will'
    versions = (2,)
    req_stats = {11: 4}


class Mentor(_Social):
    id = 54
    name = 'Mentor'
    versions = (1, 2, 3, 4, 5)


class MysteryCultInitiation(_Social):
    id = 55
    name = 'Mystery Cult Initiation'
    versions = (1, 2, 3, 4, 5)


class Pusher(_Social):
    id = 56
    name = 'Pusher'
    versions = (1,)
    req_stats = {40: 2}


class Resources(_Social):
    id = 57
    name = 'Resources'
    versions = (1, 2, 3, 4, 5)


class Retainer(_Social):
    id = 58
    name = 'Retainer'
    versions = (1, 2, 3, 4, 5)


class SafePlace(_Social):
    id = 59
    name = 'Safe Place'
    versions = (1, 2, 3, 4, 5)


class SmallUnitTactics(_Social):
    id = 60
    name = 'Small Unit Tactics'
    versions = (2,)
    req_stats = {6: 2}


class SpinDoctor(_Social):
    id = 61
    name = 'Spin Doctor'
    versions = (1,)
    req_stats = {7: 3, 43: 2}


class Staff(_Social):
    id = 62
    name = 'Staff'
    versions = (1, 2, 3, 4, 5)


class Status(_Social):
    id = 63
    name = 'Status'
    versions = (1, 2, 3, 4, 5)


class StrikingLooks(_Social):
    id = 64
    name = 'Striking Looks'
    versions = (1, 2)


class Sympathetic(_Social):
    id = 65
    name = 'Sympathetic'
    versions = (2,)


class TableTurner(_Social):
    id = 66
    name = 'Table Turner'
    versions = (1,)
    req_stats = {8: 3, 7: 3, 10: 3}


class TakesOneToKnowOne(_Social):
    id = 67
    name = 'Takes One to Know One'
    versions = (1,)


class Taste(_Social):
    id = 68
    name = 'Taste'
    versions = (1,)
    req_stats = {14: 2}

    def prereq_check(self, checker):
        pass # specialty in Crafts or Expression


class TrueFriend(_Social):
    id = 69
    name = 'True Friend'
    versions = (3,)


class Untouchable(_Social):
    id = 70
    name = 'Untouchable'
    versions = (1,)
    req_stats = {7: 3, 43: 2}


# Chronicles of Darkness - Supernatural Merits
class AuraReading(_Supernatural):
    id = 71
    name = 'Aura Reading'
    versions = (3,)


class AutomaticWriting(_Supernatural):
    id = 72
    name = 'Automatic Writing'
    versions = (2,)


class Biokinesis(_Supernatural):
    id = 73
    name = 'Biokinesis'
    versions = (1, 2, 3, 4, 5)


class Clairvoyance(_Supernatural):
    id = 74
    name = 'Clairvoyance'
    versions = (3,)


class Cursed(_Supernatural):
    id = 75
    name = 'Cursed'
    versions = (2,)


class LayingonHands(_Supernatural):
    id = 76
    name = 'Laying on Hands'
    versions = (3,)


class Medium(_Supernatural):
    id = 77
    name = 'Medium'
    versions = (3,)
    req_stats = {37: 2}


class MindofaMadman(_Supernatural):
    id = 78
    name = 'Mind of a Madman'
    versions = (2,)
    req_stats = {37: 3}


class OmenSensitivity(_Supernatural):
    id = 79
    name = 'Omen Sensitivity'
    versions = (3,)


class NumbingTouch(_Supernatural):
    id = 80
    name = 'Numbing Touch'
    versions = (1, 2, 3, 4, 5)


class Psychokinesis(_Supernatural):
    id = 81
    name = 'Psychokinesis'
    versions = (3, 5)


class Psychometry(_Supernatural):
    id = 82
    name = 'Psychometry'
    versions = (3,)


class Telekinesis(_Supernatural):
    id = 83
    name = 'Telekinesis'
    versions = (1, 2, 3, 4, 5)


class Telepathy(_Supernatural):
    id = 84
    name = 'Telepathy'
    versions = (3, 5)


class ThiefofFate(_Supernatural):
    id = 85
    name = 'Thief of Fate'
    versions = (3,)


class UnseenSense(_Supernatural):
    id = 86
    name = 'Unseen Sense'
    versions = (2,)


# Chronicles of Darkness - Fighting Merits


class ArmedDefense(_Fighting):
    id = 87
    name = 'Armed Defense'
    versions = (1, 2, 3, 4, 5)
    req_stats = {35: 2, 4: 3}
    req_merits = {91: 1}


class CheapShot(_Fighting):
    id = 88
    name = 'Cheap Shot'
    versions = (2,)
    req_stats = {43: 2}
    req_merits = {}


class ChokeHold(_Fighting):
    id = 89
    name = 'Choke Hold'
    versions = (2,)
    req_stats = {21: 2}


class CloseQuartersCombat(_Fighting):
    id = 90
    name = 'Close Quarters Combat'
    versions = (1, 2, 3, 4, 5)
    req_stats = {21: 3, 20: 2, 10: 3}


class DefensiveCombat(_Fighting):
    id = 91
    name = 'Defensive Combat'
    versions = (1,)
    req_stats = {21: 1, 35: 1}

    def prereq_check(self, checker):
        pass # or check


class FightingFinesse(_Fighting):
    id = 92
    name = 'Fighting Finesse'
    versions = (2,)
    req_stats = {4: 3} # also a specialty in weaponry or brawl


class Firefight(_Fighting):
    id = 93
    name = 'Firefight'
    versions = (1, 2, 3)
    req_stats = {4: 3, 8: 3, 20: 2, 23: 2}


class Grappling(_Fighting):
    id = 94
    name = 'Grappling'
    versions = (1, 2, 3)
    req_stats = {20: 2, 21: 2, 3: 2, 5: 3}


class HeavyWeapons(_Fighting):
    id = 95
    name = 'Heavy Weapons'
    versions = (1, 2, 3, 4, 5)
    req_stats = {5: 3, 3: 3, 20: 2, 35: 2}


class ImprovisedWeaponry(_Fighting):
    id = 96
    name = 'Improvised Weaponry'
    versions = (1, 2, 3)
    req_stats = {35: 1, 10: 3}


class IronSkin(_Fighting):
    id = 97
    name = 'Iron Skin'
    versions = (2, 3)
    req_stats = {5: 3}
    req_merits = {100: 2, 103: 2} # make it an or


class LightWeapons(_Fighting):
    id = 98
    name = 'Light Weapons'
    versions = (1, 2, 3, 4, 5)
