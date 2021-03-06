# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-13 04:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='KpiConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ebitda_account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ebitda', to='analytics.Accounts')),
                ('tax_account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tax', to='analytics.Accounts')),
            ],
        ),
    ]
