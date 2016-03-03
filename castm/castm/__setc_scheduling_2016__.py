#!/usr/bin/env python
# -*- coding: utf-8 -*-

from socket import gethostname
host_name = gethostname()

import os
if host_name == 'castm':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "production")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "development")

import sys
if host_name == 'castm':
    sys.path.append("/var/www/castm/py_castm/castm")
else:
    sys.path.append("/Users/aftabaig/Projects/Flash/Code/Backends/py_castm/castm")

import django
django.setup()

from django.db import models
from django.contrib.auth.models import User
from events.models import Event, EventAttendee, EventTalentInfo
from schedules.models import Schedule, ScheduleAttendee

# Get reference to "SETC" event.
event = Event.objects.filter(name="SETC 2016").first()
if not event:
    print "SETC event not found"
    sys.exit(0)

schedule_ids = [
    24,
    25,
    26,
    27,
    28,
    29,
    30,
    31,
    32,
    33,
    34,
    35,
    36,
    37,
    38,
    39,
    40,
    41,
    42,
    43,
    44,
]

schedule_audition_ids = [{
    "start": 1,
    "end": 40
}, {
    "start": 41,
    "end": 80
}, {
    "start": 81,
    "end": 120
}, {
    "start": 121,
    "end": 160
}, {
    "start": 161,
    "end": 200
}, {
    "start": 201,
    "end": 240
}, {
    "start": 241,
    "end": 260
}, {
    "start": 261,
    "end": 300
}, {
    "start": 301,
    "end": 340
}, {
    "start": 341,
    "end": 360
}, {
    "start": 361,
    "end": 400
}, {
    "start": 401,
    "end": 440
}, {
    "start": 441,
    "end": 480
}, {
    "start": 481,
    "end": 520
}, {
    "start": 521,
    "end": 560
}, {
    "start": 561,
    "end": 600
}, {
    "start": 601,
    "end": 640
}, {
    "start": 641,
    "end": 680
}, {
    "start": 681,
    "end": 720
}, {
    "start": 721,
    "end": 760
}, {
    "start": 761,
    "end": 780
}]

i = 0
for schedule_id in schedule_ids:
    schedule_audition = schedule_audition_ids[i]
    i += 1
    start = schedule_audition.get("start")
    end = schedule_audition.get("end")
    for audition_id in range(start, end+1):
        print "%s -> %s" % (schedule_id, audition_id)
        q1 = models.Q(event=event)
        q2 = models.Q(audition_id=audition_id)
        event_talent_info = EventTalentInfo.objects.filter(q1 & q2).first()
        if event_talent_info:
            talent = event_talent_info.talent
            schedule = Schedule.objects.filter(id=schedule_id).first()
            schedule_attendee, created = ScheduleAttendee.objects.get_or_create(schedule=schedule, attendee=talent)
            schedule_attendee.save()
