from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    from_user = models.ForeignKey(User, related_name="message_from", null=True)
    to_user = models.ForeignKey(User, related_name="message_to", null=True)
    title = models.CharField('Title', max_length=64, blank=False)
    message = models.CharField('Message', max_length=1024, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def plain(self):
        plain_msg = PlainMessage(
            msg_id=self.id,
            created_at=self.created_at,
            message=self.message,
            from_user_id=self.from_user.id,
            from_first_name=self.from_user.first_name,
            from_last_name=self.from_user.last_name,
            to_user_id=self.to_user.id,
            to_first_name=self.to_user.first_name,
            to_last_name=self.to_user.last_name,
        )
        if self.from_user.my_user.type == 'T':
            plain_msg.from_title = self.from_user.user_profile.get().title
            plain_msg.from_thumbnail_url = self.from_user.user_profile.get().thumbnail
            plain_msg.from_profile_url = "/api/talents/profile/%d" % (self.from_user.id, )
        else:
            plain_msg.from_title = ""
            # plain_msg.from_thumbnail_url = self.from_user.casting_profile.get().thumbnail
            # plain_msg.from_profile_url = "/api/casting/profile/%d" % (self.from_user.id, )
        if self.to_user.my_user.type == 'T':
            plain_msg.to_title = self.to_user.user_profile.get().title
            plain_msg.to_thumbnail_url = self.to_user.user_profile.get().thumbnail
            plain_msg.to_profile_url = "/api/talents/profile/%d" % (self.to_user.id, )
        else:
            plain_msg.to_title = "",
            # plain_msg.to_thumbnail_url = self.to_user.casting_profile.get().thumbnail
            # plain_msg.to_profile_url = "/api/casting/profile/%d" % (self.to_user.id, )
        return plain_msg

    @staticmethod
    def thread(user1, user2):

        q1 = models.Q(from_user=user1)
        q2 = models.Q(to_user=user2)
        q3 = models.Q(from_user=user2)
        q4 = models.Q(to_user=user1)
        return Message.objects.filter((q1 & q2) | (q3 & q4)).order_by('-created_at')


class PlainMessage(object):
    def __init__(self, msg_id=None, created_at=None, title=None, message=None,
                 from_user_id=None, from_first_name=None, from_last_name=None, from_title=None, from_thumbnail_url=None, from_profile_url=None,
                 to_user_id=None, to_first_name=None, to_last_name=None, to_title=None, to_thumbnail_url=None, to_profile_url=None):
        self.msg_id = msg_id
        self.created_at = created_at
        self.title = title
        self.message = message
        self.from_user_id = from_user_id
        self.from_first_name = from_first_name
        self.from_last_name = from_last_name
        self.from_title = from_title
        self.from_thumbnail_url = from_thumbnail_url
        self.from_profile_url = from_profile_url
        self.to_user_id = to_user_id
        self.to_first_name = to_first_name
        self.to_last_name = to_last_name
        self.to_title = to_title
        self.to_thumbnail_url = to_thumbnail_url
        self.to_profile_url = to_profile_url

class MyLinks(object):
    def __init__(self, links=None):
        self.links = links




