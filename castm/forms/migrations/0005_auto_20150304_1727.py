# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0004_auto_20150304_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formfield',
            name='sort_id',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
