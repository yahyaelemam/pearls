# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-18 16:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0009_auto_20171113_0841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounts',
            name='active',
            field=models.NullBooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='accounts',
            name='parentid',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Parent ID'),
        ),
    ]