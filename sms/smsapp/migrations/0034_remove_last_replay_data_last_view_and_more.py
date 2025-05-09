# Generated by Django 5.0.6 on 2025-01-24 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smsapp', '0033_last_replay_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='last_replay_data',
            name='last_view',
        ),
        migrations.AddField(
            model_name='last_replay_data',
            name='count',
            field=models.CharField(default=1, max_length=3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='last_replay_data',
            name='name',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='last_replay_data',
            name='number',
            field=models.CharField(default=1, max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='last_replay_data',
            name='status',
            field=models.CharField(default='unread', max_length=10),
        ),
        migrations.AlterField(
            model_name='last_replay_data',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
