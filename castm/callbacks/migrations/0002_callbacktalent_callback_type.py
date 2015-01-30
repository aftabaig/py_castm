# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('callbacks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='callbacktalent',
            name='callback_type',
            field=models.CharField(default='RCB', max_length=3, verbose_name=b'Callback Type', choices=[(b'RCB', b'Regular Callback'), (b'DCB', b'Dancer Callback'), (b'HCB', b'Headshot/Resume Callback')]),
            preserve_default=False,
        ),
    ]
