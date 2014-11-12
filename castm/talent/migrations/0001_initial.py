# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('um', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryJob',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=32, verbose_name=b'Title')),
                ('sub_title_1', models.CharField(max_length=32, verbose_name=b'Sub Title 1')),
                ('sub_title_2', models.CharField(max_length=32, verbose_name=b'Sub Title 2')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CategoryListItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=32, verbose_name=b'Category Description')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResumeCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=32, verbose_name=b'Category Description')),
                ('is_list', models.BooleanField(verbose_name=b'Is List')),
                ('order', models.IntegerField(verbose_name=b'Order')),
            ],
            options={
                'ordering': ['order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TalentProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stage_first_name', models.CharField(max_length=32, verbose_name=b'Stage First Name', blank=True)),
                ('stage_last_name', models.CharField(max_length=32, verbose_name=b'Stage Last Name', blank=True)),
                ('title', models.CharField(max_length=255, verbose_name=b'Title', blank=True)),
                ('height_feet', models.IntegerField(default=0, verbose_name=b'Height (Feet)')),
                ('height_inches', models.IntegerField(default=0, verbose_name=b'Height (Inches)')),
                ('weight', models.IntegerField(default=0, verbose_name=b'Weight')),
                ('birth_day', models.DateField(null=True, verbose_name=b'Birthday')),
                ('hair_color', models.CharField(max_length=32, verbose_name=b'Hair Color', blank=True)),
                ('eye_color', models.CharField(max_length=32, verbose_name=b'Eye Color', blank=True)),
                ('race', models.CharField(blank=True, max_length=1, verbose_name=b'Race', choices=[(b'E', b'Ethnic'), (b'R', b'Red-Headed')])),
                ('my_user', models.OneToOneField(to='um.MyUser')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='resumecategory',
            name='profile',
            field=models.ForeignKey(related_name=b'categories', to='talent.TalentProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='resumecategory',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='categorylistitem',
            name='category',
            field=models.ForeignKey(related_name=b'lists', to='talent.ResumeCategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='categorylistitem',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='categoryjob',
            name='category',
            field=models.ForeignKey(related_name=b'jobs', to='talent.ResumeCategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='categoryjob',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
