# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0002_link_notification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='link',
            name='notification',
        ),
    ]
