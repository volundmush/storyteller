from django.db import models


class TemplateInfo(models.Model):
    character = models.OneToOneField(
        "objects.ObjectDB",
        on_delete=models.CASCADE,
        related_name="stdb_template",
        primary_key=True,
    )
    template = models.CharField(
        max_length=30, blank=False, null=False, default="Mortal"
    )

    def __str__(self):
        return self.template

    def __repr__(self):
        return f"<{self.character}'s Template: {self.template}>"


class TemplateField(models.Model):
    character = models.ForeignKey(
        "objects.ObjectDB", on_delete=models.CASCADE, related_name="stdb_fields"
    )
    field = models.CharField(max_length=30, blank=False, null=False)
    value = models.CharField(max_length=30, blank=False, null=False)

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"<{self.character}'s {self.field} Field: {self.value} ({self.id})>"

    class Meta:
        unique_together = (("character", "field"),)


class HasValueData(models.Model):
    value = models.IntegerField(blank=False, null=False, default=0)
    data = models.JSONField(blank=False, null=True, default=dict)

    class Meta:
        abstract = True


class Stat(models.Model):
    category = models.CharField(max_length=30, blank=False, null=False)
    name = models.CharField(max_length=30, blank=False, null=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<{self.category}: {self.name} ({self.id})>"

    class Meta:
        unique_together = (("category", "name"),)


class StatRank(HasValueData, models.Model):
    character = models.ForeignKey(
        "objects.ObjectDB", on_delete=models.CASCADE, related_name="stdb_stats"
    )
    stat = models.ForeignKey(Stat, on_delete=models.CASCADE, related_name="ranks")
    context = models.CharField(max_length=100, blank=True, null=False, default="")

    def __str__(self):
        if self.context:
            return f"{self.context}"
        return str(self.stat)

    def __repr__(self):
        return f"<{self.character}'s {self.stat.category}: {self.stat} ({self.value}) ({self.id})>"

    class Meta:
        unique_together = (("character", "stat", "context"),)


class Power(models.Model):
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


class PowerRank(HasValueData, models.Model):
    character = models.ForeignKey(
        "objects.ObjectDB", on_delete=models.CASCADE, related_name="stdb_powers"
    )
    power = models.ForeignKey(Power, on_delete=models.CASCADE, related_name="ranks")

    def __str__(self):
        return str(self.power)

    def __repr__(self):
        return f"<{self.character}'s {self.power.category} {self.power.subcategory}: {self.power} ({self.value}) ({self.id})>"

    class Meta:
        unique_together = (("character", "power"),)


class StatPower(models.Model):
    stat = models.ForeignKey(Stat, on_delete=models.CASCADE, related_name="powers")
    name = models.CharField(max_length=80, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (("stat", "name"),)


class StatPowerRank(HasValueData, models.Model):
    character = models.ForeignKey(
        "objects.ObjectDB", on_delete=models.CASCADE, related_name="stdb_stat_charms"
    )
    power = models.ForeignKey(StatPower, on_delete=models.CASCADE, related_name="ranks")

    def __str__(self):
        return str(self.power)

    class Meta:
        unique_together = (("character", "power"),)


class CustomPower(HasValueData, models.Model):
    stat = models.ForeignKey(StatRank, on_delete=models.CASCADE, related_name="customs")
    name = models.CharField(max_length=80, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (("stat", "name"),)
