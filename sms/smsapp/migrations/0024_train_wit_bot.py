# Generated by Django 5.0.6 on 2024-12-13 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smsapp', '0023_customuser_authentication_coins_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Train_wit_Bot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=100, unique=True)),
                ('intent', models.CharField(max_length=100, unique=True)),
                ('content', models.TextField(default='nan')),
            ],
        ),
    ]
