# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('talent', '0015_talentprofile_agency_office_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='talentprofile',
            name='thumbnail',
            field=models.ImageField(default='', upload_to=b'thumbnails'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='talentprofile',
            name='user',
            field=models.ForeignKey(related_name=b'user_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
