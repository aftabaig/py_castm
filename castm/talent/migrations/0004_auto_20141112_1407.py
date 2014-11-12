# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('talent', '0003_auto_20141112_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resumecategory',
            name='is_list',
            field=models.BooleanField(default=True, verbose_name=b'Is List'),
        ),
    ]
