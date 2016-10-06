from django.db import models
from evennia.utils.ansi import ANSIString
from athanor.library import dramatic_capitalize, sanitize_string
from athanor.core.models import validate_color
from django.utils.encoding import smart_text

def prepare_key(value):
    return dramatic_capitalize(sanitize_string(value, strip_ansi=True, strip_indents=True,
                                               strip_newlines=True))

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


class AbstractCharacter(models.Model):
    game = models.PositiveSmallIntegerField(default=0)
    key = models.CharField(max_length=255, db_index=True)
    character = models.ForeignKey('objects.ObjectDB', related_name='personas')
    template = models.PositiveSmallIntegerField(default=0)

    class Meta:
        abstract = True
        unique_together = (('game', 'key', 'character'),)

    def __repr__(self):
        return '<Persona: %s>' % self.key

    def __str__(self):
        return self.key





class AbstractStat(models.Model):
    key = models.CharField(max_length=255, db_index=True)
    start_rating = models.PositiveSmallIntegerField(default=0, db_index=True, null=True)
    #features = models.ManyToManyField('AbstractStatTag', related_name='stats')
    parent = models.ForeignKey('self', related_name='children', null=True)
    kind = models.ForeignKey('self', related_name='kind_children', null=True)
    list_order = models.PositiveIntegerField(default=0, db_index=True)
    custom = models.BooleanField(default=False)

    class Meta:
        abstract = True
        unique_together = (('key', 'parent'),)

    def __repr__(self):
        return '<Stat: %s>' % self.key

class AbstractStatTag(models.Model):
    key = models.CharField(max_length=255, db_index=True, unique=True)

    class Meta:
        abstract = True


class AbstractPersonaStat(WithDotValue):
    #persona = models.ForeignKey('AbstractPersona', related_name='stats')
    #stat = models.ForeignKey('AbstractStat', related_name='persona_stats')
    #tags = models.ManyToManyField('AbstractStatTag', related_name='persona_stats')

    class Meta:
        abstract = True
        #unique_together = (('persona', 'stat'),)


class AbstractMerit(models.Model):
    key = models.CharField(max_length=255, db_index=True)
    parent = models.ForeignKey('self', related_name='children', null=True)
    kind = models.ForeignKey('self', related_name='kind_children', null=True)
    list_order = models.PositiveIntegerField(default=0, db_index=True)
    custom = models.BooleanField(default=False)

    class Meta:
        abstract = True
        unique_together = (('key', 'parent'))

    def __repr__(self):
        return '<Merit: %s>' % self.key

class AbstractPersonaMerit(WithDotValue):
    #merit = models.ForeignKey('AbstractMerit', related_name='persona_merits')
    #persona = models.ForeignKey('AbstractPersona', related_name='merits')
    key = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    #unique_together = (('persona', 'key'))

class AbstractPool(models.Model):
    key = models.CharField(max_length=255, db_index=True, unique=True)

    class Meta:
        abstract = True


class AbstractPersonaPool(models.Model):
    #persona = models.ForeignKey('AbstractPersona', related_name='pools')
    #pool = models.ForeignKey('AbstractPool', related_name='persona_pools')
    points = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True

class AbstractPersonaCommit(models.Model):
    key = models.CharField(max_length=255, db_index=True)
    #pool = models.ForeignKey('AbstractPersonaPool', related_name='commitments')
    value = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.key

    class Meta:
        abstract = True