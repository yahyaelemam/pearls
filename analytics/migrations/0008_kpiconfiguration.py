# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-13 05:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0007_auto_20171113_0825'),
    ]

    operations = [
        migrations.CreateModel(
            name='KpiConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_type', models.CharField(choices=[['t', 'Tax Account'], ['z', 'Zaka Account'], ['d', 'Fixed Assets Depreciation Account']], max_length=1)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='zaka', to='analytics.Accounts', verbose_name='GL Account')),
                ('company', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='analytics.Companies')),
            ],
            options={
                'verbose_name': 'KPI Configuration',
                'verbose_name_plural': 'KPIs Configurations',
                'ordering': ['company'],
            },
        ),
    ]