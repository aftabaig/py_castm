import datetime
import logging

# django
from django.db import models
from um.models import MyUser
from links.models import Link
from notifications.models import Notification

from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


class CastingProfile(models.Model):
    user = models.ForeignKey(User, related_name="casting_profile")
    my_user = models.OneToOneField(MyUser)
    add1 = models.CharField("Address 1", max_length=1024, blank=True)
    add2 = models.CharField("Address 2", max_length=1024, blank=True)
    city = models.CharField("City", max_length=16, blank=True)
    state = models.CharField("State", max_length=16, blank=True)
    zip = models.CharField("Zip", max_length=16, blank=True)
    mobile = models.CharField("Mobile #", max_length=32, blank=True)
    office = models.CharField("Office #", max_length=32, blank=True)
    thumbnail = models.CharField("Thumbnail", max_length=255, blank=True)


class CastingHeadshot(models.Model):
    user = models.ForeignKey(User)
    headshot = models.ImageField(upload_to='headshots')


class PlainProfile(object):
    def __init__(self, user=None, profile=None, notification=None, organization=None, invitation=None):
        if user:
            self.user_id = user.id
            self.username = user.username
            self.email = user.email
            self.first_name = user.first_name
            self.last_name = user.last_name
        if profile:
            self.sub_type = profile.my_user.sub_type
            self.profile_id = profile.id
            self.add1 = profile.add1
            self.add2 = profile.add2
            self.city = profile.city
            self.state = profile.state
            self.zip = profile.zip
            self.mobile = profile.mobile
            self.office = profile.office
            self.thumbnail = profile.thumbnail
        if organization:
            self.organization = organization
        else:
            self.organization = None
        if invitation:
            self.invitation = invitation
        else:
            self.invitation = None
        if notification:
            self.notifications_count = notification.notifications_count
            self.links_count = notification.links_count
        else:
            self.notifications_count = 0
            self.links_count = 0




