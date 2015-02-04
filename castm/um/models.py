import datetime
import logging
import string
import random

# django
from django.db import models
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


class MyUser(models.Model):

    type_choices = (
        ('T', 'Talent'),
        ('C', 'Casting')
    )

    user = models.OneToOneField(User, related_name='my_user')
    activation_key = models.CharField("Activation Key", max_length=32)
    type = models.CharField("Account Type", choices=type_choices, max_length=1, blank=False)
    sub_type = models.CharField("Account Sub Type", max_length=2, blank=True)

    @staticmethod
    def generate_activation_key(size=32, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))


class UserDevice(models.Model):

    device_choices = (
        ('iOS', 'iOS'),
        ('Android', 'Android')
    )

    user = models.ForeignKey(User, related_name="user_devices")
    device_type = models.CharField("Device Type", choices=device_choices, max_length=8, blank=False)
    push_token = models.CharField("Push Token", max_length=64, null=True, blank=True)

    @staticmethod
    def get_user_device(user, device_type, push_token):
        q1 = models.Q(user=user)
        q2 = models.Q(device_type=device_type)
        q3 = models.Q(push_token=push_token)
        return UserDevice.objects.filter(q1 & q2 & q3).first()

