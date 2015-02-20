# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('talent', '0022_auto_20150205_1906'),
    ]

    operations = [
        migrations.AddField(
            model_name='talentprofile',
            name='agency_email',
            field=models.CharField(default='', max_length=255, verbose_name=b'Agency Email', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='talentprofile',
            name='agency_mobile',
            field=models.CharField(default='', max_length=255, verbose_name=b'Agency Mobile', blank=True),
            preserve_default=False,
        ),
    ]
