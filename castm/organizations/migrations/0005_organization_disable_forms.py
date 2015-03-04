# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0004_auto_20150302_1538'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='disable_forms',
            field=models.BooleanField(default=False, verbose_name=b'Form Disabled?'),
            preserve_default=True,
        ),
    ]
