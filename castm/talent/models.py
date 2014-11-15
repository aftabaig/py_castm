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
    race = models.CharField("Race", max_length=1, choices=race_choices, blank=True)


class ResumeCategory(models.Model):
    user = models.ForeignKey(User)
    profile = models.ForeignKey(TalentProfile, related_name='categories')
    description = models.CharField("Category Description", max_length=32, blank=False)
    is_list = models.BooleanField("Is List", default=True)
    order = models.IntegerField("Order")

    class Meta:
        ordering = ['order']


class CategoryJob(models.Model):
    user = models.ForeignKey(User)
    category = models.ForeignKey(ResumeCategory, related_name='jobs')
    title = models.CharField("Title", max_length=32, blank=False)
    sub_title_1 = models.CharField("Sub Title 1", max_length=32, blank=False)
    sub_title_2 = models.CharField("Sub Title 2", max_length=32, blank=False)


class CategoryListItem(models.Model):
    user = models.ForeignKey(User)
    category = models.ForeignKey(ResumeCategory, related_name='lists')
    description = models.CharField("Category Description", max_length=32, blank=False)



