# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-11 10:10
from __future__ import unicode_literals

from django.db import migrations, models
import feeds.models


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to=feeds.models.group_based_uploadPost),
        ),
    ]
