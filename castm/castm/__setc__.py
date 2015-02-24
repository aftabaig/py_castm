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

from django.contrib.auth.models import User
from um.models import MyUser
from talent.models import TalentProfile, TalentHeadshot
from casting.models import CastingProfile
from organizations.models import Organization, OrganizationMember
from events.models import Event, EventAttendee, EventTalentInfo

# Step-1: Create a casting user with casting profile
# This user will be the member of "SETC" organization
# that we create below.
casting_user = User(email="april@setc.org", first_name="April J'Callahan", last_name="Marshall", username="april@setc.org")
casting_user.set_password("p@$$w0rd")
casting_user.save()

# Step-1.1: Create associated my_user.
my_user = MyUser(user=casting_user, type='C', activation_key='')
my_user.save()

# Step-1.2: Crate associated casting_profile.
casting_profile = CastingProfile(user=casting_user, my_user=my_user)
casting_profile.save()

# Step-2: Create "SETC" organization.
# This organization will be the owner of the "SETC" event
# that we create below.
organization = Organization(name="SETC")
organization.save()

# Step-3: Create an admin member of the "SETC" organization
member = OrganizationMember(organization=organization, initiator=casting_user, user=casting_user, role='ADM', is_accepted=True, is_rejected=False)
member.save()

# Step-4 Create "SETC" event
event = Event(name="SETC", owner=organization)
event.audition_start_date = "2015-03-04"
event.audition_end_date = "2015-03-08"
event.audition_time_from = "12:00"
event.audition_time_to = "20:00"
event.callback_start_date = "2015-03-04"
event.callback_end_date = "2015-03-08"
event.callback_time_from = "12:00"
event.callback_time_to = "20:00"
event.save()

import csv
with open('__data__', 'rU') as csvfile:
    reader = csv.reader(csvfile)
    lines = list(reader)
    for f0, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13, f14, f15, f16, f17, f18, f19, f20, f21, f22, f23, f24, f25, f26, f27, f28, f29, f30, f31, f32, f33, f34, f35, f36, f37, f38, f39, f40, f41, f42 in lines:

        audition_num = f0
        first_name = f2
        middle_name = f3
        last_name = f4
        street_address = f5
        city = f6
        state = f7
        zip = f8
        phone = f9
        email = f10
        dob = f11
        gender = f12
        begin_avail = f13
        end_avail = f14
        dates_flexible = f15
        work_preferences = f16
        height = f18
        weight = f19
        hair_color = f20
        eye_color = f21
        picture_file = f26
        play_show = f32
        role = f33
        producing_organization = f35

        # This condition will be true every time
        # a new email address is encountered.
        if previous_email != email:

                i += 1

                # This is the block where we add resume category jobs
                # to the last user we had in the loop.
                # The idea is to collect jobs in the loop and when
                # the email address changes, we assign all those jobs
                # to the previous email.
                # The inner condition is there because with the
                # outer condition, we get a null in the previous_email
                # for the first time in the loop.
                if previous_email:
                    resume_categories = {
                        "resume_categories": [
                            {
                                "title": "RESUME",
                                "jobs": jobs
                            }
                        ]
                    }

                    # Update user's resume.
                    u = User.objects.filter(email=previous_email)
                    profile = TalentProfile.objects.filter(user=u).first()
                    profile.resume_categories = str(resume_categories)
                    profile.save()

                    jobs = []

                import cloudinary
                import cloudinary.uploader
                import cloudinary.api
                try:
                    url = "http://setc.matchingneeds.com/inf/images/om/%s" % (picture_file, )
                    response = cloudinary.uploader.upload(url)
                except:
                    response = {}

                # Create user.
                user = User(email=email, first_name=first_name, last_name=last_name, username=email)
                user.set_password("p@$$w0rd")
                user.save()

                # Create my_user.
                my_user = MyUser(user=user, type='T', activation_key='')
                my_user.save()

                # Create user's profile.
                profile = TalentProfile(user=user, my_user=my_user)
                profile.personal_add1 = street_address
                profile.personal_city = city
                profile.personal_state = state
                profile.personal_zip = zip
                profile.personal_mobile = phone
                profile.personal_email = email
                profile.height = height
                profile.weight = weight
                profile.hair_color = hair_color
                profile.eye_color = eye_color
                profile.gender = gender[0]
                profile.birth_day = dob.replace(", ", "-")
                if response:
                    profile.thumbnail = response["url"]
                profile.save()

                # Create headshot.
                if response:
                    headshot = TalentHeadshot(user=user)
                    headshot.headshot = response["url"]
                    headshot.save()

                # Make the talent, an attendee of the "SETC" event.
                attendee = EventAttendee(event=event, attendee=user, is_accepted=True, is_rejected=False)
                attendee.save()

                # Store talent's event related info.
                info = EventTalentInfo(event=event, talent=user, audition_id=audition_num)
                date_parts = begin_avail.split('/')
                info.availability_date_start = "20%s-%s-%s" % (date_parts[2], date_parts[0], date_parts[1], )
                date_parts = end_avail.split('/')
                info.availability_date_end = "20%s-%s-%s" % (date_parts[2], date_parts[0], date_parts[1], )
                info.availability_flexible = dates_flexible
                info.hiring_preferences = work_preferences
                info.save()

                print i

        # We collect the job and store it in
        # the jobs array. The jobs array will
        # contain the jobs of a user.
        # when the user (email address) changes,
        # we store these jobs to user's profile (as described above)
        # and empty the jobs array.
        job = {
            'title': play_show,
            'detail1': role,
            'detail2': producing_organization
        }
        jobs.append(job)

        previous_email = email

