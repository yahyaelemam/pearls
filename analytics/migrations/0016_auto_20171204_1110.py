# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-04 08:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0015_auto_20171204_0945'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='role',
            options={'permissions': (('landing_page', 'Can  view landing'), ('acc_trends', 'Can  view trends accounts'), ('mrg_exp_rev', 'Can  view margin expenses and revenues KPI'), ('budget', 'Can  view budget KPI'), ('kpi_settings', 'Can  configure KPIs settings')), 'verbose_name': 'Role', 'verbose_name_plural': 'Roles'},
        ),
    ]
