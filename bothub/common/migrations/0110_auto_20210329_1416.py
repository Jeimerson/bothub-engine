# Generated by Django 2.2.19 on 2021-03-29 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("common", "0109_auto_20210329_1407")]

    operations = [
        migrations.AlterField(
            model_name="repository",
            name="repository_type",
            field=models.CharField(
                choices=[("classifier", "Classifier"), ("content", "Content")],
                default="classifier",
                max_length=10,
                verbose_name="repository type",
            ),
        )
    ]
