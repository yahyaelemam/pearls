# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-13 05:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0008_kpiconfiguration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kpiconfiguration',
            name='account_type',
            field=models.CharField(choices=[['t', 'Tax Account'], ['z', 'Zaka Account'], ['d', 'FA Depreciation Account']], max_length=1),
        ),
        migrations.AlterField(
            model_name='kpiconfiguration',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analytics.Companies'),
        ),
    ]