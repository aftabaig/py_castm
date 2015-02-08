from django.db import models
from events.models import Event
from django.contrib.auth.models import User


class Schedule(models.Model):
    event = models.ForeignKey(Event, related_name="event_schedules")
    title = models.CharField("Schedule Title", max_length=64, blank=False)
    schedule_date = models.DateField(blank=False)
    schedule_time_from = models.TimeField(blank=False)
    schedule_time_to = models.TimeField(blank=False)
    sort_id = models.IntegerField(blank=True)

    def plain(self):
        plain_schedule = PlainSchedule(
            schedule_id=self.id,
            schedule_title=self.title,
            event_id=self.event.id,
            event_name=self.event.name,
            schedule_date=self.schedule_date,
            schedule_time_from="%s %s" % (self.schedule_date, self.schedule_time_from, ),
            schedule_time_to="%s %s" % (self.schedule_date, self.schedule_time_to, ),
            sort_id=self.sort_id
        )
        return plain_schedule


class ScheduleAttendee(models.Model):
    schedule = models.ForeignKey(Schedule, related_name="schedule_attendees")
    attendee = models.ForeignKey(User)
    attendee_unique_id = models.CharField("Unique Id", max_length=16, blank=True, null=True)

    def plain(self):
        return PlainScheduleAttendee(
            schedule_id=self.schedule.id,
            attendance_id=self.id,
            attendee_id=self.attendee.id,
            attendee_first_name=self.attendee.first_name,
            attendee_last_name=self.attendee.last_name,
            attendee_title=self.attendee.talent_profile.get().title,
            attendee_thumbnail_url=self.attendee.talent_profile.get().thumbnail,
            attendee_profile_url=""
        )

    @staticmethod
    def user_is_already_scheduled(user, event):
        q1 = models.Q(attendee=user)
        q2 = models.Q(schedule__event=event)
        return ScheduleAttendee.objects.filter(q1 & q2).count() > 0


class PlainSchedule(object):
    def __init__(self, schedule_id=None, schedule_title=None,
                 event_id=None, event_name=None,
                 schedule_date=None,
                 schedule_time_from=None, schedule_time_to=None,
                 sort_id=None,
                 attendees=None):
        self.schedule_id = schedule_id
        self.schedule_title = schedule_title
        self.event_id = event_id
        self.event_name = event_name
        self.schedule_date = schedule_date
        self.schedule_time_from = schedule_time_from
        self.schedule_time_to = schedule_time_to
        self.sort_id = sort_id
        self.attendees = attendees


class PlainScheduleAttendee(object):
    def __init__(self, schedule_id=None, attendance_id=None, attendee_id=None,
                 attendee_first_name=None, attendee_last_name=None, attendee_title=None,
                 attendee_profile_url=None, attendee_thumbnail_url=None):
        self.schedule_id = schedule_id
        self.attendance_id = attendance_id
        self.attendee_id = attendee_id
        self.attendee_first_name = attendee_first_name
        self.attendee_last_name = attendee_last_name
        self.attendee_title = attendee_title
        self.attendee_thumbnail_url = attendee_thumbnail_url
        self.attendee_profile_url = attendee_profile_url
