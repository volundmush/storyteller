from django.db import models


class Charm(models.Model):
    category = models.CharField(max_length=30, blank=False, null=False)
    subcategory = models.CharField(max_length=30, blank=False, null=False)
    name = models.CharField(max_length=80, blank=False, null=False)

    class Meta:
        unique_together = (("category", "subcategory", "name"),)


class CharmRank(models.Model):
    character = models.ForeignKey("objects.ObjectDB", on_delete=models.CASCADE, related_name="stdb_charms")
    charm = models.ForeignKey(Charm, on_delete=models.CASCADE, related_name="ranks")
    value = models.IntegerField(blank=False, null=False, default=0)
    data = models.JSONField(blank=True, null=True)

    class Meta:
        unique_together = (("character", "charm"),)


class StatCharm(models.Model):
    stat = models.ForeignKey("storybase.Stat", on_delete=models.CASCADE, related_name="charms")
    name = models.CharField(max_length=80, blank=False, null=False)

    class Meta:
        unique_together = (("stat", "name"),)


class StatCharmRank(models.Model):
    character = models.ForeignKey("objects.ObjectDB", on_delete=models.CASCADE, related_name="stdb_stat_charms")
    charm = models.ForeignKey(StatCharm, on_delete=models.CASCADE, related_name="ranks")
    value = models.IntegerField(blank=False, null=False, default=0)
    data = models.JSONField(blank=True, null=True)

    class Meta:
        unique_together = (("character", "charm"),)


class Merit(models.Model):
    category = models.CharField(max_length=30, blank=False, null=False)
    name = models.CharField(max_length=80, blank=False, null=False)

    class Meta:
        unique_together = (("category", "name"),)


class MeritRank(models.Model):
    character = models.ForeignKey("objects.ObjectDB", on_delete=models.CASCADE, related_name="stdb_merits")
    merit = models.ForeignKey(Merit, on_delete=models.CASCADE, related_name="ranks")
    value = models.IntegerField(blank=False, null=False, default=0)
    data = models.JSONField(blank=True, null=True)

    class Meta:
        unique_together = (("character", "merit"),)


class Evocation(models.Model):
    merit = models.ForeignKey(MeritRank, on_delete=models.CASCADE, related_name="evocations")
    name = models.CharField(max_length=80, blank=False, null=False)
    value = models.IntegerField(blank=False, null=False, default=0)
    data = models.JSONField(blank=True, null=True)

    class Meta:
        unique_together = (("merit", "name"),)
