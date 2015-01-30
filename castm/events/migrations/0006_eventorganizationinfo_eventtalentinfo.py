# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_auto_20150121_0532'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0005_auto_20150123_0934'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventOrganizationInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', models.CharField(max_length=256, null=True, verbose_name=b'Location', blank=True)),
                ('notes', models.CharField(max_length=1024, null=True, verbose_name=b'Notes', blank=True)),
                ('event', models.ForeignKey(to='events.Event')),
                ('organization', models.ForeignKey(to='organizations.Organization')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventTalentInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('availability_date_start', models.DateField(null=True, verbose_name=b'Availability - Start', blank=True)),
                ('availability_date_end', models.DateField(null=True, verbose_name=b'Availability - End', blank=True)),
                ('availability_flexible', models.NullBooleanField(verbose_name=b'Is Flexible')),
                ('hiring_preferences', models.CharField(max_length=1024, null=True, verbose_name=b'Hiring Preferences', blank=True)),
                ('event', models.ForeignKey(to='events.Event')),
                ('talent', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
