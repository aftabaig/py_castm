# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FieldItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256, verbose_name=b'Item Title')),
                ('value', models.CharField(max_length=256, verbose_name=b'Item Value')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FormField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=5, verbose_name=b'Field Type', choices=[(b'TXT', b'Text'), (b'MUL', b'Multiline'), (b'SCL', b'Scale'), (b'RAD', b'Radio Button'), (b'CHK', b'Checkbox'), (b'DRPD', b'Dropdown')])),
                ('title', models.CharField(max_length=1024, verbose_name=b'Field Title')),
                ('max_value', models.IntegerField(null=True, verbose_name=b'Max Value', blank=True)),
                ('use_stars', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RatingForm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('organization', models.ForeignKey(related_name=b'forms', to='organizations.Organization')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='formfield',
            name='form',
            field=models.ForeignKey(related_name=b'fields', to='forms.RatingForm'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fielditem',
            name='field',
            field=models.ForeignKey(related_name=b'items', to='forms.FormField'),
            preserve_default=True,
        ),
    ]
