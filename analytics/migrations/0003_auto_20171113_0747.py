# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-13 04:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0002_kpiconfiguration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kpiconfiguration',
            name='ebitda_account',
        ),
        migrations.RemoveField(
            model_name='kpiconfiguration',
            name='tax_account',
        ),
        migrations.DeleteModel(
            name='KpiConfiguration',
        ),
    ]
