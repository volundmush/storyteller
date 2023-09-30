from django.db import models


class TemplateInfo(models.Model):
    character = models.OneToOneField("objects.ObjectDB", on_delete=models.CASCADE, related_name="stdb_template",
                                     primary_key=True)
    template = models.CharField(max_length=30, blank=False, null=False, default="Mortal")


class TemplateField(models.Model):
    character = models.ForeignKey("objects.ObjectDB", on_delete=models.CASCADE, related_name="stdb_fields")
    field = models.CharField(max_length=30, blank=False, null=False)
    value = models.CharField(max_length=30, blank=False, null=False)

    class Meta:
        unique_together = (("character", "field"),)


class Stat(models.Model):
    category = models.CharField(max_length=30, blank=False, null=False)
    name = models.CharField(max_length=30, blank=False, null=False)

    class Meta:
        unique_together = (("category", "name"),)


class StatRank(models.Model):
    character = models.ForeignKey("objects.ObjectDB", on_delete=models.CASCADE, related_name="stdb_stats")
    stat = models.ForeignKey(Stat, on_delete=models.CASCADE, related_name="ranks")
    value = models.IntegerField(blank=False, null=False, default=0)
    data = models.JSONField(blank=True, null=True)

    class Meta:
        unique_together = (("character", "stat"),)


class Specialty(models.Model):
    character = models.ForeignKey("objects.ObjectDB", on_delete=models.CASCADE, related_name="stdb_specialties")
    stat = models.ForeignKey(Stat, on_delete=models.CASCADE, related_name="specialties")
    name = models.CharField(max_length=30, blank=False, null=False)
    value = models.IntegerField(blank=False, null=False, default=0)

    class Meta:
        unique_together = (("character", "stat", "name"),)
