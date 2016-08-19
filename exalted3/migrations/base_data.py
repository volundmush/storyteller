from django.db import migrations, models
from storyteller.exalted3.rules import STAT_TAGS, STAT_PARENTS, STAT_DATA


def install_base_data(apps, schema_editor):
    StatTag = apps.get_model('exalted3', 'StatTag')
    tag_cache = dict()
    for tag in STAT_TAGS:
        new_tag, created = StatTag.objects.get_or_create(id=tag['id'], key=tag['key'])
        tag_cache[tag['id']] = new_tag

    Stat = apps.get_model('exalted3', 'Stat')
    stat_cache = dict()
    stat_cache[None] = None
    for stat in STAT_PARENTS:
        new_stat, created = Stat.objects.get_or_create(id=stat['id'], key=stat['key'],
                                                       list_order=stat['list_order'],
                                                       start_rating=stat['start_rating'])
        stat_cache[stat['id']] = new_stat
        for num in stat['features_add']:
            new_stat.features.add(tag_cache[num])

    Trait = apps.get_model('exalted3', 'Trait')

    for stat in STAT_DATA:
        new_stat, created = Stat.objects.get_or_create(id=stat['id'], key=stat['key'],
                                                       parent=stat_cache[stat['parent']],
                                                       kind=stat_cache[stat.get('kind', None)],
                                                       start_rating=stat['start_rating'],
                                                       list_order=stat['list_order'])
        stat_cache[stat['id']] = new_stat
        for num in stat['features_add']:
            new_stat.features.add(tag_cache[num])


class Migration(migrations.Migration):

    dependencies = [
        ('exalted3', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(install_base_data)
    ]