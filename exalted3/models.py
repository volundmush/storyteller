from __future__ import unicode_literals
from decimal import Decimal
from django.db import models
from django.db.models import Q, Sum
from evennia.utils.ansi import ANSIString
from storyteller.abstract.models import AbstractPersona, AbstractTemplate, AbstractTrait, AbstractTraitValue, \
    AbstractPersonaTraitValue, AbstractSheetColor, AbstractCategory, \
    AbstractStat, AbstractStatTag, AbstractPersonaStat, AbstractMerit, AbstractPersonaMerit, AbstractPool, \
    AbstractPersonaPool, AbstractPersonaCommit
from athanor.library import partial_match, sanitize_string, dramatic_capitalize


class Template(AbstractTemplate):
    pass


class Persona(AbstractPersona):
    pass


class SheetColor(AbstractSheetColor):
    pass


class Trait(AbstractTrait):
    pass


class TraitValue(AbstractTraitValue):
    pass


class PersonaTraitValue(AbstractPersonaTraitValue):
    pass


class Category(AbstractCategory):
    pass


class Stat(AbstractStat):
    pass


class StatTag(AbstractStatTag):
    pass


class PersonaStat(AbstractPersonaStat):
    pass


class Merit(AbstractMerit):
    pass


class PersonaMerit(AbstractPersonaMerit):
    pass


class Pool(AbstractPool):
    pass


class PersonaPool(AbstractPersonaPool):
    pass


class PersonaCommit(AbstractPersonaCommit):
    pass


"""
class ExpKind(models.Model):
    game = models.ForeignKey('storyteller.Game', related_name='experiences')
    key = models.CharField(max_length=50, db_index=True)

    class Meta:
        unique_together = (("game", "key"),)

    @property
    def rules(self):
        return self.game.rules['experience'][self.key]

    def __str__(self):
        return self.rules['name']

    @property
    def list_order(self):
        return self.rules['list_order']

class ExpLink(models.Model):
    kind = models.ForeignKey('storyteller.ExpKind', related_name='exp_links')
    character = models.ForeignKey('storyteller.CharacterTemplate', related_name='exp_kinds')

    class Meta:
        unique_together = (("kind", "character"),)

    def __str__(self):
        return str(self.kind)

    def sheet_format(self, rjust=None):
        gained = self.gained()
        spent = self.spent()
        val_string = '%s/%i' % (str(int(gained + spent)).rjust(2), gained)
        if rjust:
            return '%s: %s' % (str(self).rjust(rjust), val_string)
        else:
            return '%s: %s' % (self, val_string)

    @property
    def list_order(self):
        return self.kind.list_order

    def spent(self):
        spent = self.entries.filter(amount__lt=0).aggregate(spent=Sum('amount'))
        num = spent['spent']
        if num is None:
            return Decimal(0.0)
        return num

    def gained(self):
        gained = self.entries.filter(amount__gt=0).aggregate(gained=Sum('amount'))
        num = gained['gained']
        if num is None:
            return Decimal(0.0)
        return num

    def available(self):
        available = self.entries.aggregate(available=Sum('amount'))
        num = available['available']
        if num is None:
            return Decimal(0.0)
        return num

class Exp(models.Model):
    link = models.ForeignKey('storyteller.ExpLink', related_name='entries')
    amount = models.DecimalField(default=0.0, db_index=True)
    reason = models.CharField(max_length=200)
    source = models.ForeignKey('objects.ObjectDB', null=True)
    date_awarded = models.DateTimeField()

    def __int__(self):
        return int(self.amount)

    def __str__(self):
        return self.reason
"""