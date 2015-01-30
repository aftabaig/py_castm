# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_auto_20150121_0532'),
        ('events', '0005_auto_20150123_0934'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Callback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('callback_organization', models.ForeignKey(related_name=b'callbacks', to='organizations.Organization')),
                ('event', models.ForeignKey(related_name=b'event_callbacks', to='events.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CallbackTalent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sent_to_event_organization', models.BooleanField(default=False)),
                ('sent_to_talent', models.BooleanField(default=False)),
                ('callback', models.ForeignKey(related_name=b'callback_talents', to='callbacks.Callback')),
                ('talent', models.ForeignKey(related_name=b'user_callback_talent', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
