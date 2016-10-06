# Settings for the Storyteller Module. Remember, just change these in your settings.py, not here!

from athanor.athanor_settings import *

#INSTALLED_APPS = INSTALLED_APPS + ('storyteller.abstract.apps.StorytellerConfig',)

# EXALTED 2

# If true, all Virtues will be assumed to be at max values for mote calculations. It's the same as having 5 in them all.
# This does not affect Virtue channels or the ratings, only how pool calculations treat them.
EX2_POOL_MAX_VIRTUES = False

# If true, Willpower will be considered 10 for calculating Essence pools.
EX2_POOL_MAX_WILLPOWER = False

# If true, Terrestrial Breeding will be assumed to be this for mote pools if not already higher.
EX2_POOL_DEFAULT_BREEDING = 0

# If true, the Greater of (Essence or Breeding) will be used in place of Breeding for Terrestrial mote pools.
EX2_POOL_TERRESTIAL_ESSENCE__GT__BREEDING = False

# If true, Mortals are always considered Awakened and have a mote pool whether they have the Merit or not.
EX2_POOL_AWAKENED_MORTALS = False

# Styles for different Martial Arts tiers.
EX2_TERRESTRIAL_STYLES = ['Crimson Pentacle Blade Style', 'Terrestrial Hero Style', 'Even Blade Style',
                          'First Pulse Style', 'Five-Dragon Style', 'Fivefold Shadow Hand Style',
                          'Golden Exhalation Style', 'Golden Janissary Style', 'Ill Lily Style', 'Jade Mountain Style',
                          'Lightning Hoof Style', 'Night Breeze Style', 'Orgiastic Fugitive Style',
                          'Seafaring Hero Style', 'Swaying Grass Dance Style', 'Terrible Ascent-Driven Beast Style',
                          'The Path of the Arbiter Style', 'White Veil Style', 'Live Wire Style', 'Black Tide Style',
                          'Dagger Wind Style', 'Flame and Stone Style', 'Shadow Hunter Style']

EX2_CELESTIAL_STYLES = ['Dark Messiah Style', 'Hungry Ghost Style', 'Laughing Wounds Style',
                        'Thousand Wounds Gear Style', 'Eve of Heaven Style', 'Air Dragon Style', 'Earth Dragon Style',
                        'Fire Dragon Style', 'Water Dragon Style', 'Wood Dragon Style', 'Black Claw Style',
                        'Infernal Monster Style', 'Lunar Hero Style', 'White Reaper Style', 'Crane Style',
                        'Crystal Chameleon Style', 'Throne Shadow Style', 'Violet Bier of Sorrows Style',
                        'Celestial Monkey Style', 'Arms of the Unconquered Sun Style', 'Dreaming Pearl Courtesan Style',
                        'Ebon Shadow Style', 'Mantis Style', 'Righteous Devil Style', 'Silver-Voiced Nightingale Style',
                        'Snake Style', 'Solar Hero Style', 'Tiger Style', 'Art of Forceful Declaration Style',
                        'Art of Meditative Discussion Style', 'Art of Relentless Persuasion Style',
                        'Art of Victorious Concession Style']

EX2_SIDEREAL_STYLES = ['Border of Kaleidoscopic Logic Style', 'Charcoal March of Spiders Style',
                       'Citrine Poxes of Contagion Style', 'Obsidian Shards of Infinity Style',
                       'Prismatic Arrangement of Creation Style', 'Quicksilver Hand of Dreams Style',
                       'Sapphire Veil of Passion Style', 'Scarlet-Patterned Battlefield Style']