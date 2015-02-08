# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0002_scheduleattendee_attendee_unique_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='sort_id',
            field=models.IntegerField(default=0, blank=True),
            preserve_default=False,
        ),
    ]
