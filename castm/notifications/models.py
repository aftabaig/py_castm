from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):

    type_choices = (
        ('MSG', 'Message'),
        ('CB', 'Callback'),
        ('LR', 'Link Request'),
        ('LA', 'Link Accepted'),
        ('LR', 'Link Rejected'),
    )

    type = models.CharField("Notification Type", choices=type_choices, max_length=3, blank=False)
    from_user = models.ForeignKey(User, related_name="notification_from")
    for_user = models.ForeignKey(User, related_name="notification_for")
    title = models.CharField('Notification Title', max_length=256, blank=False)
    message = models.CharField('Message', max_length=1024, blank=False)
    seen = models.BooleanField('Seen', default=False, blank=True)
    action_taken = models.BooleanField('Action taken?', default=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

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
    def __init__(self, notification_id=None, notification_type=None, created_at=None, user_id=None, first_name=None, last_name=None, title=None, description=None, thumbnail_url=None, profile_url=None):
        self.notification_id = notification_id
        self.notification_type = notification_type
        self.created_at = created_at
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.title = title
        self.description = description
        self.thumbnail_url = thumbnail_url
        self.profile_url = profile_url


class MyNotifications(object):
    def __init__(self, notifications=None):
        self.notifications = notifications

