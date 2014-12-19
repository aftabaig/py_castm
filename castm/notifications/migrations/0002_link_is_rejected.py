# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='is_rejected',
            field=models.BooleanField(default=False, verbose_name=b'Is Rejected'),
            preserve_default=True,
        ),
    ]
