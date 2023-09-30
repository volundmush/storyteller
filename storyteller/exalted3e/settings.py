from storyteller.settings import *

INSTALLED_APPS.append("storyteller.exalted3e")

STORYTELLER_TEMPLATE_MODULES.append("storyteller.exalted3e.templates")

STORYTELLER_ADVANTAGES = ["Essence", "Willpower"]

STORYTELLER_ATTRIBUTES = ["Strength", "Dexterity", "Stamina", "Charisma", "Manipulation", "Appearance", "Intelligence",
                          "Wits",
                          "Perception"]

STORYTELLER_ABILITIES = ["Archery", "Athletics", "Awareness", "Brawl", "Bureaucracy", "Craft", "Dodge", "Integrity",
                         "Investigation", "Larceny", "Linguistics", "Lore", "Martial Arts", "Medicine", "Melee",
                         "Occult",
                         "Performance", "Presence", "Resistance", "Ride", "Sail", "Socialize", "Stealth", "Survival",
                         "Thrown", "War"]

STORYTELLER_SKILLS = STORYTELLER_ABILITIES

BASE_CHARACTER_TYPECLASS = "storyteller.exalted3e.typeclasses.characters.Ex3Character"

STORYTELLER_ROOT = "storyteller.exalted3e.stats.Root"
