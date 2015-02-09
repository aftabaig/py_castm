#!/usr/bin/env python
# -*- coding: utf-8 -*-

from socket import gethostname
host_name = gethostname()

import os
if host_name == 'castm':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "production")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "development")

import sys
if host_name == 'castm':
    sys.path.append("/var/www/castm/py_castm/castm")
else:
    sys.path.append("/Users/aftabaig/Projects/Flash/Code/Backends/py_castm/castm")

import django
django.setup()

i=0
previous_email = ''
jobs = []

from subscriptions.models import PaymentPlan

import csv
with open('__plans__', 'rU') as csvfile:
    reader = csv.reader(csvfile)
    lines = list(reader)
    for plan_name, plan_title, plan_charges, plan_type, can_upgrade, can_downgrade in lines:
        plan = PaymentPlan()
        plan.plan_type = plan_type
        plan.name = plan_name
        plan.title = plan_title
        plan.charges = plan_charges
        plan.can_upgrade = can_upgrade
        plan.can_downgrade = can_downgrade
        plan.save()
