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

# Get reference to "Matthew".
matthew_user, created = User.objects.get_or_create(email="matthew@castm.co")
matthew_user.username = "matthew@castm.co"
matthew_user.first_name = "Matthew"
matthew_user.last_name = "Davenport"
matthew_user.set_password("p@$$w0rd")
matthew_user.save()

# Get reference to "SETC 2016" event.
event = Event.objects.get(name="SETC 2016")

i = 0

# Create casting users.
import csv
with open('data/__setc_casting_users_2016__.csv', 'rU') as csvfile:
    reader = csv.reader(csvfile)
    lines = list(reader)
    for f0, f1, f2, f3 in lines:

        i += 1
        print ("%s/%s" % (i, lines.__len__()))

        last_name = f0
        first_name = f1
        email = f2
        org_name = f3

        print (last_name)
        print (first_name)
        print (email)
        print (org_name)

        # Get the organization.
        org, created = Organization.objects.get_or_create(name=org_name)
        org.save()

        # Create/Update user.
        casting_user, created = User.objects.get_or_create(username=email)
        casting_user.email = email
        casting_user.first_name = first_name
        casting_user.last_name = last_name
        casting_user.set_password("p@$$w0rd")
        casting_user.save()

        # Create/Update my_user.
        my_user, created = MyUser.objects.get_or_create(user=casting_user)
        my_user.type = 'C'
        my_user.activation_key = ''
        my_user.save()

        # Create user's casting profile.
        casting_profile, created = CastingProfile.objects.get_or_create(user=casting_user, my_user=my_user)
        casting_profile.save()

        # Make the user, admin member of their respective organization.
        member, created = OrganizationMember.objects.get_or_create(organization=org, initiator=casting_user, user=casting_user)
        member.role = 'ADM'
        member.is_accepted = True
        member.is_rejected = False
        member.save()

        # Make the casting user, an attendee of the "SETC 2016" event.
        attendee, created = EventAttendee.objects.get_or_create(event=event, organization=org, attendee=casting_user)
        attendee.is_accepted = True
        attendee.is_rejected = False
        attendee.save()

        # Link casting user to Matthew.
        link, created = Link.objects.get_or_create(from_user=matthew_user, to_user=casting_user)
        link.optional_message = ""
        link.is_accepted = True
        link.is_rejected = False
        link.save()

print "Casting Users - DONE"
i = 0
