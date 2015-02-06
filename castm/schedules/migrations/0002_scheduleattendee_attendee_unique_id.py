# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduleattendee',
            name='attendee_unique_id',
            field=models.CharField(max_length=16, null=True, verbose_name=b'Unique Id', blank=True),
            preserve_default=True,
        ),
    ]
