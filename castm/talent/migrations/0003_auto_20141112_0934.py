# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('talent', '0002_auto_20141112_0931'),
    ]

    operations = [
        migrations.RenameField(
            model_name='talentprofile',
            old_name='uer',
            new_name='user',
        ),
    ]
