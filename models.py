from django.db import models
from evennia.utils.ansi import ANSIString
from athanor.core.models import WithKey

class Game(models.Model):
    key = models.CharField(max_length=255, db_index=True, unique=True)

class WithDotValue(models.Model):
    rating = models.PositiveSmallIntegerField(default=0, db_index=True)

    class Meta:
        abstract = True

    @property
    def display_name(self):
        return str(self)

    @property
    def display_prefix(self):
        return ' '

    def sheet_format(self, width=23, no_prefix=False, fill_char='.', colors=None):
        if not colors:
            colors = {'statname': 'n', 'statfill': 'n', 'statdot': 'n'}
        display_name = ANSIString('{%s%s{n' % (colors['statname'], self.display_name))
        if no_prefix:
            prefix = ' '
        else:
            prefix = ANSIString('{r%s{n' % self.display_prefix)
        final_display = prefix + display_name
        if self.rating > width - len(final_display) - 1:
            dot_display = ANSIString('{%s%s{n' % (colors['statdot'], self.rating))
        else:
            dot_display = ANSIString('{%s%s{n' % (colors['statdot'], '*' * int(self)))
        fill_length = width - len(final_display) - len(dot_display)
        fill = ANSIString('{%s%s{n' % (colors['statfill'], fill_char * fill_length))
        return final_display + fill + dot_display


class Persona(models.Model):
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
    persona = models.ForeignKey('storyteller.Persona', related_name='stats')
    stat_id = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        unique_together = (('persona', 'stat_id',),)



class SpecialtyName(models.Model):
    game = models.ForeignKey('storyteller.Game', related_name='specialties')
    stat_id = models.PositiveIntegerField(default=0)
    key = models.CharField(max_length=255, db_index=True)
    creator = models.ForeignKey('objects.ObjectDB', related_name='+')
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('game', 'stat_id', 'key'),)


class Specialty(WithDotValue):
    persona = models.ForeignKey('storyteller.Persona', related_name='specialties')
    specialty = models.ForeignKey('storyteller.SpecialtyName', related_name='users')

    class Meta:
        unique_together = (('specialty', 'persona'),)


class MeritName(models.Model):
    game = models.ForeignKey('storyteller.Game', related_name='merits')
    category_id = models.PositiveSmallIntegerField(default=0)
    key = models.CharField(max_length=255, db_index=True)
    creator = models.ForeignKey('objects.ObjectDB', related_name='+')
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('game', 'category_id', 'key'),)


class Merit(models.Model):
    persona = models.ForeignKey('storyteller.Persona', related_name='merits')
    merit = models.ForeignKey('storyteller.MeritName')
    context = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = (('persona', 'merit', 'context'),)


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