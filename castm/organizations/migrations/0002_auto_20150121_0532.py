# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='add1',
            field=models.CharField(max_length=1024, null=True, verbose_name=b'Address 1', blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='add2',
            field=models.CharField(max_length=1024, null=True, verbose_name=b'Address 2', blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='city',
            field=models.CharField(max_length=16, null=True, verbose_name=b'City', blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='logo',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Logo', blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='mobile',
            field=models.CharField(max_length=32, null=True, verbose_name=b'Mobile #', blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='office',
            field=models.CharField(max_length=32, null=True, verbose_name=b'Office #', blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='state',
            field=models.CharField(max_length=16, null=True, verbose_name=b'State', blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='zip',
            field=models.CharField(max_length=16, null=True, verbose_name=b'Zip', blank=True),
        ),
    ]
