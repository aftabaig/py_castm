# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('talent', '0019_auto_20141219_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talentprofile',
            name='stage_first_name',
            field=models.CharField(db_index=True, max_length=32, verbose_name=b'Stage First Name', blank=True),
        ),
        migrations.AlterField(
            model_name='talentprofile',
            name='stage_last_name',
            field=models.CharField(db_index=True, max_length=32, verbose_name=b'Stage Last Name', blank=True),
        ),
        migrations.AlterField(
            model_name='talentprofile',
            name='title',
            field=models.CharField(db_index=True, max_length=255, verbose_name=b'Title', blank=True),
        ),
    ]
