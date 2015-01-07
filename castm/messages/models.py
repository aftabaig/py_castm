from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    from_user = models.ForeignKey(User, related_name="message_from", null=True)
    to_user = models.ForeignKey(User, related_name="message_to", null=True)
    message = models.CharField('Message', max_length=1024, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


