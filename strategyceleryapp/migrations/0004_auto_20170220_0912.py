# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-20 09:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('strategyceleryapp', '0003_strategy_output'),
    ]

    operations = [
        migrations.AddField(
            model_name='symbol',
            name='currency',
            field=models.CharField(default='USD', max_length=64),
        ),
        migrations.AddField(
            model_name='symbol',
            name='instrument',
            field=models.CharField(default='stock', max_length=64),
        ),
        migrations.AddField(
            model_name='symbol',
            name='sector',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AlterField(
            model_name='daily_price',
            name='symbol_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='strategyceleryapp.symbol'),
        ),
    ]
