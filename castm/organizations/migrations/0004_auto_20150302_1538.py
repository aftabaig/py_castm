# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0003_auto_20150302_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='city',
            field=models.CharField(max_length=64, null=True, verbose_name=b'City', blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='mobile',
            field=models.CharField(max_length=64, null=True, verbose_name=b'Mobile #', blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='office',
            field=models.CharField(max_length=64, null=True, verbose_name=b'Office #', blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='state',
            field=models.CharField(max_length=64, null=True, verbose_name=b'State', blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='zip',
            field=models.CharField(max_length=64, null=True, verbose_name=b'Zip', blank=True),
        ),
    ]
