# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('um', '0004_myuser_push_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='push_token',
            field=models.CharField(max_length=64, null=True, verbose_name=b'Push Token', blank=True),
        ),
    ]
