# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20141028_0139'),
    ]

    operations = [
        migrations.AddField(
            model_name='consignment',
            name='airport_destination',
            field=models.CharField(default='', max_length=3, verbose_name=b'Airport Destination', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='consignment',
            name='airport_originating',
            field=models.CharField(default='', max_length=3, verbose_name=b'Airport Originating', blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='consignment',
            name='eta_date',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 2, 49, 50, 911427), verbose_name=b'ETA'),
        ),
        migrations.AlterField(
            model_name='consignment',
            name='pickupDate',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 2, 49, 50, 911387), verbose_name=b'Pickup Date'),
        ),
    ]
