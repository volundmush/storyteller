from __future__ import unicode_literals
from django.db import models
from storyteller.models import WithDotValue


class CharmSet(models.Model):
    category_id = models.PositiveSmallIntegerField(default=0, db_index=True)
    sub_id = models.PositiveSmallIntegerField(default=0, db_index=True)

    class Meta:
        unique_together = (('category_id', 'sub_id'),)


class CharmName(models.Model):
    charmset = models.ForeignKey('exalted3.CharmSet', related_name='charms')
    key = models.CharField(max_length=255, db_index=True)
    creator = models.ForeignKey('objects.ObjectDB', related_name='+')
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('charmset', 'key'),)

    def __str__(self):
        return self.key


class Charm(models.Model):
    persona = models.ForeignKey('storyteller.Persona', related_name='charms')
    charm = models.ForeignKey('exalted3.CharmName', related_name='users')
    quantity = models.PositiveSmallIntegerField(default=1)
    control = models.BooleanField(default=False)

    class Meta:
        unique_together = (('persona', 'charm'),)


class Style(models.Model):
    key = models.CharField(max_length=255, db_index=True, unique=True)
    creator = models.ForeignKey('objects.ObjectDB', related_name='+')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.key


class StyleStat(WithDotValue):
    style = models.ForeignKey('exalted3.Style', related_name='personas')
    persona = models.ForeignKey('storyteller.Persona', related_name='styles')

    class Meta:
        unique_together = (('style', 'persona',))


class StyleCharmName(models.Model):
    key = models.CharField(max_length=255, db_index=True, unique=True)
    style = models.ForeignKey('exalted3.Style', related_name='charms')
    creator = models.ForeignKey('objects.ObjectDB', related_name='+')
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('key', 'style'),)

    def __str__(self):
        return self.key


class StyleCharm(models.Model):
    persona = models.ForeignKey('storyteller.Persona', related_name='style_charms')
    charm = models.ForeignKey('exalted3.StyleCharmName', related_name='personas')
    quantity = models.PositiveSmallIntegerField(default=1)

    class Meta:
        unique_together = (('persona', 'charm'),)

class Craft(models.Model):
    key = models.CharField(max_length=255, db_index=True, unique=True)
    creator = models.ForeignKey('objects.ObjectDB', related_name='+')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.key


class CraftStat(WithDotValue):
    craft = models.ForeignKey('exalted3.Craft', related_name='personas')
    persona = models.ForeignKey('storyteller.Persona', related_name='crafts')

    class Meta:
        unique_together = (('craft', 'persona',))


class EvocationArtifact(models.Model):
    key = models.CharField(max_length=255, db_index=True, unique=True)
    creator = models.ForeignKey('objects.ObjectDB', related_name='+')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.key


class EvoCharmName(models.Model):
    key = models.CharField(max_length=255, db_index=True, unique=True)
    evo = models.ForeignKey('exalted3.EvocationArtifact', related_name='charms')
    creator = models.ForeignKey('objects.ObjectDB', related_name='+')
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('key', 'evo'),)

    def __str__(self):
        return self.key


class Evocation(models.Model):
    persona = models.ForeignKey('storyteller.Persona', related_name='evocations')
    charm = models.ForeignKey('exalted3.EvoCharmName', related_name='personas')
    quantity = models.PositiveSmallIntegerField(default=1)

    class Meta:
        unique_together = (('persona', 'charm'),)