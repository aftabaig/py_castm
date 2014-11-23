# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('talent', '0007_auto_20141117_1728'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='talentprofile',
            name='height_feet',
        ),
        migrations.RemoveField(
            model_name='talentprofile',
            name='height_inches',
        ),
        migrations.AddField(
            model_name='talentprofile',
            name='agency',
            field=models.CharField(default='', max_length=255, verbose_name=b'Agency', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='talentprofile',
            name='agency_add1',
            field=models.CharField(default='', max_length=1024, verbose_name=b'Agency Address 1', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='talentprofile',
            name='agency_add2',
            field=models.CharField(default='', max_length=1024, verbose_name=b'Agency Address 2', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='talentprofile',
            name='agency_name',
            field=models.CharField(default='', max_length=255, verbose_name=b'Agency Name', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='talentprofile',
            name='height',
            field=models.IntegerField(default=0, verbose_name=b'Height'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='talentprofile',
            name='is_agency_contact',
            field=models.BooleanField(default='', verbose_name=b'Have an agent?'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='talentprofile',
            name='is_stage_name',
            field=models.BooleanField(default=False, verbose_name=b'Stage Name?'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='talentprofile',
            name='personal_add1',
            field=models.CharField(default='', max_length=1024, verbose_name=b'Personal Address 1', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='talentprofile',
            name='personal_add2',
            field=models.CharField(default='', max_length=1024, verbose_name=b'Personal Address 2', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='talentprofile',
            name='personal_email',
            field=models.CharField(default='', max_length=32, verbose_name=b'Email Address', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='talentprofile',
            name='personal_mobile',
            field=models.CharField(default='', max_length=32, verbose_name=b'Mobile #', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='talentprofile',
            name='personal_office',
            field=models.CharField(default='', max_length=32, verbose_name=b'Office #', blank=True),
            preserve_default=False,
        ),
    ]
