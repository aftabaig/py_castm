# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('talent', '0012_auto_20141209_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talentprofile',
            name='height',
            field=models.CharField(max_length=32, null=True, verbose_name=b'Height', blank=True),
        ),
        migrations.AlterField(
            model_name='talentprofile',
            name='weight',
            field=models.CharField(max_length=32, null=True, verbose_name=b'Weight', blank=True),
        ),
    ]
