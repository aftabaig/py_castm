# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('talent', '0023_auto_20150220_0849'),
    ]

    operations = [
        migrations.AddField(
            model_name='talentheadshot',
            name='headshot_original',
            field=models.ImageField(default='', upload_to=b'headshots'),
            preserve_default=False,
        ),
    ]
