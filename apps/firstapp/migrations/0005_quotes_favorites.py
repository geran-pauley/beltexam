# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-24 19:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0004_auto_20180424_1132'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotes',
            name='favorites',
            field=models.ManyToManyField(null=True, related_name='favorites', to='firstapp.User'),
        ),
    ]
