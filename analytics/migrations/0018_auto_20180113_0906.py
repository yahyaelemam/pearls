# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-13 06:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0017_userssettings_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='status',
            field=models.CharField(blank=True, choices=[['d', 'Draft'], ['s', 'Saved'], ['a', 'Approved']], default='d', max_length=1, null=True),
        ),
    ]