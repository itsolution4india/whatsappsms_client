# Generated by Django 5.0.6 on 2024-11-06 11:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smsapp', '0013_messageresponse'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('can_send_sms', models.BooleanField(default=False)),
                ('can_view_reports', models.BooleanField(default=False)),
                ('can_manage_campaign', models.BooleanField(default=False)),
                ('can_schedule_tasks', models.BooleanField(default=False)),
                ('can_create_flow_message', models.BooleanField(default=False)),
                ('can_send_flow_message', models.BooleanField(default=False)),
                ('can_link_templates', models.BooleanField(default=False)),
                ('can_manage_bot_flow', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
