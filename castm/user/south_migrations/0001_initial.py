# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Consignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pickup_tenancy', models.CharField(max_length=255, verbose_name=b'Tenancy', blank=True)),
                ('pickup_street_num', models.CharField(max_length=255, verbose_name=b'Street #', blank=True)),
                ('pickup_street', models.CharField(max_length=255, verbose_name=b'Street', blank=True)),
                ('pickup_town', models.CharField(max_length=255, verbose_name=b'Town', blank=True)),
                ('pickup_postcode', models.CharField(max_length=255, verbose_name=b'Postcode', blank=True)),
                ('pickup_state', models.CharField(max_length=255, verbose_name=b'State', blank=True)),
                ('pickup_country', models.CharField(max_length=255, verbose_name=b'Country', blank=True)),
                ('delivery_tenancy', models.CharField(max_length=255, verbose_name=b'Tenancy', blank=True)),
                ('delivery_street_num', models.CharField(max_length=255, verbose_name=b'Street #', blank=True)),
                ('delivery_street', models.CharField(max_length=255, verbose_name=b'Street', blank=True)),
                ('delivery_town', models.CharField(max_length=255, verbose_name=b'Town', blank=True)),
                ('delivery_postcode', models.CharField(max_length=255, verbose_name=b'Postcode', blank=True)),
                ('delivery_state', models.CharField(max_length=255, verbose_name=b'State', blank=True)),
                ('delivery_country', models.CharField(max_length=255, verbose_name=b'Country', blank=True)),
                ('mode', models.CharField(max_length=64, verbose_name=b'Mode')),
                ('status', models.CharField(max_length=64, verbose_name=b'Status')),
                ('pickupDate', models.DateTimeField(default=datetime.datetime(2014, 10, 28, 1, 30, 25, 594087), verbose_name=b'Pickup Date')),
                ('eta_date', models.DateTimeField(default=datetime.datetime(2014, 10, 28, 1, 30, 25, 594118), verbose_name=b'ETA')),
                ('notes', models.CharField(max_length=512, verbose_name=b'Notes', blank=True)),
                ('customer_reference', models.CharField(max_length=255, verbose_name=b'Customer Reference', blank=True)),
                ('airway_bill_number', models.CharField(max_length=64, verbose_name=b'Airway Bill #', blank=True)),
            ],
            options={
                'ordering': ['-id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ConsignmentCharge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=255, verbose_name=b'Description')),
                ('quantity', models.CharField(max_length=10, verbose_name=b'Quantity')),
                ('cost', models.CharField(max_length=10, verbose_name=b'Cost')),
                ('consignment', models.ForeignKey(related_name=b'charges', default=0, to='api.Consignment')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ConsignmentItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=255, verbose_name=b'Description')),
                ('width', models.CharField(max_length=16, verbose_name=b'Width')),
                ('length', models.CharField(max_length=16, verbose_name=b'Length')),
                ('height', models.CharField(max_length=16, verbose_name=b'Height')),
                ('dead_weight', models.CharField(max_length=16, verbose_name=b'Dead Weight')),
                ('temp', models.CharField(max_length=16, verbose_name=b'Temp')),
                ('consignment', models.ForeignKey(related_name=b'items', default=0, to='api.Consignment')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ConsignmentSupply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.CharField(max_length=10, verbose_name=b'Amount')),
                ('consignment', models.ForeignKey(related_name=b'supplies', to='api.Consignment')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'Entity Name')),
                ('type', models.CharField(max_length=255, verbose_name=b'Type')),
                ('tenancy', models.CharField(max_length=255, verbose_name=b'Tenancy', blank=True)),
                ('street_num', models.CharField(max_length=255, verbose_name=b'Street #', blank=True)),
                ('street', models.CharField(max_length=255, verbose_name=b'Street', blank=True)),
                ('town', models.CharField(max_length=255, verbose_name=b'Town', blank=True)),
                ('postcode', models.CharField(max_length=255, verbose_name=b'Postcode', blank=True)),
                ('state', models.CharField(max_length=255, verbose_name=b'State', blank=True)),
                ('country', models.CharField(max_length=255, verbose_name=b'Country', blank=True)),
                ('email', models.EmailField(max_length=64, verbose_name=b'Email', blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EntityAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=255, verbose_name=b'Description')),
                ('entity', models.ForeignKey(related_name=b'accounts', to='api.Entity')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EntityRelationship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('relationship', models.CharField(max_length=255, verbose_name=b'Relationship')),
                ('entity', models.ForeignKey(related_name=b'relationships', default=0, to='api.Entity')),
                ('other', models.ForeignKey(related_name=b'other_relationships', to='api.Entity', max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'Name')),
            ],
            options={
                'ordering': ['-id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SearchCriterion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('criterion', models.CharField(max_length=255, verbose_name=b'Criteria')),
                ('criterion_value', models.CharField(max_length=255, verbose_name=b'Value')),
                ('search', models.ForeignKey(related_name=b'criteria', to='api.Search')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SearchField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'Field')),
                ('title', models.CharField(max_length=255, verbose_name=b'Title')),
                ('selected', models.BooleanField(default=True, verbose_name=b'Selected')),
                ('search', models.ForeignKey(related_name=b'fields', to='api.Search')),
            ],
            options={
                'ordering': ['id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Supply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=255, verbose_name=b'Description')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='consignmentsupply',
            name='supply',
            field=models.ForeignKey(to='api.Supply'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='consignment',
            name='account',
            field=models.ForeignKey(to='api.EntityAccount'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='consignment',
            name='consignee',
            field=models.ForeignKey(related_name=b'consignment_consignee', default=0, to='api.Entity'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='consignment',
            name='consignor',
            field=models.ForeignKey(related_name=b'consignment_consignor', default=0, to='api.Entity'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='consignment',
            name='originator',
            field=models.ForeignKey(related_name=b'consignment_originator', default=0, to='api.Entity'),
            preserve_default=True,
        ),
    ]
