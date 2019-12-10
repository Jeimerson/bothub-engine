# Generated by Django 2.1.11 on 2019-12-09 19:33

import bothub.common.languages
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("common", "0040_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="RepositoryVersion",
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
                ("name", models.CharField(max_length=40)),
                (
                    "last_update",
                    models.DateTimeField(auto_now_add=True, verbose_name="last update"),
                ),
                ("is_default", models.BooleanField(default=True)),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"verbose_name": "repository version"},
        ),
        migrations.CreateModel(
            name="RepositoryVersionLanguage",
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
                ("bot_data", models.TextField(blank=True, verbose_name="bot data")),
                (
                    "training_started_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="training started at"
                    ),
                ),
                (
                    "training_end_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="trained at"
                    ),
                ),
                (
                    "failed_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="failed at"
                    ),
                ),
                ("use_analyze_char", models.BooleanField(default=False)),
                ("use_name_entities", models.BooleanField(default=False)),
                ("use_competing_intents", models.BooleanField(default=False)),
                (
                    "algorithm",
                    models.CharField(
                        choices=[
                            ("statistical_model", "Statistical Model"),
                            (
                                "neural_network_internal",
                                "Neural Network with internal vocabulary",
                            ),
                            (
                                "neural_network_external",
                                "Neural Network with external vocabulary (BETA)",
                            ),
                        ],
                        default="statistical_model",
                        max_length=24,
                        verbose_name="algorithm",
                    ),
                ),
                (
                    "training_log",
                    models.TextField(
                        blank=True, editable=False, verbose_name="training log"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "last_update",
                    models.DateTimeField(auto_now_add=True, verbose_name="last update"),
                ),
                (
                    "total_training_end",
                    models.IntegerField(default=0, verbose_name="total training end"),
                ),
                (
                    "repository_version",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="common.RepositoryVersion",
                    ),
                ),
            ],
            options={
                "verbose_name": "repository version language",
                "verbose_name_plural": "repository version languages",
                "ordering": ["-created_at"],
            },
        ),
        migrations.RemoveField(model_name="repositoryupdate", name="by"),
        migrations.RemoveField(model_name="repositoryupdate", name="repository"),
        migrations.RemoveField(model_name="repository", name="total_updates"),
        migrations.RemoveField(
            model_name="repositoryevaluate", name="repository_update"
        ),
        migrations.RemoveField(
            model_name="repositoryevaluateresult", name="repository_update"
        ),
        migrations.RemoveField(
            model_name="repositoryexample", name="repository_update"
        ),
        migrations.RemoveField(
            model_name="repositorytranslatedexample", name="repository_update"
        ),
        migrations.AddField(
            model_name="repositoryexample",
            name="last_update",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="last update"
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="repositoryevaluate",
            name="deleted_in",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="deleted_evaluate",
                to="common.RepositoryVersionLanguage",
            ),
        ),
        migrations.AlterField(
            model_name="repositoryexample",
            name="deleted_in",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="deleted",
                to="common.RepositoryVersionLanguage",
            ),
        ),
        migrations.DeleteModel(name="RepositoryUpdate"),
        migrations.AddField(
            model_name="repositoryversion",
            name="repository",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="versions",
                to="common.Repository",
            ),
        ),
        migrations.AddField(
            model_name="repositoryevaluate",
            name="repository_version_language",
            field=models.ForeignKey(
                default=None,
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="added_evaluate",
                to="common.RepositoryVersionLanguage",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="repositoryevaluateresult",
            name="repository_version_language",
            field=models.ForeignKey(
                default=None,
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="results",
                to="common.RepositoryVersionLanguage",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="repositoryexample",
            name="repository_version_language",
            field=models.ForeignKey(
                default=None,
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="added",
                to="common.RepositoryVersionLanguage",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="repositorytranslatedexample",
            name="repository_version_language",
            field=models.ForeignKey(
                default=None,
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="translated_added",
                to="common.RepositoryVersionLanguage",
            ),
            preserve_default=False,
        ),
    ]
