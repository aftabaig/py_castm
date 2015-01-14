from django.db import models
from events.models import Event
from organizations.models import Organization


class CallbackQueue(models.Model):
    event = models.ForeignKey(Event, related_name="event_queues")
    callback_organization = models.ForeignKey(Organization, related_name="callbacks")
    location = models.CharField("Callback Location", max_length=64, blan=False)
    schedule_date = models.DateField()
    schedule_time_from = models.TimeField()
    schedule_time_to = models.TimeField()



