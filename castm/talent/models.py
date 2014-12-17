import datetime
import logging

# django
from django.db import models
from um.models import MyUser

from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


class TalentProfile(models.Model):
    race_choices = (
        ('E', 'Ethnic'),
        ('R', 'Red-Headed'),
    )
    user = models.ForeignKey(User)
    my_user = models.OneToOneField(MyUser)
    is_stage_name = models.BooleanField("Stage Name?", blank=True, default=False)
    stage_first_name = models.CharField("Stage First Name", max_length=32, blank=True)
    stage_last_name = models.CharField("Stage Last Name", max_length=32, blank=True)
    title = models.CharField("Title", max_length=255, blank=True)
    height = models.CharField("Height", max_length=32, null=True, blank=True)
    weight = models.CharField("Weight", max_length=32, null=True, blank=True)
    birth_day = models.DateField("Birthday", null=True, blank=True)
    hair_color = models.CharField("Hair Color", max_length=32, blank=True)
    eye_color = models.CharField("Eye Color", max_length=32, blank=True)
    race = models.CharField("Race", max_length=2, choices=race_choices, blank=True)
    personal_add1 = models.CharField("Personal Address 1", max_length=1024, blank=True)
    personal_add2 = models.CharField("Personal Address 2", max_length=1024, blank=True)
    personal_mobile = models.CharField("Mobile #", max_length=32, blank=True)
    personal_office = models.CharField("Office #", max_length=32, blank=True)
    personal_email = models.CharField("Email Address", max_length=32, blank=True)
    is_agency_contact = models.BooleanField("Have an agent?", blank=True, default=False)
    agency = models.CharField("Agency", max_length=255, blank=True)
    agency_name = models.CharField("Agency Name", max_length=255, blank=True)
    agency_add1 = models.CharField("Agency Address 1", max_length=1024, blank=True)
    agency_add2 = models.CharField("Agency Address 2", max_length=1024, blank=True)
    resume_categories = models.TextField("Categories Dump", blank=True)


class TalentHeadshot(models.Model):
    user = models.ForeignKey(User)
    headshot = models.ImageField(upload_to='headshots')


class Notification(object):
    def __init__(self):
        self.notifications_count = 0
        self.links_count = 0

    @staticmethod
    def get_notifications(user_id):
        notification = Notification()
        notification.notifications_count = 5
        notification.links_count = 7
        return notification


class PlainProfile(object):
    def __init__(self, user=None, profile=None, notification=None):
        if user:
            self.user_id = user.id
            self.username = user.username
            self.email = user.email
            self.first_name = user.first_name
            self.last_name = user.last_name
        if profile:
            self.profile_id = profile.id
            self.is_stage_name = profile.is_stage_name
            self.stage_first_name = profile.stage_first_name
            self.stage_last_name = profile.stage_last_name
            self.title = profile.title
            self.height = profile.height
            self.weight = profile.weight
            self.birth_day = profile.birth_day
            self.hair_color = profile.hair_color
            self.eye_color = profile.eye_color
            self.race = profile.race
            self.personal_add1 = profile.personal_add1
            self.personal_add2 = profile.personal_add2
            self.personal_mobile = profile.personal_mobile
            self.personal_office = profile.personal_office
            self.personal_email = profile.personal_email
            self.is_agency_contact = profile.is_agency_contact
            self.agency = profile.agency
            self.agency_name = profile.agency_name
            self.agency_add1 = profile.agency_add1
            self.agency_add2 = profile.agency_add2
            self.resume_categories = profile.resume_categories
        if notification:
            self.notifications_count = notification.notifications_count
            self.links_count = notification.links_count
        else:
            self.notifications_count = 0
            self.links_count = 0




