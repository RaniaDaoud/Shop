# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-18 09:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_utilisateur'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='age',
            field=models.IntegerField(default=30),
        ),
    ]
