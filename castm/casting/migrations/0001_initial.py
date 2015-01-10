# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('um', '0005_auto_20150106_0822'),
    ]

    operations = [
        migrations.CreateModel(
            name='CastingHeadshot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('headshot', models.ImageField(upload_to=b'headshots')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CastingProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('add1', models.CharField(max_length=1024, verbose_name=b'Address 1', blank=True)),
                ('add2', models.CharField(max_length=1024, verbose_name=b'Address 2', blank=True)),
                ('city', models.CharField(max_length=16, verbose_name=b'City', blank=True)),
                ('state', models.CharField(max_length=16, verbose_name=b'State', blank=True)),
                ('zip', models.CharField(max_length=16, verbose_name=b'Zip', blank=True)),
                ('mobile', models.CharField(max_length=32, verbose_name=b'Mobile #', blank=True)),
                ('office', models.CharField(max_length=32, verbose_name=b'Office #', blank=True)),
                ('thumbnail', models.CharField(max_length=255, verbose_name=b'Thumbnail', blank=True)),
                ('my_user', models.OneToOneField(to='um.MyUser')),
                ('user', models.ForeignKey(related_name=b'casting_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
