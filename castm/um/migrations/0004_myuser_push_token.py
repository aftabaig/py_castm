# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('um', '0003_myuser_activation_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='push_token',
            field=models.CharField(default='', max_length=64, verbose_name=b'Push Token'),
            preserve_default=False,
        ),
    ]
