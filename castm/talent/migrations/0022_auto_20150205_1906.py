# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('talent', '0021_talentprofile_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talentprofile',
            name='agency_city',
            field=models.CharField(max_length=32, verbose_name=b'City', blank=True),
        ),
        migrations.AlterField(
            model_name='talentprofile',
            name='agency_state',
            field=models.CharField(max_length=32, verbose_name=b'State', blank=True),
        ),
        migrations.AlterField(
            model_name='talentprofile',
            name='agency_zip',
            field=models.CharField(max_length=32, verbose_name=b'Zip', blank=True),
        ),
        migrations.AlterField(
            model_name='talentprofile',
            name='personal_city',
            field=models.CharField(max_length=32, verbose_name=b'City', blank=True),
        ),
        migrations.AlterField(
            model_name='talentprofile',
            name='personal_email',
            field=models.CharField(max_length=75, verbose_name=b'Email Address', blank=True),
        ),
        migrations.AlterField(
            model_name='talentprofile',
            name='personal_state',
            field=models.CharField(max_length=32, verbose_name=b'State', blank=True),
        ),
        migrations.AlterField(
            model_name='talentprofile',
            name='personal_zip',
            field=models.CharField(max_length=32, verbose_name=b'Zip', blank=True),
        ),
    ]
