from django.db import models
from forms.models import RatingForm, FormField
from django.contrib.auth.models import User


class UserRating(models.model):
    rating_form = models.ForeignKey(RatingForm)
    talent_user = models.ForeignKey(User)
    casting_user = models.ForeignKey(User)
    rated_at = models.DateTimeField(auto_now_add=True, blank=True)


class RatingItem(models.model):
    rating_field = models.ForeignKey(FormField)
    value = models.CharField("Rating Value", max_length=64, blank=False)


class PlainUserRating(object):
    def __init__(self, ):
