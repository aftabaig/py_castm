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

i = 0

from django.contrib.auth.models import User
from um.models import MyUser
from talent.models import TalentProfile, TalentHeadshot
from casting.models import CastingProfile
from organizations.models import Organization, OrganizationMember
from events.models import Event, EventAttendee, EventTalentInfo
from links.models import Link

# Step-1: Create a casting user with casting profile
# This will be "Matthew" who would be linked to all casting users.
matthew_user = User(email="matthew@castm.co", first_name="Matthew", last_name="Davenport", username="matthew@castm.co")
matthew_user.set_password("p@$$w0rd")
matthew_user.save()

# Step-1.1: Create associated my_user.
my_user = MyUser(user=matthew_user, type='C', activation_key='')
my_user.save()

# Step-1.2: Crate associated casting_profile.
casting_profile = CastingProfile(user=matthew_user, my_user=my_user)
casting_profile.save()

# Get reference to "SETC" event.
event = Event.objects.filter(name="SETC").first()
if not event:
    print "SETC event not found"
    sys.exit(0)

# Create organizations.
import csv
with open('data/__setc_organizations__', 'rU') as csvfile:
    reader = csv.reader(csvfile)
    lines = list(reader)
    for f0, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10 in lines:

        i += 1
        print ("%s/%s" % (i, lines.__len__()))

        org_name = f1
        org_add1 = f6
        org_add2 = f7
        org_city = f8
        org_state = f9
        org_zip = f10
        org_office = f5

        org = Organization()
        org.name = org_name
        org.add1 = org_add1
        org.add2 = org_add2
        org.city = org_city
        org.state = org_state
        org.zip = org_zip
        org.office = org_office
        org.save()

print "Organizations - DONE"
i = 0

# Create casting users.
with open('data/__setc_casting_users__', 'rU') as csvfile:
    reader = csv.reader(csvfile)
    lines = list(reader)
    for f0, f1, f2, f3, f4, f5, f6 in lines:

        i += 1
        print ("%s/%s" % (i, lines.__len__()))

        last_name = f1
        first_name = f2
        email = f3
        org_name = f4

        # Get the organization.
        org = Organization.objects.filter(name=org_name).first()
        if not org:
            print "Organization with name `%s` not found" % (org_name,)

        # Create user.
        casting_user = User(email=email, first_name=first_name, last_name=last_name, username=email)
        casting_user.set_password("p@$$w0rd")
        casting_user.save()

        # Create my_user.
        my_user = MyUser(user=casting_user, type='C', activation_key='')
        my_user.save()

        # Create user's casting profile.
        casting_profile = CastingProfile(user=casting_user, my_user=my_user)
        casting_profile.save()

        # Make the user, admin member of their respective organization.
        member = OrganizationMember(organization=org, initiator=casting_user, user=casting_user, role='ADM', is_accepted=True, is_rejected=False)
        member.save()

        # Make the casting user, an attendee of the "SETC" event.
        attendee = EventAttendee(event=event, organization=org, attendee=casting_user, is_accepted=True, is_rejected=False)
        attendee.save()

        # Link casting user to Matthew.
        link = Link(from_user=matthew_user, to_user=casting_user, optional_message="", is_accepted=True, is_rejected=False)
        link.save()

print "Casting Users - DONE"
i = 0





