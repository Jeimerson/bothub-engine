# Generated by Django 3.2.8 on 2022-03-03 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0010_alter_repositoryowner_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='language',
            field=models.CharField(blank=True, choices=[('en-us', 'English'), ('pt-br', 'Brazilian Portuguese'), ('es', 'Spanish')], max_length=5, null=True),
        ),
    ]
