# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('talent', '0014_auto_20141218_2021'),
    ]

    operations = [
        migrations.AddField(
            model_name='talentprofile',
            name='agency_office_num',
            field=models.CharField(default='', max_length=16, verbose_name=b'Agency Office #', blank=True),
            preserve_default=False,
        ),
    ]
