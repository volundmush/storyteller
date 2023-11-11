from django.db import models


class SheetInfo(models.Model):
    """
    A one-to-one link that relates characters to Storyteller sheets.
    """

    character = models.OneToOneField(
        "objects.ObjectDB",
        on_delete=models.CASCADE,
        related_name="sheet",
        primary_key=True,
    )
    # This string must match the name of a Game object loaded by the server.
    game = models.CharField(max_length=30, blank=False, null=False)
    # The Template the character is - Vampire, Garou, Solar, Mortal, whatever.
    template = models.CharField(
        max_length=30, blank=False, null=False, default="Mortal"
    )

    def __str__(self):
        return self.template

    def __repr__(self):
        return f"<{self.character}'s {self.game} Template: {self.template}>"


class TemplateField(models.Model):
    """
    This model stores a character's Storyteller Fields, like Clan, Tribe, Caste, etc.
    """

    sheet = models.ForeignKey(
        SheetInfo, on_delete=models.CASCADE, related_name="fields"
    )
    field = models.CharField(max_length=30, blank=False, null=False)
    value = models.CharField(max_length=30, blank=False, null=False)

    def __str__(self):
        return self.value

    def __repr__(self):
        return (
            f"<{self.sheet.character}'s {self.field} Field: {self.value} ({self.id})>"
        )

    class Meta:
        unique_together = (("sheet", "field"),)


class HasData(models.Model):
    """
    Abstract model to provide a data field, since it's used everywhere.
    """

    data = models.JSONField(blank=False, null=True, default=dict)

    class Meta:
        abstract = True


class HasValue(models.Model):
    """
    Abstract model to provide these two fields, since they're used everywhere.
    """

    value = models.IntegerField(blank=False, null=False, default=0)

    class Meta:
        abstract = True


class HasValueData(HasValue, HasData):
    """
    Convenience wrapper for the above two abstract models.
    """

    class Meta:
        abstract = True


class Stat(HasData):
    """
    This model normalizes storage of Stat names.
    """

    # Example category names: Attributes, Abilities, Advantages, Backgrounds, Merits, Flaws, Disciplines, Spheres, Styles,
    # Arcana, etc.
    category = models.CharField(max_length=30, blank=False, null=False)
    # The name of the stat itself, like Strength, Celerity, Animal Ken, etc.
    name = models.CharField(max_length=30, blank=False, null=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<{self.category}: {self.name} ({self.id})>"

    class Meta:
        unique_together = (("category", "name"),)


class StatRank(HasValueData):
    """
    Relational table which stores a character's Stat ranks.

    Since many kinds of Stats, like Merits, can be purchased multiple times, this table includes a
    context field for determining just what kind of purchase it is.

    For instance, each purchase of the merit "Artifact" in Exalted covers a separate Artifact,
    so the context is the artifact's name or category, like "The Distaff" or "Grand Daiklave".

    For ordinary stats, like Strength, the context is left as an empty string.
    """

    sheet = models.ForeignKey(SheetInfo, on_delete=models.CASCADE, related_name="stats")
    stat = models.ForeignKey(Stat, on_delete=models.CASCADE, related_name="ranks")
    context = models.CharField(max_length=100, blank=True, null=False, default="")
    # As it implements HasValueData, we also have a value and data field here.

    def __str__(self):
        if self.context:
            return f"{self.context}"
        return str(self.stat)

    def __repr__(self):
        return f"<{self.sheet.character}'s {self.stat.category}: {self.stat} ({self.value}) ({self.id})>"

    class Meta:
        unique_together = (("sheet", "stat", "context"),)


class Power(HasData):
    """
    This model normalizes storage of Power names. These are used by powers which are much more complicated than stats,
    and often are categorized in elaborate hierarchies.

    The most prominent example is Charms and Spells from Exalted. in that case, the hierarchy is:
    (in order of: family, category, subcategory, name)
    ("Charms", "Solar", "Melee", "Fire and Stones Strike")
    ("Charms", "Lunar", "Intelligence", "Counting the Elephant's Wrinkles")
    ("Spells", "Sorcery", "Terrestrial", "Demon of the First Circle")
    ("Spells", "Necromancy", "Shadowlands", "Summon Ghost")
    """

    family = models.CharField(max_length=12, blank=False, null=False)
    category = models.CharField(max_length=30, blank=False, null=False)
    subcategory = models.CharField(max_length=30, blank=False, null=False)
    name = models.CharField(max_length=80, blank=False, null=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<{self.family}: {self.subcategory} {self.category}: {self.name} ({self.id})>"

    class Meta:
        unique_together = (("family", "category", "subcategory", "name"),)


class PowerRank(HasValueData):
    """
    Relates a Power with a Character sheet. This is where power "purchases" are stored.
    """

    sheet = models.ForeignKey(
        SheetInfo, on_delete=models.CASCADE, related_name="powers"
    )
    power = models.ForeignKey(Power, on_delete=models.CASCADE, related_name="ranks")
    # As it implements HasValueData, we also have a value and data field here.

    def __str__(self):
        return str(self.power)

    def __repr__(self):
        return f"<{self.sheet.character}'s {self.power.category} {self.power.subcategory}: {self.power} ({self.value}) ({self.id})>"

    class Meta:
        unique_together = (("sheet", "power"),)


class StatPower(models.Model):
    """
    Certain Powers are closely tied to a Stat.
    The primary example is Martial Arts Charms in Exalted 3e, which are powers only available to characters
    who have ranks in a specific style, like Wood Dragon Style or Golden Janissary Style.
    """

    stat = models.ForeignKey(Stat, on_delete=models.CASCADE, related_name="powers")
    name = models.CharField(max_length=80, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (("stat", "name"),)


class StatPowerRank(HasValueData):
    """
    Handles 'purchases' of StatPowers on a character sheet.
    """

    sheet = models.ForeignKey(
        SheetInfo, on_delete=models.CASCADE, related_name="stat_powers"
    )
    power = models.ForeignKey(StatPower, on_delete=models.CASCADE, related_name="ranks")

    def __str__(self):
        return str(self.power)

    class Meta:
        unique_together = (("sheet", "power"),)


class CustomPower(HasValueData):
    """
    A CustomPower is linked to a stat AND a context.

    This is primarily intended to be used with Exalted 3e's implementation of Evocations, powers linked to Artifacts.
    In that case, the stat row being pointed at would be the Artifact.

    An example, the character would have the merit, "Artifact: The Distaff", and their custom power is the evocation,
    "Poppet-Knitting Practice". Since Evocations are unique, they are simply stored alongside the purchase because there's
    no point in creating a normalized database of them.

    """

    stat = models.ForeignKey(StatRank, on_delete=models.CASCADE, related_name="customs")
    name = models.CharField(max_length=80, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (("stat", "name"),)
