import logging

from django.db import models
from django.contrib.auth.models import User
from organizations.models import Organization
from organizations.models import OrganizationMember

logger = logging.getLogger(__name__)


class Event(models.Model):
    name = models.CharField("Event Name", max_length=64, blank=False)
    owner = models.ForeignKey(Organization, related_name="events")
    audition_date = models.DateField(auto_now_add=True)
    audition_time_from = models.TimeField()
    audition_time_to = models.TimeField()
    callback_date = models.DateField(auto_now_add=True)
    callback_time_from = models.TimeField()
    callback_time_to = models.TimeField()

    def plain(self):
        plain_event = PlainEvent(
            event_id=self.id,
            name=self.name,
            owner_id=self.owner.id,
            owner_name=self.owner.name,
            audition_date=self.audition_date,
            audition_time_from=self.audition_time_from,
            audition_time_to=self.audition_time_to,
            callback_date=self.callback_date,
            callback_time_from=self.callback_time_from,
            callback_time_to=self.callback_time_to,
        )
        return plain_event


class EventAttendee(models.Model):
    event = models.ForeignKey(Event, related_name="attendees")
    organization = models.ForeignKey(Organization, null=True, blank=True)
    attendee = models.ForeignKey(User)
    is_accepted = models.BooleanField('Is Accepted', default=False, blank=False)
    is_rejected = models.BooleanField('Is Rejected', default=False, blank=False)

    def plain(self):
        plain_attendee = PlainAttendee(
            attendance_id=self.id,
            attendee_id=self.attendee.id,
            organization_id=self.organization.id,
            organization_name=self.organization.name,
            attendee_first_name=self.attendee.first_name,
            attendee_last_name=self.attendee.last_name,
            is_accepted=self.is_accepted,
            is_rejected=self.is_rejected
        )
        if self.attendee.my_user.type == 'T':
            plain_attendee.attendee_title = self.attendee.user_profile.get().title
            plain_attendee.attendee_thumbnail_url = self.attendee.user_profile.get().thumbnail[0]
            plain_attendee.attendee_profile_url = "/api/talents/profile/%d" % (self.attendee.id, )
        else:
            plain_attendee.attendee_title = ""
            # plain_attendee.attendee_thumbnail_url = self.attendee.casting_profile.get().thumbnail
            # plain_attendee.attendee_profile_url = "/api/casting/profile/%d" % (self.attendee.id, )

        return plain_attendee

    def is_new(self):
        q1 = not self.is_accepted
        q2 = not self.is_rejected
        return q1 and q2

    @staticmethod
    def user_is_already_attending(user, event):
        q = models.Q(event=event)
        if user.my_user.type == 'T':
            q = q & models.Q(attendee=user)
        else:
            organization = OrganizationMember.user_organization(user)
            q = q & models.Q(organization=organization)
        return EventAttendee.objects.filter(q).count() > 0

    @staticmethod
    def qualified_attendees(event, talents=True):
        q = models.Q(event=event)
        logger.debug("1")
        q = q & models.Q(is_accepted=True)
        logger.debug("2")
        q = q & models.Q(is_rejected=False)
        logger.debug("3")
        if talents:
            q = q & models.Q(organization__isnull=True)
        else:
            q = q & models.Q(organization__isnull=False)
        logger.debug(EventAttendee.objects.filter(q))
        return EventAttendee.objects.filter(q)

    @staticmethod
    def pending_attendees(event, talents=True):
        q = models.Q(event=event)
        q = q & models.Q(is_accepted=False)
        q = q & models.Q(is_rejected=False)
        if talents:
            q = q & models.Q(organization__isnull=True)
        else:
            q = q & models.Q(organization__isnull=False)
        return EventAttendee.objects.filter(q)


class PlainEvent(object):
    def __init__(self, event_id=None, name=None, owner_id=None, owner_name=None,
                 audition_date=None, audition_time_from=None, audition_time_to=None,
                 callback_date=None, callback_time_from=None, callback_time_to=None):
        self.event_id = event_id
        self.name = name
        self.owner_id = owner_id
        self.owner_name = owner_name
        self.audition_date = audition_date
        self.audition_time_from = audition_time_from
        self.audition_time_to = audition_time_to
        self.callback_date = callback_date
        self.callback_time_from = callback_time_from
        self.callback_time_to = callback_time_to


class PlainAttendee(object):
    def __init__(self, attendance_id=None, organization_id=None, organization_name=None,
                 attendee_id=None, attendee_first_name=None, attendee_last_name=None, attendee_title=None,
                 attendee_thumbnail_url=None, attendee_profile_url=None,
                 is_accepted=None, is_rejected=None):
        self.attendance_id = attendance_id
        self.organization_id = organization_id
        self.organization_name = organization_name
        self.attendee_id = attendee_id
        self.attendee_first_name = attendee_first_name
        self.attendee_last_name = attendee_last_name
        self.attendee_title = attendee_title
        self.attendee_thumbnail_url = attendee_thumbnail_url
        self.attendee_profile_url = attendee_profile_url
        self.is_accepted = is_accepted
        self.is_rejected = is_rejected