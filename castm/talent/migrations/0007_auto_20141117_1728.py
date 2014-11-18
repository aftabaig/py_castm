# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('talent', '0006_auto_20141117_1325'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoryjob',
            name='category',
        ),
        migrations.RemoveField(
            model_name='categoryjob',
            name='user',
        ),
        migrations.DeleteModel(
            name='CategoryJob',
        ),
        migrations.RemoveField(
            model_name='categorylistitem',
            name='category',
        ),
        migrations.RemoveField(
            model_name='categorylistitem',
            name='user',
        ),
        migrations.DeleteModel(
            name='CategoryListItem',
        ),
        migrations.RemoveField(
            model_name='resumecategory',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='resumecategory',
            name='user',
        ),
        migrations.DeleteModel(
            name='ResumeCategory',
        ),
    ]
