# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0002_auto_20150126_1811'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fielditem',
            options={'ordering': ['id']},
        ),
    ]
