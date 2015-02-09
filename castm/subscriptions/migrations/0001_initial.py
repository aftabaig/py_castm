# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_auto_20150121_0532'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('plan_type', models.CharField(max_length=1, verbose_name=b'Plan Type', choices=[(b'T', b'Talent'), (b'C', b'Casting')])),
                ('name', models.CharField(max_length=64, verbose_name=b'Plan Name')),
                ('title', models.CharField(max_length=128, verbose_name=b'Plan Title')),
                ('charges', models.FloatField(verbose_name=b'Charges /Month')),
                ('can_upgrade', models.BooleanField(default=False, verbose_name=b'Can Upgrade?')),
                ('can_downgrade', models.BooleanField(default=False, verbose_name=b'Can Downgrade?')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StripeEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stripe_event_id', models.CharField(max_length=64, verbose_name=b'Stripe Event Id')),
                ('stripe_event_type', models.CharField(max_length=64, verbose_name=b'Event Type')),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('user', models.ForeignKey(related_name=b'stripe_events', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserSubscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stripe_customer_id', models.CharField(max_length=128, verbose_name=b'Customer #')),
                ('stripe_subscription_id', models.CharField(max_length=128, verbose_name=b'Subscription #')),
                ('status', models.CharField(max_length=2, verbose_name=b'Payment Status', choices=[(b'AS', b'Active Subscription'), (b'US', b'Un-subscribed'), (b'FS', b'Failed Subscription'), (b'PN', b'Pending')])),
                ('organization', models.OneToOneField(related_name=b'organization_subscription', to='organizations.Organization')),
                ('plan', models.ForeignKey(to='subscriptions.PaymentPlan')),
                ('user', models.OneToOneField(related_name=b'subscription', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
