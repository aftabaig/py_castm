from django.db import models
from django.contrib.auth.models import User

from notifications.models import Notification


class Link(models.Model):

    from_user = models.ForeignKey(User, related_name="from_link")
    to_user = models.ForeignKey(User, related_name="to_link")
    notification = models.ForeignKey(Notification, related_name="link")
    optional_message = models.CharField('Optional Message', max_length=1024, blank=True)
    is_accepted = models.BooleanField('Is Accepted', default=False, blank=False)
    is_rejected = models.BooleanField('Is Rejected', default=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def plain(self, user=None):

        plain_link = PlainLink(
            link_id=self.id,
            link_type="T",
            user_id=self.to_user.id,
            first_name=self.to_user.first_name,
            last_name=self.to_user.last_name,
            title=self.to_user.user_profile.get().title,
            thumbnail_url=self.to_user.user_profile.get().thumbnail,
            profile_url="/api/talents/profile/%d" % (self.to_user.id, ),
        )

        if user:
            if self.is_accepted:
                plain_link.link_status = "F"
            else:
                if self.from_user == user:
                    if self.is_rejected:
                        plain_link.link_status = "RH"
                    else:
                        plain_link.link_status = "PH"
                else:
                    if self.is_rejected:
                        plain_link.link_status = "RY"
                    else:
                        plain_link.link_status = "PY"

        return plain_link

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

    @staticmethod
    def links_count(user):
        return Link.user_links(user).count()

    @staticmethod
    def talent_links(user):
        q1 = models.Q(from_user=user)
        q2 = models.Q(to_user=user)
        q3 = models.Q(is_accepted=True)
        q4 = models.Q(from_user__my_user__type__startswith='T')
        return Link.objects.filter((q1 | q2) & q3 & q4)

    @staticmethod
    def casting_links(user):
        q1 = models.Q(from_user=user)
        q2 = models.Q(to_user=user)
        q3 = models.Q(is_accepted=True)
        q4 = models.Q(from_user__my_user__type__startswith='C')
        return Link.objects.filter((q1 | q2) & q3 & q4)

    @staticmethod
    def link_requests(user):
        q1 = models.Q(to_user=user)
        q2 = models.Q(is_accepted=False)
        q3 = models.Q(is_rejected=False)
        return Link.objects.filter(q1 & q2 & q3)


class PlainLink(object):
    def __init__(self, link_id=None, link_type=None, created_at=None, user_id=None, first_name=None, last_name=None, title=None, thumbnail_url=None, profile_url=None, link_status=None):
        self.link_id = link_id
        self.link_type = link_type
        self.created_at = created_at
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.title = title
        self.thumbnail_url = thumbnail_url
        self.profile_url = profile_url
        self.link_status = link_status


class MyLinks(object):
    def __init__(self, links=None):
        self.links = links