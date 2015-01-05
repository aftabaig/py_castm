# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_link_is_rejected'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='link',
            name='from_user',
        ),
        migrations.RemoveField(
            model_name='link',
            name='to_user',
        ),
        migrations.DeleteModel(
            name='Link',
        ),
    ]
