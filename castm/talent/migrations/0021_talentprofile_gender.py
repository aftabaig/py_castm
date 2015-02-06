# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('talent', '0020_auto_20150109_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='talentprofile',
            name='gender',
            field=models.CharField(default='M', max_length=1, verbose_name=b'Gender', blank=True, choices=[(b'M', b'Male'), (b'F', b'Female')]),
            preserve_default=False,
        ),
    ]
