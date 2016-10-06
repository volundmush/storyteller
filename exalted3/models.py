from __future__ import unicode_literals
from django.db import models
from athanor.core.models import WithKey


class Persona(models.Model):
    key = models.CharField(max_length=255, db_index=True)
    parent = models.ForeignKey('exalted3.Persona', null=True, default=None, related_name='children')
    character = models.ForeignKey('objects.ObjectDB', related_name='ex3_personas')
    template = models.PositiveSmallIntegerField(default=1)
    caste = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = (('key', 'character'),)

    def __repr__(self):
        return '<Persona: %s>' % self.key

    def __str__(self):
        return self.key


class Trait(models.Model):
    persona = models.ForeignKey('exalted3.Persona', related_name='traits')
    trait_id = models.PositiveIntegerField(default=0)
    answer = models.ForeignKey('exalted3.TraitAnswer', related_name='trait_characters')

    class Meta:
        unique_together = (('trait_id', 'persona'),)


class TraitAnswer(WithKey):
    pass


class Stat(models.Model):
    persona = models.OneToOneField('exalted3.Persona', related_name='stats')

    #Advantages
    essence = models.PositiveSmallIntegerField(default=None, null=True)
    willpower = models.PositiveSmallIntegerField(default=None, null=True)

    #Attributes
    strength = models.PositiveSmallIntegerField(default=None, null=True)
    dexterity = models.PositiveSmallIntegerField(default=None, null=True)
    stamina = models.PositiveSmallIntegerField(default=None, null=True)
    charisma = models.PositiveSmallIntegerField(default=None, null=True)
    manipulation = models.PositiveSmallIntegerField(default=None, null=True)
    appearance = models.PositiveSmallIntegerField(default=None, null=True)
    perception = models.PositiveSmallIntegerField(default=None, null=True)
    intelligence = models.PositiveSmallIntegerField(default=None, null=True)
    wits = models.PositiveSmallIntegerField(default=None, null=True)

    # Attributes - Favored
    strength_favored = models.BooleanField(default=False)
    dexterity_favored = models.BooleanField(default=False)
    stamina_favored = models.BooleanField(default=False)
    charisma_favored = models.BooleanField(default=False)
    manipulation_favored = models.BooleanField(default=False)
    appearance_favored = models.BooleanField(default=False)
    perception_favored = models.BooleanField(default=False)
    intelligence_favored = models.BooleanField(default=False)
    wits_favored = models.BooleanField(default=False)

    # Attributes - Supernal
    strength_supernal = models.BooleanField(default=False)
    dexterity_supernal = models.BooleanField(default=False)
    stamina_supernal = models.BooleanField(default=False)
    charisma_supernal = models.BooleanField(default=False)
    manipulation_supernal = models.BooleanField(default=False)
    appearance_supernal = models.BooleanField(default=False)
    perception_supernal = models.BooleanField(default=False)
    intelligence_supernal = models.BooleanField(default=False)
    wits_supernal = models.BooleanField(default=False)

    #Abilities
    archery = models.PositiveSmallIntegerField(default=None, null=True)
    brawl = models.PositiveSmallIntegerField(default=None, null=True)
    melee = models.PositiveSmallIntegerField(default=None, null=True)
    war = models.PositiveSmallIntegerField(default=None, null=True)
    thrown = models.PositiveSmallIntegerField(default=None, null=True)
    bureaucracy = models.PositiveSmallIntegerField(default=None, null=True)
    linguistics = models.PositiveSmallIntegerField(default=None, null=True)
    ride = models.PositiveSmallIntegerField(default=None, null=True)
    sail = models.PositiveSmallIntegerField(default=None, null=True)
    socialize = models.PositiveSmallIntegerField(default=None, null=True)
    athletics = models.PositiveSmallIntegerField(default=None, null=True)
    awareness = models.PositiveSmallIntegerField(default=None, null=True)
    dodge = models.PositiveSmallIntegerField(default=None, null=True)
    larceny = models.PositiveSmallIntegerField(default=None, null=True)
    stealth = models.PositiveSmallIntegerField(default=None, null=True)
    craft = models.PositiveSmallIntegerField(default=None, null=True)
    investigation = models.PositiveSmallIntegerField(default=None, null=True)
    lore = models.PositiveSmallIntegerField(default=None, null=True)
    medicine = models.PositiveSmallIntegerField(default=None, null=True)
    occult = models.PositiveSmallIntegerField(default=None, null=True)
    integrity = models.PositiveSmallIntegerField(default=None, null=True)
    performance = models.PositiveSmallIntegerField(default=None, null=True)
    presence = models.PositiveSmallIntegerField(default=None, null=True)
    resistance = models.PositiveSmallIntegerField(default=None, null=True)
    survival = models.PositiveSmallIntegerField(default=None, null=True)
    martialarts = models.PositiveSmallIntegerField(default=None, null=True)

    # Abilities - Favored
    archery_favored = models.BooleanField(default=False)
    brawl_favored = models.BooleanField(default=False)
    melee_favored = models.BooleanField(default=False)
    war_favored = models.BooleanField(default=False)
    thrown_favored = models.BooleanField(default=False)
    bureaucracy_favored = models.BooleanField(default=False)
    linguistics_favored = models.BooleanField(default=False)
    ride_favored = models.BooleanField(default=False)
    sail_favored = models.BooleanField(default=False)
    socialize_favored = models.BooleanField(default=False)
    athletics_favored = models.BooleanField(default=False)
    awareness_favored = models.BooleanField(default=False)
    dodge_favored = models.BooleanField(default=False)
    larceny_favored = models.BooleanField(default=False)
    stealth_favored = models.BooleanField(default=False)
    craft_favored = models.BooleanField(default=False)
    investigation_favored = models.BooleanField(default=False)
    lore_favored = models.BooleanField(default=False)
    medicine_favored = models.BooleanField(default=False)
    occult_favored = models.BooleanField(default=False)
    integrity_favored = models.BooleanField(default=False)
    performance_favored = models.BooleanField(default=False)
    presence_favored = models.BooleanField(default=False)
    resistance_favored = models.BooleanField(default=False)
    survival_favored = models.BooleanField(default=False)
    martialarts_favored = models.BooleanField(default=False)

    # Abilities - Supernal
    archery_supernal = models.BooleanField(default=False)
    brawl_supernal = models.BooleanField(default=False)
    melee_supernal = models.BooleanField(default=False)
    war_supernal = models.BooleanField(default=False)
    thrown_supernal = models.BooleanField(default=False)
    bureaucracy_supernal = models.BooleanField(default=False)
    linguistics_supernal = models.BooleanField(default=False)
    ride_supernal = models.BooleanField(default=False)
    sail_supernal = models.BooleanField(default=False)
    socialize_supernal = models.BooleanField(default=False)
    athletics_supernal = models.BooleanField(default=False)
    awareness_supernal = models.BooleanField(default=False)
    dodge_supernal = models.BooleanField(default=False)
    larceny_supernal = models.BooleanField(default=False)
    stealth_supernal = models.BooleanField(default=False)
    craft_supernal = models.BooleanField(default=False)
    investigation_supernal = models.BooleanField(default=False)
    lore_supernal = models.BooleanField(default=False)
    medicine_supernal = models.BooleanField(default=False)
    occult_supernal = models.BooleanField(default=False)
    integrity_supernal = models.BooleanField(default=False)
    performance_supernal = models.BooleanField(default=False)
    presence_supernal = models.BooleanField(default=False)
    resistance_supernal = models.BooleanField(default=False)
    survival_supernal = models.BooleanField(default=False)
    martialarts_supernal = models.BooleanField(default=False)

    #Styles
    snake = models.PositiveSmallIntegerField(default=None, null=True)
    tiger = models.PositiveSmallIntegerField(default=None, null=True)
    singlepoint = models.PositiveSmallIntegerField(default=None, null=True)
    silvervoice = models.PositiveSmallIntegerField(default=None, null=True)
    whitereaper = models.PositiveSmallIntegerField(default=None, null=True)
    ebonshadow = models.PositiveSmallIntegerField(default=None, null=True)
    crane = models.PositiveSmallIntegerField(default=None, null=True)
    righteousdevil = models.PositiveSmallIntegerField(default=None, null=True)
    blackclaw = models.PositiveSmallIntegerField(default=None, null=True)
    steeldevil = models.PositiveSmallIntegerField(default=None, null=True)



class SpecialtyName(models.Model):
    stat_id = models.PositiveIntegerField(default=0)
    key = models.CharField(max_length=255, db_index=True)

    class Meta:
        unique_together = (('stat_id', 'key'),)


class Specialty(models.Model):
    persona = models.ForeignKey('exalted3.Persona', related_name='specialties')
    specialty = models.ForeignKey('exalted3.SpecialtyName', related_name='users')
    value = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = (('specialty', 'persona'),)


class CustomStat(models.Model):
    key = models.CharField(max_length=255, db_index=True)
    category = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = (('key', 'category'),)


class Custom(models.Model):
    persona = models.ForeignKey('exalted3.Persona', related_name='custom_stats')
    stat = models.ForeignKey('exalted3.CustomStat', related_name='users')
    value = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = (('persona', 'stat'),)


class CustomSpecialty(models.Model):
    stat = models.ForeignKey('exalted3.Custom', related_name='specialties')
    key = models.CharField(max_length=255, db_index=True)
    value = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = (('stat', 'key'),)


class Merit(models.Model):
    persona = models.ForeignKey('exalted3.Persona', related_name='merits')
    merit_id = models.PositiveIntegerField(default=0)
    context = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = (('persona', 'merit_id', 'context'),)


class Pool(models.Model):
    persona = models.ForeignKey('Persona', related_name='pools')
    pool_id = models.PositiveSmallIntegerField(default=0)
    spent = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = (('persona', 'pool_id'),)


class PoolCommit(models.Model):
    pool = models.ForeignKey('exalted3.Pool', related_name='commits')
    key = models.CharField(max_length=255, db_index=True)
    value = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = (('pool', 'key'),)


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