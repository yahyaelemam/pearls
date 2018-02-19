# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-13 04:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0005_auto_20171113_0756'),
    ]

    operations = [
        migrations.CreateModel(
            name='KpiConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='analytics.Companies')),
                ('fa_depreciation_account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ebitda', to='analytics.Accounts', verbose_name='Fixed Asset Depreciation Account')),
                ('tax_account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tax', to='analytics.Accounts', verbose_name='Tax Account')),
                ('zaka_account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='zaka', to='analytics.Accounts', verbose_name='Zaka account')),
            ],
            options={
                'verbose_name': 'KPI Configuration',
                'ordering': ['company'],
                'verbose_name_plural': 'KPIs Configurations',
            },
        ),
    ]
