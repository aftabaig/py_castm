# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20141028_0138'),
    ]

    operations = [
        migrations.AddField(
            model_name='consignment',
            name='airway_bill_number',
            field=models.CharField(default='', max_length=64, verbose_name=b'Airway Bill #', blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='consignment',
            name='eta_date',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 1, 39, 6, 759129), verbose_name=b'ETA'),
        ),
        migrations.AlterField(
            model_name='consignment',
            name='pickupDate',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 1, 39, 6, 759093), verbose_name=b'Pickup Date'),
        ),
    ]
