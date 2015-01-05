# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('optional_message', models.CharField(max_length=1024, verbose_name=b'Optional Message', blank=True)),
                ('is_accepted', models.BooleanField(default=False, verbose_name=b'Is Accepted')),
                ('is_rejected', models.BooleanField(default=False, verbose_name=b'Is Rejected')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('from_user', models.ForeignKey(related_name=b'from_link', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(related_name=b'to_link', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
