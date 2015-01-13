# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_messages', '0002_remove_message_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='title',
            field=models.CharField(default='', max_length=64, verbose_name=b'Title'),
            preserve_default=False,
        ),
    ]
