# Generated by Django 5.0.6 on 2024-11-06 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smsapp', '0015_coinshistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='coinshistory',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=9, unique=True),
        ),
    ]
