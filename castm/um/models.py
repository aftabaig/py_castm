import datetime
import logging

# django
from django.db import models
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


class MyUser(models.Model):

    type_choices = (
        ('T', 'Talent'),
        ('C', 'Casting')
    )

    user = models.OneToOneField(User, related_name='user')
    type = models.CharField("Account Type", choices=type_choices, max_length=1, blank=False)
    sub_type = models.CharField("Account Sub Type", max_length=1, blank=True)

