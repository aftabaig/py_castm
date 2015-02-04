# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_eventorganizationinfo_eventtalentinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventtalentinfo',
            name='audition_id',
            field=models.CharField(default='0', max_length=16, verbose_name=b'Audition #'),
            preserve_default=False,
        ),
    ]
