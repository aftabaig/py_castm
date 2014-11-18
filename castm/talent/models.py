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
    stage_first_name = models.CharField("Stage First Name", max_length=32, blank=True)
    stage_last_name = models.CharField("Stage Last Name", max_length=32, blank=True)
    title = models.CharField("Title", max_length=255, blank=True)
    height_feet = models.IntegerField("Height (Feet)", default=0)
    height_inches = models.IntegerField("Height (Inches)", default=0)
    weight = models.IntegerField("Weight", default=0)
    birth_day = models.DateField("Birthday", null=True, blank=True)
    hair_color = models.CharField("Hair Color", max_length=32, blank=True)
    eye_color = models.CharField("Eye Color", max_length=32, blank=True)
    race = models.CharField("Race", max_length=2, choices=race_choices, blank=True)
    resume_categories = models.TextField("Categories Dump", blank=True)


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
            self.stage_first_name = profile.stage_first_name
            self.stage_last_name = profile.stage_last_name
            self.title = profile.title
            self.height_feet = profile.height_feet
            self.height_inches = profile.height_inches
            self.weight = profile.weight
            self.birth_day = profile.birth_day
            self.hair_color = profile.hair_color
            self.eye_color = profile.eye_color
            self.race = profile.race
            self.resume_categories = profile.resume_categories
        if notification:
            self.notifications_count = notification.notifications_count
            self.links_count = notification.links_count
        else:
            self.notifications_count = 0
            self.links_count = 0




