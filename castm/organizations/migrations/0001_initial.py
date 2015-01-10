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
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, verbose_name=b'Organization Name')),
                ('add1', models.CharField(max_length=1024, verbose_name=b'Address 1', blank=True)),
                ('add2', models.CharField(max_length=1024, verbose_name=b'Address 2', blank=True)),
                ('city', models.CharField(max_length=16, verbose_name=b'City', blank=True)),
                ('state', models.CharField(max_length=16, verbose_name=b'State', blank=True)),
                ('zip', models.CharField(max_length=16, verbose_name=b'Zip', blank=True)),
                ('mobile', models.CharField(max_length=32, verbose_name=b'Mobile #', blank=True)),
                ('office', models.CharField(max_length=32, verbose_name=b'Office #', blank=True)),
                ('logo', models.CharField(max_length=255, verbose_name=b'Logo', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrganizationMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(max_length=4, verbose_name=b"Member's Role")),
                ('is_accepted', models.BooleanField(default=False, verbose_name=b'Is Accepted')),
                ('is_rejected', models.BooleanField(default=False, verbose_name=b'Is Rejected')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('initiator', models.ForeignKey(related_name=b'initiated_members', to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(related_name=b'members', to='organizations.Organization')),
                ('user', models.ForeignKey(related_name=b'user_members', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
