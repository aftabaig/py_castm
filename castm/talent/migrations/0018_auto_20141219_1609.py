# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('talent', '0017_auto_20141219_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talentprofile',
            name='thumbnail',
            field=models.ImageField(default=b'http://res.cloudinary.com/flash-solutions/image/upload/v1419026575/default_acaywm.png', upload_to=b'headshots'),
        ),
    ]
