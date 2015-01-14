# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('um', '0005_auto_20150106_0822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='sub_type',
            field=models.CharField(max_length=2, verbose_name=b'Account Sub Type', blank=True),
        ),
    ]
