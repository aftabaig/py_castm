# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('um', '0002_auto_20141209_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='activation_key',
            field=models.CharField(default='', max_length=32, verbose_name=b'Activation Key'),
            preserve_default=False,
        ),
    ]
