import logging

from django.db import models
from django.contrib.auth.models import User
from links.models import Link
from my_messages.models import Message
from organizations.models import OrganizationMember
from callbacks.models import CallbackTalent

logger = logging.getLogger(__name__)


class Notification(models.Model):

    type_choices = (
        ('MSG', 'Message'),
        ('CB', 'Callback'),
        ('LR', 'Link Request'),
        ('LA', 'Link Accepted'),
        ('LD', 'Link Rejected'),
        ('OMI', 'Organization Membership Invitation'),
        ('OIA', 'Organization Invitation Accepted'),
        ('OIR', 'Organization Invitation Rejected'),
        ('OMR', 'Organization Membership Request'),
        ('ORA', 'Organization Request Accepted'),
        ('ORR', 'Organization Request Rejected'),
        ('ER', 'Event Attendance Request'),
        ('ERA', 'Event Request Accepted'),
        ('ERR', 'Event Request Rejected'),
    )

    type = models.CharField("Notification Type", choices=type_choices, max_length=3, blank=False)
    source_id = models.IntegerField("Notification Source Id", blank=False)
    from_user = models.ForeignKey(User, related_name="notification_from")
    for_user = models.ForeignKey(User, related_name="notification_for")
    message = models.CharField('Message', max_length=1024, blank=False)
    seen = models.BooleanField('Seen', default=False, blank=True)
    action_taken = models.BooleanField('Action taken?', default=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def plain(self):

        plain_notification = PlainNotification(
            notification_id=self.id,
            notification_type=self.type,
            created_at=self.created_at,
            user_id=self.from_user.id,
            first_name=self.from_user.first_name,
            last_name=self.from_user.last_name,
            description=self.message,
            source_id=self.source_id,
        )

        if self.from_user.my_user.type == 'T':
            plain_notification.title = self.from_user.user_profile.get().title
            plain_notification.thumbnail_url = self.from_user.user_profile.get().thumbnail
            plain_notification.profile_url = "/api/talents/profile/%d" % (self.from_user.id, )
        else:
            plain_notification.title = ""
            plain_notification.thumbnail_url = self.from_user.casting_profile.get().thumbnail
            plain_notification.profile_url = "/api/casting/profile/%d" % (self.from_user.id, )

        if self.type == 'LR' or self.type == 'LA' or self.type == 'LR':
            plain_notification.source = Link.objects.filter(id=self.source_id).first().plain()
        elif self.type == 'MSG':
            plain_notification.source = Message.objects.filter(id=self.source_id).first().plain()
        elif self.type == 'OMI' or self.type == 'OIA' or self.type == 'OIR' or self.type == 'OMR' or self.type == 'ORA' or self.type == 'ORR':
            logger.debug(self.source_id)
            plain_notification.source = OrganizationMember.objects.filter(id=self.source_id).first().plain()
        elif self.type == 'CB':
            plain_notification.source = CallbackTalent.objects.filter(id=self.source_id).first().plain()

        return plain_notification

    @staticmethod
    def unread_notifications(user, type):
        q1 = models.Q(for_user=user)
        q2 = models.Q(action_taken=False)
        q3 = models.Q(type=type)
        return Notification.objects.filter(q1 & q2 & q3)

    @staticmethod
    def unseen_notifications_count(user):
        q1 = models.Q(for_user=user)
        q2 = models.Q(seen=False)
        return Notification.objects.filter(q1 & q2).count()


class PlainNotification(object):
    def __init__(self, notification_id=None, source_id=None, notification_type=None, created_at=None, user_id=None, first_name=None, last_name=None, title=None, thumbnail_url=None, profile_url=None, description=None):
        self.notification_id = notification_id
        self.source_id = source_id
        self.notification_type = notification_type
        self.created_at = created_at
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.title = title
        self.thumbnail_url = thumbnail_url
        self.profile_url = profile_url
        self.description = description


class MyNotifications(object):
    def __init__(self, notifications=None):
        self.notifications = notifications


class NotificationSummary(object):
    def __init__(self):
        self.notifications_count = 0
        self.links_count = 0

    @staticmethod
    def get_notifications(user_id):
        user = User.objects.get(id=user_id)
        notification = NotificationSummary()
        notification.notifications_count = Notification.unseen_notifications_count(user)
        notification.links_count = Link.links_count(user)
        return notification


