from django.db import models
from events.models import Event, EventOrganizationInfo
from organizations.models import Organization

from django.contrib.auth.models import User


class Callback(models.Model):
    event = models.ForeignKey(Event, related_name="event_callbacks")
    callback_organization = models.ForeignKey(Organization, related_name="callbacks")

    def plain(self):

        q1 = models.Q(event=self.event)
        q2 = models.Q(organization=self.callback_organization)
        organization_info = EventOrganizationInfo.objects.filter(q1 & q2).first()

        return PlainCallback(
            callback=self,
            callback_organization=self.callback_organization,
            organization_info=organization_info,
            event=self.event,
        )

    @staticmethod
    def organization_callback(organization, event):
        q1 = models.Q(callback_organization=organization)
        q2 = models.Q(event=event)
        return Callback.objects.filter(q1 & q2)

    @staticmethod
    def organization_callback_exists(organization, event):
        return Callback.organization_callback(organization, event).count() > 0


class CallbackTalent(models.Model):

    type_choices = (
        ('RCB', 'Regular Callback'),
        ('DCB', 'Dancer Callback'),
        ('HCB', 'Headshot/Resume Callback')
    )

    callback = models.ForeignKey(Callback, related_name="callback_talents")
    talent = models.ForeignKey(User, related_name="user_callback_talent")
    callback_type = models.CharField("Callback Type", max_length=3, choices=type_choices, blank=False)
    sent_to_event_organization = models.BooleanField(default=False)
    sent_to_talent = models.BooleanField(default=False)

    def plain(self):

        q1 = models.Q(event=self.callback.event)
        q2 = models.Q(organization=self.callback.callback_organization)
        organization_info = EventOrganizationInfo.objects.filter(q1 & q2).first()

        return PlainCallbackTalent(
            talent_callback_id=self.id,
            callback=self.callback,
            callback_organization=self.callback.callback_organization,
            organization_info=organization_info,
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
                 organization_info=None,
                 event=None):
        self.callback_id = callback.id
        self.callback_organization_id = callback_organization.id
        self.callback_organization_name = callback_organization.name
        self.callback_organization_logo_url = callback_organization.logo
        self.callback_location = organization_info.location
        self.callback_notes = organization_info.notes
        self.event_id = event.id
        self.event_name = event.name


class PlainCallbackTalent(object):
    def __init__(self, talent_callback_id=None,
                 callback=None,
                 callback_organization=None,
                 organization_info=None,
                 talent=None,
                 event=None,
                 ):
        self.talent_callback_id = talent_callback_id
        self.callback_id = callback.id
        self.callback_organization_id = callback_organization.id
        self.callback_organization_name = callback_organization.name
        self.callback_organization_logo_url = callback_organization.logo
        self.callback_type = callback.callback_type
        self.callback_location = organization_info.location
        self.callback_notes = organization_info.notes
        self.talent_id = talent.id
        self.talent_first_name = talent.first_name
        self.talent_last_name = talent.last_name
        self.talent_title = talent.user_profile.get().title
        self.talent_thumbnail_url = talent.user_profile.get().thumbnail
        self.talent_profile_url = "/api/talents/profile/%d" % (talent.id, )
        self.event_id = event.id
        self.event_name = event.name