# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('um', '0006_auto_20150114_0623'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='device_type',
            field=models.CharField(default='iOS', max_length=8, verbose_name=b'Device Type', choices=[(b'iOS', b'iOS'), (b'Android', b'Android')]),
            preserve_default=False,
        ),
    ]
