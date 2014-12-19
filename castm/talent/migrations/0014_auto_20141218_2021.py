# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('talent', '0013_auto_20141216_2147'),
    ]

    operations = [
        migrations.AddField(
            model_name='talentprofile',
            name='agency_city',
            field=models.CharField(default='', max_length=16, verbose_name=b'City', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='talentprofile',
            name='agency_state',
            field=models.CharField(default='', max_length=16, verbose_name=b'State', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='talentprofile',
            name='agency_zip',
            field=models.CharField(default='', max_length=16, verbose_name=b'Zip', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='talentprofile',
            name='personal_city',
            field=models.CharField(default='', max_length=16, verbose_name=b'City', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='talentprofile',
            name='personal_state',
            field=models.CharField(default='', max_length=16, verbose_name=b'State', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='talentprofile',
            name='personal_zip',
            field=models.CharField(default='', max_length=16, verbose_name=b'Zip', blank=True),
            preserve_default=False,
        ),
    ]
