# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-06-14 06:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('strategyceleryapp', '0005_auto_20170221_0341'),
    ]

    operations = [
        migrations.AddField(
            model_name='strategy',
            name='tickers',
            field=models.TextField(default=''),
        ),
        migrations.AlterUniqueTogether(
            name='strategy',
            unique_together=set([('user', 'strategy_name')]),
        ),
    ]
