# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name=b'Event Name')),
                ('audition_date', models.DateField(auto_now_add=True)),
                ('audition_time_from', models.TimeField()),
                ('audition_time_to', models.TimeField()),
                ('callback_date', models.DateField(auto_now_add=True)),
                ('callback_time_from', models.TimeField()),
                ('callback_time_to', models.TimeField()),
                ('owner', models.ForeignKey(related_name=b'events', to='organizations.Organization')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventAttendee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_accepted', models.BooleanField(default=False, verbose_name=b'Is Accepted')),
                ('is_rejected', models.BooleanField(default=False, verbose_name=b'Is Rejected')),
                ('attendee', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(related_name=b'attendees', to='events.Event')),
                ('organization', models.ForeignKey(blank=True, to='organizations.Organization', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
