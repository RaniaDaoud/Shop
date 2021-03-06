# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-23 13:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('post', '0004_auto_20170815_1353'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_type', models.CharField(choices=[('F', 'Favorite'), ('L', 'Like'), ('U', 'Up Vote'), ('D', 'Down Vote')], max_length=1)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('feed', models.IntegerField(blank=True, null=True)),
                ('question', models.IntegerField(blank=True, null=True)),
                ('answer', models.IntegerField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Activity',
                'verbose_name_plural': 'Activities',
            },
        ),
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, choices=[('normal', 'normal'), ('smile', 'smile'), ('love', 'love'), ('wish', 'wish'), ('like', 'like'), ('dislike', 'dislike')], max_length=255, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='post.Post')),
                ('produit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Produit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='reaction',
            unique_together=set([('user', 'produit', 'post')]),
        ),
    ]
