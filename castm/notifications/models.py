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
    for_user = models.ForeignKey(User, related_name="notification")
    title = models.CharField('Notification Title', max_length=256, blank=False)
    message = models.CharField('Message', max_length=1024, blank=False)
    seen = models.BooleanField('Seen', default=False, blank=True)
    action_taken = models.BooleanField('Action taken?', default=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    @staticmethod
    def unseen_notifications_count(user):
        q1 = models.Q(for_user=user)
        q2 = models.Q(seen=False)
        return Notification.objects.filter(q1 & q2).count()
