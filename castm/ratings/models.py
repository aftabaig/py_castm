import logging

from django.db import models
from forms.models import RatingForm, FormField
from organizations.models import Organization
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


class UserRating(models.Model):
    rating_form = models.ForeignKey(RatingForm)
    talent_user = models.ForeignKey(User, related_name="rating_talent_user")
    casting_user = models.ForeignKey(User, related_name="rating_casting_user")
    casting_organization = models.ForeignKey(Organization)
    rated_at = models.DateTimeField(auto_now_add=True, blank=True)

    @staticmethod
    def user_is_already_rated(talent_user, casting_user):
        q1 = models.Q(talent_user=talent_user)
        q2 = models.Q(casting_user=casting_user)
        return UserRating.objects.filter(q1 & q2).count() > 0


class UserRatingField(models.Model):
    rating = models.ForeignKey(UserRating)
    form_field = models.ForeignKey(FormField)
    field_value = models.CharField("Rating Value", max_length=64, blank=False)

    @staticmethod
    def user_field_ratings(talent_user, casting_user, field):
        q1 = models.Q(rating__talent_user=talent_user)
        q2 = models.Q(rating__casting_user=casting_user)
        q3 = models.Q(form_field=field)
        field_rating = UserRatingField.objects.filter(q1 & q2 & q3).first()
        if field_rating:
            return field_rating.field_value
        return ""


class PlainUserRatingField(object):
    def __init__(self, rating_id=None, form_field_id=None, form_field_value=None):
        self.rating_id = rating_id
        self.form_field_id = form_field_id
        self.form_field_value = form_field_value


# class UserOverallRating(object):
#     def __init__(self, talent_id=None, talent_first_name=None, talent_last_name=None, talent_title=None,
#                  talent_thumbnail_url=None, talent_profile_url=None,
#                  event_id=None, event_name=None):

