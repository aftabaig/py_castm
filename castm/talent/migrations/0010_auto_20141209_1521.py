# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('talent', '0009_talentheadshot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talentprofile',
            name='personal_email',
            field=models.CharField(default=False, max_length=32, verbose_name=b'Email Address', blank=True),
        ),
    ]
