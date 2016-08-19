from django.db import models
from evennia.utils.ansi import ANSIString
from athanor.library import dramatic_capitalize, sanitize_string
from athanor.core.models import validate_color
from django.utils.encoding import smart_text

class CapitalCharField(models.CharField):
    def to_python(self, obj):
        return dramatic_capitalize(sanitize_string(obj, strip_ansi=True))

    def get_prep_value(self, value):
        value = super(CapitalCharField, self).get_prep_value(value)
        return dramatic_capitalize(sanitize_string(value, strip_ansi=True,
                                                   strip_newlines=True, strip_indents=True))

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


class AbstractPersona(models.Model):
    key = CapitalCharField(max_length=255, db_index=True)
    character = models.ForeignKey('objects.ObjectDB', related_name='personas')
    active = models.BooleanField(default=True)
    #template = models.ForeignKey('AbstractTemplate', related_name='personas')
    #category1 = models.ForeignKey('AbstractCategory', related_name='personas_1', null=True)
    #category2 = models.ForeignKey('AbstractCategory', related_name='personas_2', null=True)
    #category3 = models.ForeignKey('AbstractCategory', related_name='personas_3', null=True)

    class Meta:
        abstract = True
        unique_together = (('key', 'character'),)

    def __repr__(self):
        return '<Persona: %s>' % self.key

class AbstractTemplate(models.Model):
    key = CapitalCharField(max_length=255, db_index=True, unique=True)
    default_template = models.BooleanField(default=False)
    category1_name = models.CharField(max_length=255, default='Category1')
    category2_name = models.CharField(max_length=255, default='Category2')
    category3_name = models.CharField(max_length=255, default='Category3')

    def __repr__(self):
        return '<Template: %s>' % self.key

    class Meta:
        abstract = True

    def add_trait(self, name):
        old = self.trait_choices.filter(key__iexact=name).first()
        if old:
            old.rename(name)
        else:
            return self.trait_choices.create(key=name)

    def find_trait(self, name):
        trait = self.trait_choices.filter(key__iexact=name).first()
        if not trait:
            raise ValueError("Trait not found.")
        return trait

    def del_trait(self, name):
        old = self.find_trait(name)
        old.delete()

    def set_color(self, name, value):
        self.sheet_colors.get_or_create(key=name, value=value)


class AbstractCategory(models.Model):
    key = CapitalCharField(max_length=255, db_index=True)
    #template = models.ForeignKey('AbstractTemplate', related_name='categories')
    category = models.PositiveSmallIntegerField(default=1)

    class Meta:
        abstract = True

    def __repr__(self):
        return '<Category: %s>' % self.key

class AbstractSheetColor(models.Model):
    key = CapitalCharField(max_length=255, db_index=True)
    #template = models.OneToOneField('AbstractTemplate', related_name='sheet_colors')
    title = models.CharField(max_length=20, default='n', validators=[validate_color])
    border = models.CharField(max_length=20, default='n', validators=[validate_color])
    textfield = models.CharField(max_length=20, default='n', validators=[validate_color])
    texthead = models.CharField(max_length=20, default='n', validators=[validate_color])
    colon = models.CharField(max_length=20, default='n', validators=[validate_color])
    section_name = models.CharField(max_length=20, default='n', validators=[validate_color])
    triple_column_name = models.CharField(max_length=20, default='n', validators=[validate_color])
    advantage_name = models.CharField(max_length=20, default='n', validators=[validate_color])
    advantage_border = models.CharField(max_length=20, default='n', validators=[validate_color])
    slash = models.CharField(max_length=20, default='n', validators=[validate_color])
    statdot = models.CharField(max_length=20, default='n', validators=[validate_color])
    statfill = models.CharField(max_length=20, default='n', validators=[validate_color])
    statname = models.CharField(max_length=20, default='n', validators=[validate_color])
    damagename = models.CharField(max_length=20, default='n', validators=[validate_color])
    damagetotal = models.CharField(max_length=20, default='n', validators=[validate_color])
    damagetotalnum = models.CharField(max_length=20, default='n', validators=[validate_color])

    class Meta:
        abstract = True
        #unique_together = (('template', 'key'),)


class AbstractTrait(models.Model):
    key = CapitalCharField(max_length=255, db_index=True)
    #template = models.ForeignKey('AbstractTemplate', related_name='trait_choices')

    def __repr__(self):
        return '<Trait: %s>' % self.key

    class Meta:
        abstract = True
        #unique_together = (('template', 'key'),)

    def add_option(self, name):
        old = self.options.filter(key__iexact=name).first()
        if old:
            old.rename(name)
        else:
            return self.options.create(key=name)

    def del_option(self, name):
        old = self.options.filter(key__iexact=name).first()
        if not old:
            raise ValueError("Trait option not found.")
        old.delete()


class AbstractTraitValue(models.Model):
    #trait = models.ForeignKey('AbstractTrait', related_name='values')
    key = models.CharField(max_length=255, db_index=True)

    class Meta:
        abstract = True
        #unique_together = (('trait', 'key'),)


class AbstractPersonaTraitValue(models.Model):
    #value = models.ForeignKey('AbstractTraitValue', related_name='personas')
    #persona = models.ForeignKey('AbstractPersona', related_name='traits')

    class Meta:
        abstract = True


class AbstractStat(models.Model):
    key = CapitalCharField(max_length=255, db_index=True)
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
    key = CapitalCharField(max_length=255, db_index=True, unique=True)

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
    key = CapitalCharField(max_length=255, db_index=True)
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
    key = CapitalCharField(max_length=255, db_index=True)
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    #unique_together = (('persona', 'key'))

class AbstractPool(models.Model):
    key = CapitalCharField(max_length=255, db_index=True, unique=True)

    class Meta:
        abstract = True


class AbstractPersonaPool(models.Model):
    #persona = models.ForeignKey('AbstractPersona', related_name='pools')
    #pool = models.ForeignKey('AbstractPool', related_name='persona_pools')
    points = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True

class AbstractPersonaCommit(models.Model):
    key = CapitalCharField(max_length=255, db_index=True)
    #pool = models.ForeignKey('AbstractPersonaPool', related_name='commitments')
    value = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.key

    class Meta:
        abstract = True