# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersubscription',
            name='organization',
            field=models.OneToOneField(related_name=b'organization_subscription', null=True, blank=True, to='organizations.Organization'),
        ),
    ]
