# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-25 11:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_remove_produit_product'),
        ('wish_list', '0003_remove_wishlist_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlist',
            name='product',
            field=models.ManyToManyField(to='shop.Produit'),
        ),
    ]