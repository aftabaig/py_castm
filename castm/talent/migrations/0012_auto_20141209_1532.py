# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('talent', '0011_auto_20141209_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talentprofile',
            name='is_stage_name',
            field=models.BooleanField(default=False, verbose_name=b'Stage Name?'),
        ),
    ]
