# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('talent', '0010_auto_20141209_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talentprofile',
            name='is_agency_contact',
            field=models.BooleanField(default=False, verbose_name=b'Have an agent?'),
        ),
        migrations.AlterField(
            model_name='talentprofile',
            name='personal_email',
            field=models.CharField(max_length=32, verbose_name=b'Email Address', blank=True),
        ),
    ]
