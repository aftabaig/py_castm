# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0006_auto_20150107_0548'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='source_id',
            field=models.IntegerField(default=1, verbose_name=b'Notification Source Id'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='notification',
            name='type',
            field=models.CharField(max_length=3, verbose_name=b'Notification Type', choices=[(b'MSG', b'Message'), (b'CB', b'Callback'), (b'LR', b'Link Request'), (b'LA', b'Link Accepted'), (b'LR', b'Link Rejected'), (b'OMI', b'Organization Membership Invitation'), (b'OIA', b'Organization Invitation Accepted'), (b'OIR', b'Organization Invitation Rejected'), (b'OMR', b'Organization Membership Request'), (b'ORA', b'Organization Request Accepted'), (b'ORR', b'Organization Request Rejected')]),
        ),
    ]
