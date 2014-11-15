# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('talent', '0004_auto_20141112_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talentprofile',
            name='birth_day',
            field=models.DateField(null=True, verbose_name=b'Birthday', blank=True),
        ),
    ]
