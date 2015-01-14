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
    push_token = models.CharField("Push Token", max_length=64, null=True, blank=True)
    type = models.CharField("Account Type", choices=type_choices, max_length=1, blank=False)
    sub_type = models.CharField("Account Sub Type", max_length=2, blank=True)

    @staticmethod
    def generate_activation_key(size=32, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

