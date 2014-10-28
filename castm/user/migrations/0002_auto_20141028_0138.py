# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consignment',
            name='eta_date',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 1, 38, 17, 485222), verbose_name=b'ETA'),
        ),
        migrations.AlterField(
            model_name='consignment',
            name='pickupDate',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 28, 1, 38, 17, 485191), verbose_name=b'Pickup Date'),
        ),
    ]
