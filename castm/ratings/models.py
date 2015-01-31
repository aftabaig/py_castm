from django.db import models
from forms.models import RatingForm, FormField
from organizations.models import Organization
from django.contrib.auth.models import User


class UserRating(models.model):
    rating_form = models.ForeignKey(RatingForm)
    talent_user = models.ForeignKey(User)
    casting_user = models.ForeignKey(User)
    casting_organization = models.ForeignKey(Organization)
    rated_at = models.DateTimeField(auto_now_add=True, blank=True)

    @staticmethod
    def user_is_already_rated(talent_user, casting_user):
        q1 = models.Q(talent_user=talent_user)
        q2 = models.Q(casting_user=casting_user)
        return UserRating.objects.filter(q1 & q2).count() > 0


class UserRatingField(models.model):
    rating = models.ForeignKey(UserRating)
    form_field = models.ForeignKey(FormField)
    field_value = models.CharField("Rating Value", max_length=64, blank=False)


class UserOverallRating(object):
    def __init__(self, talent_id=None, talent_first_name=None, talent_last_name=None, talent_title=None,
                 talent_thumbnail_url=None, talent_profile_url=None,
                 event_id=None, event_name=None):

