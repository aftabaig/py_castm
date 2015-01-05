# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_auto_20141224_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='type',
            field=models.CharField(default='ASD', max_length=3, verbose_name=b'Notification Type', choices=[(b'MSG', b'Message'), (b'CB', b'Callback'), (b'LR', b'Link Request'), (b'LA', b'Link Accepted'), (b'LR', b'Link Rejected')]),
            preserve_default=False,
        ),
    ]
