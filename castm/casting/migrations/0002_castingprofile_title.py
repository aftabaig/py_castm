# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('casting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='castingprofile',
            name='title',
            field=models.CharField(default='', max_length=255, verbose_name=b'Title', db_index=True, blank=True),
            preserve_default=False,
        ),
    ]
