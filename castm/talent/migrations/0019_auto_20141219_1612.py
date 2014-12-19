# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('talent', '0018_auto_20141219_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talentprofile',
            name='thumbnail',
            field=models.CharField(max_length=255, verbose_name=b'Thumbnail', blank=True),
        ),
    ]
