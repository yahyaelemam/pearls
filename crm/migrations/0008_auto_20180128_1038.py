# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-28 07:38
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0018_auto_20180113_0906'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crm', '0007_auto_20180127_1746'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomersBudget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('budget_amount', models.PositiveIntegerField(default=0)),
                ('status', models.CharField(blank=True, choices=[['d', 'Draft'], ['s', 'Saved'], ['a', 'Approved']], default='d', max_length=1, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='analytics.Companies')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='crm.Customers')),
                ('sale_agent', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='crm.SalesAgents')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='analytics.BudgetYear', verbose_name='Year')),
            ],
            options={
                'verbose_name': 'Customer Budget',
                'verbose_name_plural': 'Customers Budget',
            },
        ),
        migrations.AlterModelOptions(
            name='opportunities',
            options={'permissions': (('opportunities_add', 'Can  Add Opportunity'), ('Update_Opportunity', 'Can uUpdate Opportunity')), 'verbose_name': 'Opportunity', 'verbose_name_plural': 'Opportunities'},
        ),
        migrations.AlterField(
            model_name='categoriesbudget',
            name='status',
            field=models.CharField(blank=True, choices=[['d', 'Draft'], ['s', 'Saved'], ['a', 'Approved']], default='d', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='customersactivities',
            name='activity_date',
            field=models.DateField(default=datetime.date(2018, 1, 28)),
        ),
        migrations.AlterField(
            model_name='customersactivities',
            name='status',
            field=models.CharField(blank=True, choices=[['c', 'Closed'], ['o', 'Open']], default='o', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='customersactivitiesactions',
            name='action_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 1, 28, 7, 38, 16, 583311, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='customersactivitiesactions',
            name='status',
            field=models.CharField(blank=True, choices=[['c', 'Closed'], ['o', 'Open']], default='o', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='customersdetails',
            name='registration_date',
            field=models.DateField(default=datetime.date(2018, 1, 28)),
        ),
        migrations.AlterField(
            model_name='customersstatus',
            name='event_date',
            field=models.DateField(blank=True, default=datetime.date(2018, 1, 28), null=True),
        ),
        migrations.AlterField(
            model_name='customersstatus',
            name='rate',
            field=models.CharField(blank=True, choices=[['e', 'Excellent'], ['g', 'Good'], ['n', 'Not Rated'], ['a', 'Accepted'], ['v', 'V.Good']], default='n', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='customersstatus',
            name='status',
            field=models.CharField(blank=True, choices=[['d', 'Dormant'], ['n', 'New'], ['a', 'Active'], ['r', 'Archived']], default='n', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='industriesbudget',
            name='status',
            field=models.CharField(blank=True, choices=[['d', 'Draft'], ['s', 'Saved'], ['a', 'Approved']], default='d', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='opportunities',
            name='status',
            field=models.CharField(blank=True, choices=[['m', 'Missed'], ['s', 'Success'], ['o', 'Open']], default='o', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='salesagentsbudget',
            name='status',
            field=models.CharField(blank=True, choices=[['d', 'Draft'], ['s', 'Saved'], ['a', 'Approved']], default='d', max_length=1, null=True),
        ),
        migrations.AddIndex(
            model_name='customersbudget',
            index=models.Index(fields=['status'], name='crm_custome_status_409477_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='customersbudget',
            unique_together=set([('year', 'customer', 'sale_agent')]),
        ),
    ]
