from django.db import models
from events.models import Event
from organizations.models import Organization

from django.contrib.auth.models import User


class Callback(models.Model):
    event = models.ForeignKey(Event, related_name="event_callbacks")
    callback_organization = models.ForeignKey(Organization, related_name="callbacks")
    location = models.CharField("Callback Location", max_length=64, blank=False)
    schedule_date = models.DateField(blank=True, null=True)
    schedule_time_from = models.TimeField(blank=True, null=True)
    schedule_time_to = models.TimeField(blank=True, null=True)
    instructions_by_callback = models.CharField("Instructions by Callback Organization", max_length=1024, blank=True, null=True)
    instructions_by_event = models.CharField("Instructions by Callback Organization", max_length=1024, blank=True, null=True)

    def plain(self):
        return PlainCallback(
            callback=self,
            callback_organization=self.callback_organization,
            event=self.event,
        )

    @staticmethod
    def organization_callback(organization, event):
        q1 = models.Q(callback_ogranization=organization)
        q2 = models.Q(event=event)
        return Callback.objects.filter(q1 & q2)

    @staticmethod
    def organization_callback_exists(organization, event):
        return Callback.organization_callback(organization, event).count() > 0


class CallbackTalent(models.Model):
    callback = models.ForeignKey(Callback, related_name="callback_talents")
    talent = models.ForeignKey(User, related_name="user_callback_talent")
    sent_to_event_organization = models.BooleanField(default=False)
    sent_to_talent = models.BooleanField(default=False)

    def plain(self):
        return PlainCallbackTalent(
            talent_callback_id=self.id,
            callback=self.callback,
            callback_organization=self.callback.callback_organization,
            talent=self.talent,
            event=self.callback.event,
        )

    @staticmethod
    def callback_already_sent(talent, organization, event):
        q1 = models.Q(talent=talent)
        q2 = models.Q(callback__callback_organization=organization)
        q3 = models.Q(callback__event=event)
        return CallbackTalent.objects.filter(q1 & q2 & q3).count() > 0


    @staticmethod
    def organization_event_callbacks(organization, event):
        q1 = models.Q(callback__callback_organization=organization)
        q2 = models.Q(callback__event=event)
        return CallbackTalent.objects.filter(q1 & q2)


    @staticmethod
    def talent_event_callbacks(talent, event):
        q1 = models.Q(talent=talent)
        q2 = models.Q(callback__event=event)
        q3 = models.Q(sent_to_event_organization=True)
        q4 = models.Q(sent_to_talent=True)
        return CallbackTalent.objects.filter(q1 & q2 & q3 & q4)


class PlainCallback(object):
    def __init__(self,
                 callback=None,
                 callback_organization=None,
                 event=None):
        self.callback_id = callback.id
        self.callback_organization_id = callback_organization.id
        self.callback_organization_name = callback_organization.name
        self.callback_organization_logo_url = callback_organization.logo
        self.callback_location = callback.location
        self.callback_schedule_date = callback.schedule_date
        self.callback_schedule_time_from = callback.schedule_time_from
        self.callback_schedule_time_to = callback.schedule_time_to
        self.instructions_by_callback = callback.instructions_by_callback
        self.instructions_by_event = callback.instructions_by_event
        self.event_id = event.id
        self.event_name = event.name


class PlainCallbackTalent(object):
    def __init__(self, talent_callback_id=None,
                 callback=None,
                 callback_organization=None,
                 talent=None,
                 event=None,
                 ):
        self.talent_callback_id = talent_callback_id
        self.callback_id = callback.id
        self.callback_organization_id = callback_organization.id
        self.callback_organization_name = callback_organization.name
        self.callback_organization_logo_url = callback_organization.logo
        self.callback_location = callback.location
        self.callback_schedule_date = callback.schedule_date
        self.callback_schedule_time_from = callback.schedule_time_from
        self.callback_schedule_time_to = callback.schedule_time_to
        self.instructions_by_callback = callback.instructions_by_callback
        self.instructions_by_event = callback.instructions_by_event
        self.talent_id = talent.id
        self.talent_first_name = talent.first_name
        self.talent_last_name = talent.last_name
        self.talent_title = talent.user_profile.get().title
        self.talent_thumbnail_url = talent.user_profile.get().thumbnail
        self.talent_profile_url = "/api/talents/profile/%d" % (talent.id, )
        self.event_id = event.id
        self.event_name = event.name