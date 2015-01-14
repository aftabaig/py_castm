# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0002_event_schedule_published'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=64, verbose_name=b'Schedule Title')),
                ('schedule_date', models.DateField()),
                ('schedule_time_from', models.TimeField()),
                ('schedule_time_to', models.TimeField()),
                ('event', models.ForeignKey(related_name=b'event_schedules', to='events.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ScheduleAttendee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attendee', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('schedule', models.ForeignKey(related_name=b'schedule_attendees', to='schedules.Schedule')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
