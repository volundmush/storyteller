from django.db import models
from athanor.core.models import WithKey


class Game(models.Model):
    """
    This Model is used to seperate one game (Exalted 3, Chronicles of Darkness, etc) from another. This allows the
    single running database to potentially service multiple games.
    """
    key = models.CharField(max_length=255, db_index=True, unique=True)


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
    key = models.CharField(max_length=255, db_index=True)
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
    persona = models.ForeignKey('storyteller.Persona', related_name='traits')
    trait_id = models.PositiveIntegerField(default=0)
    answer = models.ForeignKey('storyteller.TraitAnswer', related_name='trait_characters')

    class Meta:
        unique_together = (('trait_id', 'persona'),)


class TraitAnswer(WithKey):
    pass


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


class SpecialtyName(models.Model):
    """
    Model is used for storing the names of Specialties so that if two Characters have the same specialty,
    it only exists once in the database.
    """
    game = models.ForeignKey('storyteller.Game', related_name='specialties')
    stat_id = models.PositiveIntegerField(default=0)
    key = models.CharField(max_length=255, db_index=True)
    creator = models.ForeignKey('objects.ObjectDB', related_name='+')
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('game', 'stat_id', 'key'),)


class Specialty(WithDotValue):
    """
    Model for storing Character-specific Specialty data.
    """
    persona = models.ForeignKey('storyteller.Persona', related_name='specialties')
    specialty = models.ForeignKey('storyteller.SpecialtyName', related_name='users')

    class Meta:
        unique_together = (('specialty', 'persona'),)


class ExtraSet(models.Model):
    game = models.ForeignKey('storyteller.Game', related_name='extras')
    category_id = models.PositiveIntegerField(default=0)
    sub_id = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = (('game', 'category_id', 'sub_id'),)


class ExtraName(models.Model):
    category = models.ForeignKey('storyteller.ExtraSet', related_name='entries', null=True, default=None)
    key = models.CharField(max_length=255, db_index=True)
    parent = models.ForeignKey('storyteller.ExtraName', null=True, default=None, related_name='specialties')
    creator = models.ForeignKey('objects.ObjectDB', related_name='+')
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('category', 'key', 'parent'),)


class Extra(WithDotValue):
    persona = models.ForeignKey('storyteller.Persona', related_name='extras')
    stat = models.ForeignKey('storyteller.ExtraName', related_name='users')
    context = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    many = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = (('persona', 'stat', 'context'),)


class Pool(models.Model):
    persona = models.ForeignKey('Persona', related_name='pools')
    pool_id = models.PositiveSmallIntegerField(default=0)
    points = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = (('persona', 'pool_id'),)


class PoolCommit(models.Model):
    pool = models.ForeignKey('storyteller.Pool', related_name='commits')
    key = models.CharField(max_length=255, db_index=True)
    value = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = (('pool', 'key'),)