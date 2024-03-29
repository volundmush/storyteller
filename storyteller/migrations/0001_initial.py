# Generated by Django 4.1.11 on 2023-11-26 02:58

import athanor.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("objects", "0013_defaultobject_alter_objectdb_id_defaultcharacter_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Experience",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=30)),
                ("description", models.TextField(blank=True, default="")),
            ],
        ),
        migrations.CreateModel(
            name="Pool",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=30)),
                ("spent", models.IntegerField(default=0)),
                ("bonus", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="Power",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("data", models.JSONField(default=dict, null=True)),
                ("family", models.CharField(max_length=12)),
                ("category", models.CharField(max_length=30)),
                ("subcategory", models.CharField(max_length=30)),
                ("name", models.CharField(max_length=80)),
            ],
            options={
                "unique_together": {("family", "category", "subcategory", "name")},
            },
        ),
        migrations.CreateModel(
            name="SheetInfo",
            fields=[
                (
                    "character",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="sheet",
                        serialize=False,
                        to="objects.objectdb",
                    ),
                ),
                ("game", models.CharField(max_length=30)),
                ("template", models.CharField(default="Mortal", max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name="Stat",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("data", models.JSONField(default=dict, null=True)),
                ("category", models.CharField(max_length=30)),
                ("name", models.CharField(max_length=30)),
            ],
            options={
                "unique_together": {("category", "name")},
            },
        ),
        migrations.CreateModel(
            name="StatPower",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=80)),
                (
                    "stat",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="powers",
                        to="storyteller.stat",
                    ),
                ),
            ],
            options={
                "unique_together": {("stat", "name")},
            },
        ),
        migrations.CreateModel(
            name="StatRank",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("data", models.JSONField(default=dict, null=True)),
                ("value", models.IntegerField(default=0)),
                ("modules", models.JSONField(default=dict, null=True)),
                ("tags", models.JSONField(default=list, null=True)),
                ("tier", models.SmallIntegerField(default=0)),
                ("context", models.CharField(blank=True, default="", max_length=100)),
                ("description", models.TextField(blank=True, default="")),
                (
                    "sheet",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="stats",
                        to="storyteller.sheetinfo",
                    ),
                ),
                (
                    "stat",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ranks",
                        to="storyteller.stat",
                    ),
                ),
            ],
            options={
                "unique_together": {("sheet", "stat", "context")},
            },
        ),
        migrations.CreateModel(
            name="PoolCommit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("value", models.IntegerField(default=0)),
                ("description", models.TextField(blank=True, default="")),
                (
                    "pool",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="commits",
                        to="storyteller.pool",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="pool",
            name="sheet",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="pools",
                to="storyteller.sheetinfo",
            ),
        ),
        migrations.CreateModel(
            name="ExperienceTransaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount", models.IntegerField(default=0)),
                ("date_created", models.DateTimeField(default=athanor.utils.utcnow)),
                ("explanation", models.TextField(blank=True, default="")),
                (
                    "exp",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transactions",
                        to="storyteller.experience",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="experience",
            name="sheet",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="xp",
                to="storyteller.sheetinfo",
            ),
        ),
        migrations.CreateModel(
            name="TemplateField",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("field", models.CharField(max_length=30)),
                ("value", models.CharField(max_length=30)),
                (
                    "sheet",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="fields",
                        to="storyteller.sheetinfo",
                    ),
                ),
            ],
            options={
                "unique_together": {("sheet", "field")},
            },
        ),
        migrations.CreateModel(
            name="StatPowerRank",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("data", models.JSONField(default=dict, null=True)),
                ("value", models.IntegerField(default=0)),
                ("modules", models.JSONField(default=dict, null=True)),
                ("tags", models.JSONField(default=list, null=True)),
                ("tier", models.SmallIntegerField(default=0)),
                (
                    "power",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ranks",
                        to="storyteller.statpower",
                    ),
                ),
                (
                    "sheet",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="stat_powers",
                        to="storyteller.sheetinfo",
                    ),
                ),
            ],
            options={
                "unique_together": {("sheet", "power")},
            },
        ),
        migrations.CreateModel(
            name="PowerRank",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("data", models.JSONField(default=dict, null=True)),
                ("value", models.IntegerField(default=0)),
                ("modules", models.JSONField(default=dict, null=True)),
                ("tags", models.JSONField(default=list, null=True)),
                ("tier", models.SmallIntegerField(default=0)),
                (
                    "power",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ranks",
                        to="storyteller.power",
                    ),
                ),
                (
                    "sheet",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="powers",
                        to="storyteller.sheetinfo",
                    ),
                ),
            ],
            options={
                "unique_together": {("sheet", "power")},
            },
        ),
        migrations.AlterUniqueTogether(
            name="pool",
            unique_together={("sheet", "name")},
        ),
        migrations.AlterUniqueTogether(
            name="experience",
            unique_together={("sheet", "name")},
        ),
        migrations.CreateModel(
            name="CustomPower",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("data", models.JSONField(default=dict, null=True)),
                ("value", models.IntegerField(default=0)),
                ("modules", models.JSONField(default=dict, null=True)),
                ("tags", models.JSONField(default=list, null=True)),
                ("tier", models.SmallIntegerField(default=0)),
                ("name", models.CharField(max_length=80)),
                (
                    "stat",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="customs",
                        to="storyteller.statrank",
                    ),
                ),
            ],
            options={
                "unique_together": {("stat", "name")},
            },
        ),
        migrations.CreateModel(
            name="CreateEntry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateTimeField(auto_now_add=True)),
                ("object_id", models.PositiveIntegerField()),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="story_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-date"],
                "unique_together": {("content_type", "object_id")},
            },
        ),
    ]
