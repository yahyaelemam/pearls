# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-27 08:46
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0018_auto_20180113_0906'),
        ('crm', '0003_auto_20180123_2243'),
    ]

    operations = [
        migrations.AddField(
            model_name='opportunities',
            name='company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='analytics.Companies'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='categoriesbudget',
            name='status',
            field=models.CharField(blank=True, choices=[['d', 'Draft'], ['s', 'Saved'], ['a', 'Approved']], default='d', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='customersactivities',
            name='activity_date',
            field=models.DateField(default=datetime.date(2018, 1, 27)),
        ),
        migrations.AlterField(
            model_name='customersactivities',
            name='status',
            field=models.CharField(blank=True, choices=[['o', 'Open'], ['c', 'Closed']], default='o', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='customersactivitiesactions',
            name='action_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 1, 27, 8, 46, 12, 837869, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='customersactivitiesactions',
            name='status',
            field=models.CharField(blank=True, choices=[['o', 'Open'], ['c', 'Closed']], default='o', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='customersdetails',
            name='registration_date',
            field=models.DateField(default=datetime.date(2018, 1, 27)),
        ),
        migrations.AlterField(
            model_name='customersstatus',
            name='event_date',
            field=models.DateField(blank=True, default=datetime.date(2018, 1, 27), null=True),
        ),
        migrations.AlterField(
            model_name='customersstatus',
            name='rate',
            field=models.CharField(blank=True, choices=[['n', 'Not Rated'], ['v', 'V.Good'], ['e', 'Excellent'], ['g', 'Good'], ['a', 'Accepted']], default='n', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='industriesbudget',
            name='status',
            field=models.CharField(blank=True, choices=[['d', 'Draft'], ['s', 'Saved'], ['a', 'Approved']], default='d', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='opportunities',
            name='status',
            field=models.CharField(blank=True, choices=[['m', 'Missed'], ['o', 'Open'], ['s', 'Success']], default='o', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='salesagentsbudget',
            name='status',
            field=models.CharField(blank=True, choices=[['d', 'Draft'], ['s', 'Saved'], ['a', 'Approved']], default='d', max_length=1, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='opportunities',
            unique_together=set([('customer', 'company', 'status')]),
        ),
    ]
