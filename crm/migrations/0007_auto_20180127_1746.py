# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-27 14:46
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0006_auto_20180127_1745'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='opportunities',
            options={'permissions': (), 'verbose_name': 'Opportunity', 'verbose_name_plural': 'Opportunities'},
        ),
        migrations.AlterField(
            model_name='categoriesbudget',
            name='status',
            field=models.CharField(blank=True, choices=[['s', 'Saved'], ['d', 'Draft'], ['a', 'Approved']], default='d', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='customersactivities',
            name='status',
            field=models.CharField(blank=True, choices=[['o', 'Open'], ['c', 'Closed']], default='o', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='customersactivitiesactions',
            name='action_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 1, 27, 14, 46, 18, 99939, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='customersactivitiesactions',
            name='status',
            field=models.CharField(blank=True, choices=[['o', 'Open'], ['c', 'Closed']], default='o', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='customersstatus',
            name='rate',
            field=models.CharField(blank=True, choices=[['n', 'Not Rated'], ['a', 'Accepted'], ['g', 'Good'], ['e', 'Excellent'], ['v', 'V.Good']], default='n', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='industriesbudget',
            name='status',
            field=models.CharField(blank=True, choices=[['s', 'Saved'], ['d', 'Draft'], ['a', 'Approved']], default='d', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='opportunities',
            name='status',
            field=models.CharField(blank=True, choices=[['o', 'Open'], ['s', 'Success'], ['m', 'Missed']], default='o', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='salesagentsbudget',
            name='status',
            field=models.CharField(blank=True, choices=[['s', 'Saved'], ['d', 'Draft'], ['a', 'Approved']], default='d', max_length=1, null=True),
        ),
    ]