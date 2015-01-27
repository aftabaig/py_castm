# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formfield',
            name='type',
            field=models.CharField(max_length=5, verbose_name=b'Field Type', choices=[(b'TXT', b'Text'), (b'MUL', b'Multi-line'), (b'SCL', b'Scale'), (b'RAD', b'Radio Button'), (b'CHK', b'Checkbox'), (b'DRPD', b'Drop-down')]),
        ),
        migrations.AlterField(
            model_name='formfield',
            name='use_stars',
            field=models.NullBooleanField(default=False),
        ),
    ]
