# Generated by Django 3.2.6 on 2021-09-08 11:35

import bothub.common.languages
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authentication', '0009_auto_20210506_1453'),
        ('common', '0110_auto_20210601_1443'),
    ]

    operations = [
        migrations.CreateModel(
            name='QALogs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField(help_text='Question')),
                ('confidence', models.FloatField(help_text='Confidence')),
                ('question', models.TextField(help_text='Question')),
                ('user_agent', models.TextField(help_text='User Agent')),
                ('from_backend', models.BooleanField()),
                ('language', models.CharField(max_length=5, validators=[bothub.common.languages.validate_language], verbose_name='language')),
                ('nlp_log', models.TextField(blank=True, help_text='NLP Log')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
            ],
            options={
                'verbose_name': 'repository qa nlp logs',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='QAtext',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='QA context text', max_length=25000, verbose_name='text')),
                ('language', models.CharField(help_text='Knowledge Base language', max_length=5, validators=[bothub.common.languages.validate_language], verbose_name='language')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='last update')),
            ],
        ),
        migrations.AddField(
            model_name='qaknowledgebase',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='knowledge_bases', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='QAContext',
        ),
        migrations.AddField(
            model_name='qatext',
            name='knowledge_base',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='texts', to='common.qaknowledgebase'),
        ),
        migrations.AddField(
            model_name='qalogs',
            name='knowledge_base',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='qa_nlp_logs', to='common.qaknowledgebase'),
        ),
        migrations.AddField(
            model_name='qalogs',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.repositoryowner'),
        ),
        migrations.AlterUniqueTogether(
            name='qatext',
            unique_together={('knowledge_base', 'language')},
        ),
        migrations.AddIndex(
            model_name='qalogs',
            index=models.Index(condition=models.Q(('from_backend', False)), fields=['knowledge_base', 'user'], name='common_repo_qa_nlp_log_idx'),
        ),
    ]
