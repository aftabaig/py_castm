# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notifications', '0003_auto_20141223_1510'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256, verbose_name=b'Notification Title')),
                ('message', models.CharField(max_length=1024, verbose_name=b'Message')),
                ('seen', models.BooleanField(default=False, verbose_name=b'Seen')),
                ('action_taken', models.BooleanField(default=False, verbose_name=b'Action taken?')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('for_user', models.ForeignKey(related_name=b'notification', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='Callback',
        ),
        migrations.RemoveField(
            model_name='message',
            name='from_user',
        ),
        migrations.RemoveField(
            model_name='message',
            name='to_user',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]
