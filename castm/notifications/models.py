from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    from_user = models.ForeignKey(User, related_name="from_message")
    to_user = models.ForeignKey(User, related_name="to_message")
    message = models.CharField('Message', max_length=1024, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Link(models.Model):
    from_user = models.ForeignKey(User, related_name="from_link")
    to_user = models.ForeignKey(User, related_name="to_link")
    optional_message = models.CharField('Optional Message', max_length=1024, blank=True)
    is_accepted = models.BooleanField('Is Accepted', default=False, blank=False)
    is_rejected = models.BooleanField('Is Rejected', default=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def is_already_link(user_1, user_2):
        q1 = models.Q(from_user=user_1)
        q2 = models.Q(to_user=user_1)
        q3 = models.Q(from_user=user_2)
        q4 = models.Q(to_user=user_2)
        link = Link.objects.filter((q1 & q4) | (q2 & q3)).first()
        return link is not None


    @staticmethod
    def user_links(user):
        q1 = models.Q(from_user=user)
        q2 = models.Q(to_user=user)
        q3 = models.Q(is_accepted=True)
        return Link.objects.filter((q1 | q2) & q3)


class Callback(models.Model):
    pass


class PlainLink(object):
    def __init__(self, id=None, first_name=None, last_name=None, title=None, profile_url=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.title = title
        self.profile_url = profile_url


class MyLinks(object):
    def __init__(self, talent_links=None, casting_links=None):
        self.talent_links = talent_links
        self.casting_links = casting_links