# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-11 15:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='categorie',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='post.Categorie'),
        ),
    ]