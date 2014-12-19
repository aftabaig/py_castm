# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('talent', '0016_auto_20141219_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talentprofile',
            name='thumbnail',
            field=models.ImageField(default=b'thumbnails/default.png', upload_to=b'thumbnails'),
        ),
    ]
