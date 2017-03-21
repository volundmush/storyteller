from storyteller.exbase.powers import Charm as _Charm

# Base classes...

class _SolarCharm(_Charm):
    tags = ('solar',)


class _Archery(_SolarCharm):
    tags = ('solar', 'solar_archery')


# CORE RULES lineup...

#ARCHERY - ID Range 100000 to 100999
class WiseArrow(_Archery):
    id = 100000
    name = 'Wise Arrow'
    cost = '1m'
    mins = 'Archery 2, Essence 1'
    type = 'Supplemental'
    keywords = ('Uniform',)
    duration = 'Instant'
    req_charms = 'None'
    req_stats = {1: 1, 100: 2}


class SightWithoutEyes(_Archery):
    id = 100001
    name = 'Sight Without Eyes'
    cost = '1m'
    mins = 'Archery 3, Essence 1'
    type = 'Reflexive'
    keywords = ('None',)
    duration = 'One Tick'
    req_charms = 'Wise Arrow'
    req_ids = (100000,)
    req_stats = {1: 1, 100: 3}


class BloodWithoutBalance(_Archery):
    id = 100002
    name = 'Blood Without Balance'
    cost = '3m'
    mins = 'Archery 4, Essence 1'
    type = 'Reflexive'
    keywords = ('Decisive-only',)
    duration = 'Instant'
    req_charms = 'Sight Without Eyes'
    req_ids = (100001,)
    req_stats = {1: 1, 100: 4}


class ForceWithoutFire(_Archery):
    id = 1000003
    name = 'Force Without Fire'
    cost = '3m'
    mins = 'Archery 4, Essence 1'
    type = 'Supplemental'
    keywords = ('Withering-only',)
    duration = 'Instant'
    req_charms = 'Sight Without Eyes'
    req_ids = (100001,)
    req_stats = {1: 1, 100: 4}


class TranceofUnhesitatingSpeed(_Archery):
    id = 100004
    name = "Trance of Unhesitating Speed"
    cost = '4m, 1wp'
    mins = 'Archery 3, Essence 1'
    type = 'Simple'
    keywords = ('Decisive-only',)
    duration = 'Instant'
    req_charms = 'Wise Arrow'
    req_ids = (100001,)
    req_stats = {1: 1, 100: 3}


class PhantomArrowTechnique(_Archery):
    id = 100005
    name = 'Phantom Arrow Technique'
    cost = '1m'
    mins = 'Archery 3, Essence 1'
    type = 'Reflexive'
    keywords = ('None',)
    duration = 'Instant'
    req_stats = {1: 1, 100: 3}


class FieryArrowAttack(_Archery):
    id = 100006
    name = 'Fiery Arrow Attack'
    cost = '2m'
    mins = 'Archery 4, Essence 1'
    type = 'Supplemental'
    keywords = ('Decisive-only',)
    duration = 'Instant'
    req_charms = 'Phantom Arrow Technique'
    req_ids = (100005,)
    req_stats = {1: 1, 100: 4}


class ThereIsNoWind(_Archery):
    id = 100007
    name = 'There Is No Wind'
    cost = '3m'
    mins = 'Archery 5, Essence 2'
    type = 'Reflexive'
    keywords = ('Dual',)
    duration = 'Instant'
    req_charms = 'Sight Without Eyes'
    req_ids = (100001,)
    req_stats = {1: 2, 100: 5}


class AccuracyWithoutDistance(_Archery):
    id = 100008
    name = 'Accuracy Without Distance'
    cost = '1m, 1wp'
    mins = 'Archery 5, Essence 2'
    type = 'Reflexive'
    keywords = ('Decisive-only',)
    duration = 'Instant'
    req_charms = 'Force Without Fire'
    req_ids = (1000003,)
    req_stats = {1: 2, 100: 5}


class ArrowStormTechnique(_Archery):
    id = 100009
    name = 'Arrow Storm Technique'
    cost = '5m, 1wp'
    mins = 'Archery 5, Essence 2'
    type = 'Simple'
    keywords = ('Decisive-only',)
    duration = 'Instant'
    req_charms = 'Trance of Unhesitating Speed'
    req_ids = (100004,)
    req_stats = {1: 2, 100: 5}