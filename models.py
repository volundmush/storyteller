from django.db import models


class Game(models.Model):
    """
    This Model is used to seperate one game (Exalted 3, Chronicles of Darkness, etc) from another. This allows the
    single running database to potentially service multiple games.
    """
    name = models.CharField(max_length=255, db_index=True, unique=True)


class WithDotValue(models.Model):
    """
    Abstract class to represent general kinds of stats that have dot ratings. Skills, Merits, etc.
    """
    rating = models.PositiveSmallIntegerField(default=0, db_index=True)

    class Meta:
        abstract = True


class Persona(models.Model):
    """
    The big daddy of the Models. This is designed to accomodate both Exalted and Chronicles of Darkness.
    key = name of the character.
    parent = self referential foreign key, used for various character types like Demons or Social-build Solars. Allows
             one Character to have various sub-forms. Not currently implemented.
    template = The ID of the Template in use. (Solar, Mortal, Vampire, Mage, Lunar, etc.) Default is 1: Mortal.
    x, y, z splats = Splat variations per-template. For exalted, x_splat is the ID of the Caste/Aspect. For Cod,
            things like Werewolf Auspice or Vampire Clan. Y and Z are for Chronicles other subtypes.
    """
    game = models.ForeignKey('storyteller.Game', related_name='personas')
    name = models.CharField(max_length=255, db_index=True)
    parent = models.ForeignKey('storyteller.Persona', null=True, default=None, related_name='children')
    character = models.ForeignKey('objects.ObjectDB', related_name='personas')
    template = models.PositiveSmallIntegerField(default=1)
    x_splat = models.PositiveIntegerField(null=True)
    y_splat = models.PositiveIntegerField(null=True)
    z_splat = models.PositiveIntegerField(null=True)

    class Meta:
        unique_together = (('key', 'character', 'game'),)

    def __repr__(self):
        return '<Persona: %s>' % self.key

    def __str__(self):
        return self.key


class Trait(models.Model):
    """
    Sometimes a Template has other things that need to be answered. For instance, Lunars in Exalted have a
    'Totem Animal' field and Abyssals might have a 'Liege' field.
    """
    persona = models.ForeignKey('storyteller.Persona', related_name='traits')
    trait_id = models.PositiveIntegerField(default=0)
    value = models.CharField(max_length=255)

    class Meta:
        unique_together = (('trait_id', 'persona'),)


class Stat(WithDotValue):
    """
    Model used for storing Stat data. Attributes, Skills, Abilities, Advantages, etc.
    """
    persona = models.ForeignKey('storyteller.Persona', related_name='stats')
    stat_id = models.PositiveIntegerField(default=0, db_index=True)
    flag_1 = models.PositiveSmallIntegerField(default=0)
    flag_2 = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = (('persona', 'stat_id',),)


class Specialty(WithDotValue):
    """
    Model is used for storing the names of Specialties so that if two Characters have the same specialty,
    it only exists once in the database.
    """
    stat = models.ForeignKey('storyteller.Stat', related_name='specialties')
    name = models.CharField(max_length=255, db_index=True)

    class Meta:
        unique_together = (('stat', 'key'),)


class Custom(WithDotValue):
    """
    This Model exists for any kind of straightforward Stat-like trait where the name is up to the player, but it behaves
    like other Stats. Examples include specific Crafts from Exalted 3e. The Category # determines what kind of Custom
    Stat it is.
    """
    persona = models.ForeignKey('storyteller.Persona', related_name='customs')
    category = models.PositiveSmallIntegerField(default=0)
    name = models.CharField(max_length=255, db_index=True)

    class Meta:
        unique_together = (('persona', 'category', 'name'),)


class CustomSpecialty(WithDotValue):
    """
    Implements Specialties for Custom Stats. Same as other Specialties.
    """
    stat = models.ForeignKey('storyteller.Custom', related_name='specialties')
    name = models.CharField(max_length=255, db_index=True)

    class Meta:
        unique_together = (('stat', 'name'),)


class Merit(WithDotValue):
    """
    Model to contain all Merit and Merit-like traits for a character, such as Flaws and Backgrounds.
    """
    persona = models.ForeignKey('storyteller.Persona', related_name='merits')
    merit_id = models.PositiveIntegerField(default=0, db_index=True)
    context = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = (('persona', 'category', 'merit_id', 'context'),)


class Pool(models.Model):
    persona = models.ForeignKey('Persona', related_name='pools')
    pool_id = models.PositiveSmallIntegerField(default=0)
    points = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = (('persona', 'pool_id'),)


class PoolCommit(models.Model):
    pool = models.ForeignKey('storyteller.Pool', related_name='commits')
    name = models.CharField(max_length=255, db_index=True)
    value = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = (('pool', 'key'),)


class Power(WithDotValue):
    """
    Model to contain save data for all special powers in use. Example Word-powers would be Exalted Charms and Spells.
    There is some conceptual overlap with the Stat model here, because traits like 'Vampire Disciplines' could be
    stored here too. (They are not, they are considered Stats.) This is intended for powers which might have data that
    the Stat model cannot accomodate.

    The 'rating' field from WithDotValue is used for various purposes, but usually 'how many times have you purchased
    this power.'

    'Description' and 'Notes' are there for certain powers which go above and beyond even the needs of a 'rating',
    although those are rare. Examples include Werewolf Shadow Gifts and certain Exalted Charms with sub-powers. Storing
    JSON data allows these fields to be whatever they need to be.
    """
    persona = models.ForeignKey('storyteller.Persona', related_name='wordpowers')
    power_id = models.PositiveIntegerField(default=0, db_index=True)
    description = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)