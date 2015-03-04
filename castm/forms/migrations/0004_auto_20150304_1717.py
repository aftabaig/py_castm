# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0003_auto_20150201_0656'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='formfield',
            options={'ordering': ['sort_id']},
        ),
        migrations.AddField(
            model_name='formfield',
            name='sort_id',
            field=models.IntegerField(default=0, blank=True),
            preserve_default=False,
        ),
    ]
