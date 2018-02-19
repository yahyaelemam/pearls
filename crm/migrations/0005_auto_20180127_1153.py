# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-27 08:53
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_auto_20180127_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoriesbudget',
            name='status',
            field=models.CharField(blank=True, choices=[['s', 'Saved'], ['a', 'Approved'], ['d', 'Draft']], default='d', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='customersactivitiesactions',
            name='action_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 1, 27, 8, 53, 38, 589877, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='customersstatus',
            name='rate',
            field=models.CharField(blank=True, choices=[['v', 'V.Good'], ['n', 'Not Rated'], ['a', 'Accepted'], ['e', 'Excellent'], ['g', 'Good']], default='n', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='customersstatus',
            name='status',
            field=models.CharField(blank=True, choices=[['r', 'Archived'], ['n', 'New'], ['a', 'Active'], ['d', 'Dormant']], default='n', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='industriesbudget',
            name='status',
            field=models.CharField(blank=True, choices=[['s', 'Saved'], ['a', 'Approved'], ['d', 'Draft']], default='d', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='opportunities',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='crm.Customers'),
        ),
        migrations.AlterField(
            model_name='opportunities',
            name='status',
            field=models.CharField(blank=True, choices=[['o', 'Open'], ['s', 'Success'], ['m', 'Missed']], default='o', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='salesagentsbudget',
            name='status',
            field=models.CharField(blank=True, choices=[['s', 'Saved'], ['a', 'Approved'], ['d', 'Draft']], default='d', max_length=1, null=True),
        ),
    ]
