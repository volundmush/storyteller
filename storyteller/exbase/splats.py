from storyteller.base.splats import Splat


# Mortal


class _Profession(Splat):
    pass


class Warrior(_Profession):
    id = 1
    name = 'Warrior'


class Priest(_Profession):
    id = 2
    name = 'Priest'


class Savant(_Profession):
    id = 3
    name = 'Savant'


class Criminal(_Profession):
    id = 4
    name = 'Criminal'


class Broker(_Profession):
    id = 5
    name = 'Broker'


ALL_MORTAL_X = (Warrior, Priest, Savant, Criminal, Broker)


# Solar


class _Caste(Splat):
    pass


class Dawn(_Caste):
    id = 6
    name = 'Dawn'


class Zenith(_Caste):
    id = 7
    name = 'Zenith'


class Twilight(_Caste):
    id = 8
    name = 'Twilight'


class Night(_Caste):
    id = 9
    name = 'Night'


class Eclipse(_Caste):
    id = 10
    name = 'Eclipse'


ALL_SOLAR_X = (Dawn, Zenith, Twilight, Night, Eclipse)


# Abyssal


class Dusk(_Caste):
    key = 'Dusk'
    id = 11


class Midnight(_Caste):
    key = 'Midnight'
    id = 12


class Day(_Caste):
    key = 'Day'
    id = 13


class Daybreak(_Caste):
    key = 'Daybreak'
    id = 14


class Moonshadow(_Caste):
    key = 'Moonshadow'
    id = 15


ALL_ABYSSAL_X = (Dusk, Midnight, Day, Daybreak, Moonshadow)


# Infernal


class Slayer(_Caste):
    id = 16
    name = 'Slayer'


class Malefactor(_Caste):
    id = 17
    name = 'Malefactor'


class Defiler(_Caste):
    id = 18
    name = 'Defiler'


class Scourge(_Caste):
    id = 19
    name = 'Scourge'


class Fiend(_Caste):
    id = 20
    name = 'Fiend'


ALL_INFERNAL_X = (Slayer, Malefactor, Defiler, Scourge, Fiend)


# Terrestrial


class _Aspect(Splat):
    pass


class Fire(_Aspect):
    key = 'Fire'
    id = 21


class Water(_Aspect):
    key = 'Water'
    id = 22


class Air(_Aspect):
    key = 'Air'
    id = 23


class Earth(_Aspect):
    key = 'Earth'
    id = 24


class Wood(_Aspect):
    key = 'Wood'
    id = 25


ALL_TERRESTRIAL_X = (Fire, Water, Air, Earth, Wood)


# Sidereal


class Journeys(_Caste):
    id = 26
    name = 'Journeys'


class Serenity(_Caste):
    id = 27
    name = 'Serenity'


class Battles(_Caste):
    id = 28
    name = 'Battles'


class Secrets(_Caste):
    id = 29
    name = 'Secrets'


class Endings(_Caste):
    id = 30
    name = 'Endings'


ALL_SIDEREAL_X = (Journeys, Serenity, Battles, Secrets, Endings,)


# Alchemical


class Orichalcum(_Caste):
    id = 31
    name = 'Orichalcum'


class Moonsilver(_Caste):
    id = 31
    name = 'Moonsilver'


class Jade(_Caste):
    id = 32
    name = 'Jade'


class Starmetal(_Caste):
    id = 33
    name = 'Starmetal'


class Soulsteel(_Caste):
    id = 34
    name = 'Soulsteel'


class Adamant(_Caste):
    id = 35
    name = 'Adamant'


ALL_ALCHEMICAL_X = (Orichalcum, Moonsilver, Jade, Starmetal, Soulsteel, Adamant)


# Lunar
class FullMoon(_Caste):
    id = 36
    name = 'Full Moon'


class ChangingMoon(_Caste):
    id = 37
    name = 'Changing Moon'


class NoMoon(_Caste):
    id = 38
    name = 'No Moon'


class WaxingMoon(_Caste):
    id = 39
    name = 'Waxing Moon'


class HalfMoon(_Caste):
    id = 40
    name = 'Half Moon'


class WaningMoon(_Caste):
    id = 41
    name = 'Waning Moon'


ALL_LUNAR_X = (FullMoon, ChangingMoon, NoMoon, WaxingMoon, HalfMoon, WaningMoon)


# Spirit
class Elemental(_Caste):
    id = 42
    name = 'Elemental'


class Demon(_Caste):
    id = 43
    name = 'Demon'


class God(_Caste):
    id = 44
    name = 'God'


ALL_SPIRIT_X = (Elemental, Demon, God)


# God-Blooded
class Fae(_Caste):
    id = 45
    name = 'Fae'


class Ghost(_Caste):
    id = 46
    name = 'Ghost'


class Solar(_Caste):
    id = 47
    name = 'Solar'


class Lunar(_Caste):
    id = 48
    name = 'Lunar'


class Sidereal(_Caste):
    id = 49
    name = 'Sidereal'


class Abyssal(_Caste):
    id = 50
    name = 'Abyssal'


class Infernal(_Caste):
    id = 51
    name = 'Infernal'


class Jadeborn(_Caste):
    id = 52
    name = 'Jadeborn'


ALL_BLOODED_X = (Fae, Ghost, Solar, Lunar, Sidereal, Abyssal, Infernal, Jadeborn) + ALL_SPIRIT_X


# Jadeborn

class Artisan(_Caste):
    id = 53
    name = 'Artisan'


class JWarrior(_Caste):
    id = 54
    name = 'Warrior'


class Worker(_Caste):
    id = 55
    name = 'Worker'


ALL_JADEBORN_X = (Artisan, JWarrior, Worker)


class Enlightened(_Caste):
    id = 1
    name = 'Enlightened'


class UnEnlightened(_Caste):
    id = 2
    name = 'UnEnlightened'


ALL_JADEBORN_Y = (Enlightened, UnEnlightened)


# Dragon Kings


class _Breed(Splat):
    pass


class Anklok(_Breed):
    id = 56
    name = 'Anklok'


class Mosok(_Breed):
    id = 57
    name = 'Mosok'


class Pterok(_Breed):
    id = 58
    name = 'Pterok'


class Raptok(_Breed):
    id = 59
    name = 'Raptok'


ALL_DRAGONKING_X = (Anklok, Mosok, Pterok, Raptok)

# Raksha

class RWarrior(_Caste):
    id = 60
    name = 'Warrior'


class Diplomat(_Caste):
    id = 61
    name = 'Diplomat'


class RWorker(_Caste):
    id = 62
    name = 'Worker'


class Entertainer(_Caste):
    id = 63
    name = 'Entertainer'


ALL_RAKSHA_X = (RWarrior, Diplomat, RWorker, Entertainer)

ALL_RAKSHA_Y = ALL_RAKSHA_X


# Liminal

class Blood(_Aspect):
    id = 100
    name = 'Blood'


class Breath(_Aspect):
    id = 101
    name = 'Breath'


class Flesh(_Aspect):
    id = 102
    name = 'Flesh'


class Marrow(_Aspect):
    id = 103
    name = 'Marrow'


class Soil(_Aspect):
    id = 104
    name = 'Soil'


ALL_LIMINAL_X = (Blood, Breath, Flesh, Marrow, Soil)