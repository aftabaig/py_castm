# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('talent', '0005_auto_20141115_0938'),
    ]

    operations = [
        migrations.AddField(
            model_name='talentprofile',
            name='resume_categories',
            field=models.TextField(default='', verbose_name=b'Categories Dump', blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='talentprofile',
            name='race',
            field=models.CharField(blank=True, max_length=2, verbose_name=b'Race', choices=[(b'E', b'Ethnic'), (b'R', b'Red-Headed')]),
        ),
    ]
