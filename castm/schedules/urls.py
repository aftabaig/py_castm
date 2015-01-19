from django.conf.urls import patterns, url

# views
from views import update_or_delete_schedule, get_or_add_schedules
from views import add_attendee, delete_attendee

urlpatterns = patterns(
    'schedules.views',
    url(r'^$', get_or_add_schedules),
    url(r'^(?P<schedule_id>[0-9]+)/$', update_or_delete_schedule),
    url(r'^(?P<schedule_id>[0-9]+)/attendees/$', add_attendee),
    url(r'^(?P<schedule_id>[0-9]+)/attendees/(?P<attendance_id>[0-9]+)/$', delete_attendee),
)


