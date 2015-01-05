# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_auto_20141224_1914'),
        ('links', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='notification',
            field=models.ForeignKey(related_name=b'link', default=None, to='notifications.Notification'),
            preserve_default=False,
        ),
    ]
