# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('um', '0008_auto_20150204_0552'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='sub_type',
        ),
    ]
