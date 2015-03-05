# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_eventtalentinfo_audition_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='audition_end_date',
            field=models.CharField(max_length=64, null=True, verbose_name=b'Audition End Date', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='audition_start_date',
            field=models.CharField(max_length=64, null=True, verbose_name=b'Audition Start Date', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='audition_time_from',
            field=models.CharField(max_length=64, null=True, verbose_name=b'Audition Time From', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='audition_time_to',
            field=models.CharField(max_length=64, null=True, verbose_name=b'Audition Time To', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='callback_end_date',
            field=models.CharField(max_length=64, null=True, verbose_name=b'Callback End Date', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='callback_start_date',
            field=models.CharField(max_length=64, null=True, verbose_name=b'Callback Start Date', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='callback_time_from',
            field=models.CharField(max_length=64, null=True, verbose_name=b'Callback Time From', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='callback_time_to',
            field=models.CharField(max_length=64, null=True, verbose_name=b'Callback Time To', blank=True),
        ),
    ]
