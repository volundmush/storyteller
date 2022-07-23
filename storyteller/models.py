from django.db import models


class StorytellerStat(models.Model):
    name_1 = models.CharField(max_length=80, null=False, blank=False)
    name_2 = models.CharField(max_length=80, null=False, blank=True, default='')
    name_3 = models.CharField(max_length=80, null=False, blank=True, default='')
    name_4 = models.CharField(max_length=80, null=False, blank=True, default='')
    creator = models.ForeignKey('objects.ObjectDB', null=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = (("name_1", "name_2", "name_3", "name_4"),)


class CharacterStat(models.Model):
    stat = models.ForeignKey(StorytellerStat, on_delete=models.PROTECT, related_name="users")
    owner = models.ForeignKey("objects.ObjectDB", on_delete=models.CASCADE, related_name="story_stats")
    stat_value = models.PositiveIntegerField(default=0, null=False)
    stat_extra = models.JSONField(null=True, default=None)

    class Meta:
        unique_together = (("stat", "owner"),)
