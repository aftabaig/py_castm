# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0008_auto_20150109_1814'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='title',
        ),
    ]
