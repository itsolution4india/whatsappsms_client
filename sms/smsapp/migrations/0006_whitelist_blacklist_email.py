# Generated by Django 5.0.6 on 2024-07-06 06:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smsapp', '0005_templates'),
    ]

    operations = [
        migrations.AddField(
            model_name='whitelist_blacklist',
            name='email',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
