# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20150123_0901'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='add1',
            field=models.CharField(max_length=1024, null=True, verbose_name=b'Address 1', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='add2',
            field=models.CharField(max_length=1024, null=True, verbose_name=b'Address 2', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='city',
            field=models.CharField(max_length=16, null=True, verbose_name=b'City', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='state',
            field=models.CharField(max_length=16, null=True, verbose_name=b'State', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='zip',
            field=models.CharField(max_length=16, null=True, verbose_name=b'Zip', blank=True),
            preserve_default=True,
        ),
    ]
