# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('um', '0007_myuser_device_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDevice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('device_type', models.CharField(max_length=8, verbose_name=b'Device Type', choices=[(b'iOS', b'iOS'), (b'Android', b'Android')])),
                ('push_token', models.CharField(max_length=64, null=True, verbose_name=b'Push Token', blank=True)),
                ('user', models.ForeignKey(related_name=b'user_devices', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='device_type',
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='push_token',
        ),
    ]
