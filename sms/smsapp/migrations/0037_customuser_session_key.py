# Generated by Django 5.0.6 on 2025-01-27 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smsapp', '0036_last_replay_data_last_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='session_key',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
