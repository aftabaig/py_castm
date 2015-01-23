# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20150120_0659'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='audition_date',
            new_name='audition_end_date',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='callback_date',
            new_name='audition_start_date',
        ),
        migrations.AddField(
            model_name='event',
            name='callback_end_date',
            field=models.DateField(default=datetime.date(2015, 1, 23), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='callback_start_date',
            field=models.DateField(default=datetime.date(2015, 1, 23), auto_now_add=True),
            preserve_default=False,
        ),
    ]
