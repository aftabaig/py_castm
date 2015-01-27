# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0010_auto_20150112_0716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='type',
            field=models.CharField(max_length=3, verbose_name=b'Notification Type', choices=[(b'MSG', b'Message'), (b'CB', b'Callback'), (b'LR', b'Link Request'), (b'LA', b'Link Accepted'), (b'LD', b'Link Rejected'), (b'OMI', b'Organization Membership Invitation'), (b'OIA', b'Organization Invitation Accepted'), (b'OIR', b'Organization Invitation Rejected'), (b'OMR', b'Organization Membership Request'), (b'ORA', b'Organization Request Accepted'), (b'ORR', b'Organization Request Rejected'), (b'ER', b'Event Attendance Request'), (b'ERA', b'Event Request Accepted'), (b'ERR', b'Event Request Rejected')]),
        ),
    ]
