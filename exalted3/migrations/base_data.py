from django.db import migrations, models
from storyteller.exalted3.rules import STAT_TAGS, STAT_DATA


def install_base_data(apps, schema_editor):
    StatTag = apps.get_model('exalted3', 'StatTag')
    tag_cache = dict()
    for tag in STAT_TAGS:
        new_tag, created = StatTag.objects.get_or_create(id=tag['id'], key=tag['key'])
        tag_cache[tag['id']] = new_tag

    Stat = apps.get_model('exalted3', 'Stat')
    stat_cache = dict()
    stat_cache[None] = None
    feature_cache = dict()
    for stat in STAT_DATA:
        new_stat, created = Stat.objects.get_or_create(id=stat['id'], key=stat['key'],
                                                       parent=stat_cache[stat.get('parent',None)],
                                                       kind=stat_cache[stat.get('kind', None)],
                                                       start_rating=stat.get('start_rating', 0),
                                                       list_order=stat.get('list_order', 0))
        stat_cache[stat['id']] = new_stat
        for num in stat.get('features_add', tuple()):
            new_stat.features.add(tag_cache[num])
        if not stat.get('parent', None):
            feature_cache[stat['id']] = new_stat.features.all()
        else:
            for feature in feature_cache[stat['parent']]:
                new_stat.features.add(feature)

        for num in stat.get('features_remove', tuple()):
            new_stat.features.remove(tag_cache[num])

    Trait = apps.get_model('exalted3', 'Trait')


class Migration(migrations.Migration):

    dependencies = [
        ('exalted3', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(install_base_data)
    ]