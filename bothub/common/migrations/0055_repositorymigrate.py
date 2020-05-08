# Generated by Django 2.1.11 on 2020-05-08 14:45

import bothub.common.languages
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("common", "0054_repositoryversion_is_deleted"),
    ]

    operations = [
        migrations.CreateModel(
            name="RepositoryMigrate",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "language",
                    models.CharField(
                        max_length=5,
                        validators=[bothub.common.languages.validate_language],
                        verbose_name="language",
                    ),
                ),
                ("auth_token", models.TextField()),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "repository",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="migrate",
                        to="common.Repository",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="repository_migrate",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "repository migrate",
                "verbose_name_plural": "repository migrates",
            },
        )
    ]
