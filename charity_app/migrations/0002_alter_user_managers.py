# Generated by Django 5.0.1 on 2024-01-23 20:57

import charity_app.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('charity_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', charity_app.models.CharityUserManager()),
            ],
        ),
    ]
