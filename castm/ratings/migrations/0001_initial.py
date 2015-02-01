# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_auto_20150121_0532'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forms', '0003_auto_20150201_0656'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rated_at', models.DateTimeField(auto_now_add=True)),
                ('casting_organization', models.ForeignKey(to='organizations.Organization')),
                ('casting_user', models.ForeignKey(related_name=b'rating_casting_user', to=settings.AUTH_USER_MODEL)),
                ('rating_form', models.ForeignKey(to='forms.RatingForm')),
                ('talent_user', models.ForeignKey(related_name=b'rating_talent_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserRatingField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field_value', models.CharField(max_length=64, verbose_name=b'Rating Value')),
                ('form_field', models.ForeignKey(to='forms.FormField')),
                ('rating', models.ForeignKey(to='ratings.UserRating')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
