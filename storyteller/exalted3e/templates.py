from storyteller.base import Template


class _Ex3Template(Template):
    power_stat = "Essence"
    native_charms = None
    game = "Exalted 3e"

    def calculate_personal_motes(self, target: "DefaultCharacter"):
        return 0

    def calculate_peripheral_motes(self, target: "DefaultCharacter"):
        return 0


class Mortal(_Ex3Template):
    fields = []


class Solar(_Ex3Template):
    fields = ["Caste"]
    field_defaults = {"Caste": "Dawn"}
    field_choices = {"Caste": ["Dawn", "Zenith", "Twilight", "Night", "Eclipse"]}
    native_charms = "Solar"


class Lunar(_Ex3Template):
    fields = ["Caste", "Spirit Shape"]
    field_defaults = {"Caste": "Casteless"}
    field_choices = {"Caste": ["Full Moon", "Changing Moon", "No Moon", "Casteless"]}
    native_charms = "Lunar"


class DragonBlooded(_Ex3Template):
    name = "Dragon-Blooded"
    fields = ["Aspect"]
    field_defaults = {"Aspect": "Air"}
    field_choices = {"Aspect": ["Air", "Earth", "Fire", "Water", "Wood"]}
    native_charms = "Dragon-Blooded"


class Sidereal(_Ex3Template):
    fields = ["Caste"]
    field_defaults = {"Caste": "Journeys"}
    field_choices = {"Caste": ["Journeys", "Battles", "Secrets", "Endings", "Serenity"]}
    native_charms = "Sidereal"


class Abyssal(Solar):
    fields = ["Caste"]
    field_defaults = {"Caste": "Dusk"}
    field_choices = {"Caste": ["Dusk", "Midnight", "Daybreak", "Day", "Moonshadow"]}
    native_charms = "Abyssal"


class Infernal(Solar):
    fields = ["Caste"]
    field_defaults = {"Caste": "Azimuth"}
    field_choices = {"Caste": ["Azimuth", "Ascendant", "Horizon", "Nadir", "Penumbra"]}
    native_charms = "Infernal"


class Alchemical(_Ex3Template):
    fields = ["Caste"]
    field_defaults = {"Caste": "Orichalcum"}
    field_choices = {"Caste": ["Orichalcum", "Moonsilver", "Starmetal", "Jade", "Soulsteel", "Adamant"]}
    native_charms = "Alchemical"


class Liminal(_Ex3Template):
    fields = ["Aspect"]
    field_defaults = {"Aspect": "Blood"}
    field_choices = {"Aspect": ["Blood", "Breath", "Flesh", "Marrow", "Soil"]}
    native_charms = "Liminal"


class Getimian(_Ex3Template):
    fields = ["Caste"]
    field_defaults = {"Caste": "Spring"}
    field_choices = {"Caste": ["Spring", "Summer", "Autumn", "Winter"]}
    native_charms = "Getimian"


class Exigent(_Ex3Template):
    fields = ["Tier", "Type", "Patron"]
    field_defaults = {"Tier": "Terrestrial", "Type": "Essence"}
    field_choices = {"Tier": ["Terrestrial", "Celestial"], "Type": ["Essence", "Attribute", "Ability"]}
    native_charms = "Exigent"


class Architect(_Ex3Template):
    fields = ["City"]
    native_charms = "Architect"


class DreamSouled(_Ex3Template):
    name = "Dream-Souled"
    native_charms = "Dream-Souled"


class Sovereign(_Ex3Template):
    native_charms = "Sovereign"


class Hearteater(_Ex3Template):
    native_charms = "Hearteater"


class Umbral(_Ex3Template):
    native_charms = "Umbral"



ALL_TEMPLATES = [Mortal, Solar, Lunar, DragonBlooded, Sidereal, Abyssal, Infernal, Alchemical, Liminal, Getimian,
                 Exigent, Architect, DreamSouled, Sovereign, Hearteater, Umbral]
