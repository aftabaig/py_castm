import logging

from django.db import models
from django.contrib.auth.models import User
from organizations.models import Organization
from organizations.models import OrganizationMember

logger = logging.getLogger(__name__)


class Event(models.Model):
    name = models.CharField("Event Name", max_length=64, blank=False)
    owner = models.ForeignKey(Organization, related_name="events")
    add1 = models.CharField("Address 1", max_length=1024, blank=True, null=True)
    add2 = models.CharField("Address 2", max_length=1024, blank=True, null=True)
    city = models.CharField("City", max_length=16, blank=True, null=True)
    state = models.CharField("State", max_length=16, blank=True, null=True)
    zip = models.CharField("Zip", max_length=16, blank=True, null=True)
    audition_start_date = models.DateField(auto_now_add=True)
    audition_end_date = models.DateField(auto_now_add=True)
    audition_time_from = models.TimeField()
    audition_time_to = models.TimeField()
    callback_start_date = models.DateField(auto_now_add=True)
    callback_end_date = models.DateField(auto_now_add=True)
    callback_time_from = models.TimeField()
    callback_time_to = models.TimeField()
    schedule_published = models.BooleanField(default=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    archived = models.BooleanField(default=False, blank=True)

    class Meta:
        ordering = ['-created_at']

    def plain(self):
        plain_event = PlainEvent(
            event_id=self.id,
            name=self.name,
            owner_id=self.owner.id,
            owner_name=self.owner.name,
            add1=self.add1,
            add2=self.add2,
            city=self.city,
            state=self.state,
            zip=self.zip,
            audition_start_date=self.audition_start_date,
            audition_end_date=self.audition_end_date,
            audition_time_from=self.audition_time_from,
            audition_time_to=self.audition_time_to,
            callback_start_date=self.callback_start_date,
            callback_end_date=self.callback_end_date,
            callback_time_from=self.callback_time_from,
            callback_time_to=self.callback_time_to,
            schedule_published=self.schedule_published,
        )
        return plain_event

    @staticmethod
    def talent_events(talent_user):
        """
        :return: All events being attended by the talent.
        """
        events = Event.objects.all()
        user_events = []
        for event in events:
            me = event.attendees.filter(attendee=talent_user).first()
            if me:
                user_events.append(event)
        return user_events

    @staticmethod
    def casting_events(casting_user):
        """
        :return: All events being attended by the organization to which the casting user is attached.
        """
        user_organization = OrganizationMember.user_organization(casting_user)
        if user_organization is None:
            return []
        events = Event.objects.all()
        user_events = []
        for event in events:
            me = event.attendees.filter(organization=user_organization).first()
            if me:
                user_events.append(event)
            # in case the user's organization is the
            # owner of the event.
            if user_organization == event.owner:
                user_events.append(event)
        return user_events


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
            attendee_first_name=self.attendee.first_name,
            attendee_last_name=self.attendee.last_name,
            is_accepted=self.is_accepted,
            is_rejected=self.is_rejected
        )
        if self.attendee.my_user.type == 'T':
            talent_info = EventTalentInfo.get_talent_info(self.event, self.attendee)
            if talent_info:
                plain_attendee.attendee_audition_id = talent_info.audition_id
            plain_attendee.attendee_title = self.attendee.user_profile.get().title
            plain_attendee.attendee_thumbnail_url = self.attendee.user_profile.get().thumbnail
            plain_attendee.attendee_profile_url = "/api/talents/profile/%d" % (self.attendee.id, )
        else:
            plain_attendee.attendee_title = self.attendee.casting_profile.get().title
            plain_attendee.attendee_thumbnail_url = self.attendee.casting_profile.get().thumbnail
            plain_attendee.attendee_profile_url = "/api/casting/profile/%d" % (self.attendee.id, )
            if self.organization:
                plain_attendee.organization_id = self.organization.id
                plain_attendee.organization_name = self.organization.name

        return plain_attendee

    def is_new(self):
        q1 = not self.is_accepted
        q2 = not self.is_rejected
        return q1 and q2

    @staticmethod
    def is_user_attending_event(user, event):
        q1 = models.Q(attendee=user)
        q2 = models.Q(event=event)
        q3 = models.Q(is_accepted=True)
        return EventAttendee.objects.filter(q1 & q2 & q3).count() > 0

    @staticmethod
    def is_organization_attending_event(organization, event):
        q1 = models.Q(organization=organization)
        q2 = models.Q(event=event)
        q3 = models.Q(is_accepted=True)
        return EventAttendee.objects.filter(q1 & q2 & q3).count() > 0

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
    def attendance_status(user, event):
        q = models.Q(event=event)
        if user.my_user.type == 'T':
            q = q & models.Q(attendee=user)
        else:
            organization = OrganizationMember.user_organization(user)
            if not organization:
                return 'NOL';
            q = q & models.Q(organization=organization)
        attendee = EventAttendee.objects.filter(q).first()
        if not attendee:
            return 'NOL'
        if attendee.is_accepted:
            return 'LNK'
        if attendee.is_rejected:
            return 'REJ'
        return 'PEND'

    @staticmethod
    def all_attendees(event, talents=True):
        q = models.Q(event=event)
        if talents:
            q = q & models.Q(organization__isnull=True)
        else:
            q = q & models.Q(organization__isnull=False)
        return EventAttendee.objects.filter(q)

    @staticmethod
    def qualified_attendees(event, talents=True):
        q = models.Q(event=event)
        q = q & models.Q(is_accepted=True)
        q = q & models.Q(is_rejected=False)
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


class EventTalentInfo(models.Model):
    event = models.ForeignKey(Event)
    talent = models.ForeignKey(User)
    audition_id = models.CharField("Audition #", max_length=16, blank=False)
    availability_date_start = models.DateField("Availability - Start", blank=True, null=True)
    availability_date_end = models.DateField("Availability - End", blank=True, null=True)
    availability_flexible = models.NullBooleanField("Is Flexible", blank=True, null=True)
    hiring_preferences = models.CharField("Hiring Preferences", max_length=1024, blank=True, null=True)

    def plain(self):
        return PlainEventTalentInfo(
            audition_id=self.audition_id,
            availability_date_start=self.availability_date_start,
            availability_date_end=self.availability_date_end,
            availability_flexible=self.availability_flexible,
            hiring_preferences=self.hiring_preferences
        )

    @staticmethod
    def get_talent_info(event, talent):
        return EventTalentInfo.objects.filter(event=event, talent=talent).first()


class EventOrganizationInfo(models.Model):
    event = models.ForeignKey(Event)
    organization = models.ForeignKey(Organization)
    location = models.CharField("Location", max_length=256, blank=True, null=True)
    notes = models.CharField("Notes", max_length=1024, blank=True, null=True)


class PlainEvent(object):
    def __init__(self, event_id=None, name=None, owner_id=None, owner_name=None,
                 add1=None, add2=None, city=None, state=None, zip=None,
                 audition_start_date=None, audition_end_date=None,
                 audition_time_from=None, audition_time_to=None,
                 callback_start_date=None, callback_end_date=None,
                 callback_time_from=None, callback_time_to=None,
                 schedule_published=None, my_attending_status=None):
        self.event_id = event_id
        self.name = name
        self.owner_id = owner_id
        self.owner_name = owner_name
        self.add1 = add1
        self.add2 = add2
        self.city = city
        self.state = state
        self.zip = zip
        self.audition_start_date = audition_start_date
        self.audition_end_date = audition_end_date
        self.audition_time_from = audition_time_from
        self.audition_time_to = audition_time_to
        self.callback_start_date = callback_start_date
        self.callback_end_date = callback_end_date
        self.callback_time_from = callback_time_from
        self.callback_time_to = callback_time_to
        self.schedule_published = schedule_published
        self.my_attending_status = my_attending_status


class PlainAttendee(object):
    def __init__(self, attendance_id=None, organization_id=None, organization_name=None,
                 attendee_id=None, attendee_audition_id=None,
                 attendee_first_name=None, attendee_last_name=None, attendee_title=None,
                 attendee_thumbnail_url=None, attendee_profile_url=None,
                 is_accepted=None, is_rejected=None):
        self.attendance_id = attendance_id
        self.organization_id = organization_id
        self.organization_name = organization_name
        self.attendee_id = attendee_id
        self.attendee_audition_id = attendee_audition_id
        self.attendee_first_name = attendee_first_name
        self.attendee_last_name = attendee_last_name
        self.attendee_title = attendee_title
        self.attendee_thumbnail_url = attendee_thumbnail_url
        self.attendee_profile_url = attendee_profile_url
        self.is_accepted = is_accepted
        self.is_rejected = is_rejected


class PlainEventTalentInfo(object):
    def __init__(self, audition_id=None, availability_date_start=None, availability_date_end=None, availability_flexible=None,
                 hiring_preferences=None):
        self.audition_id = audition_id
        self.availability_date_start = availability_date_start
        self.availability_date_end = availability_date_end
        self.availability_flexible = availability_flexible
        self.hiring_preferences = hiring_preferences
