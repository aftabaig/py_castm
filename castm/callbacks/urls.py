from django.conf.urls import patterns, url

# views
from views import schedules, single_schedule
from views import add_attendee, delete_attendee

urlpatterns = patterns(
    'callbacks.views',
    url(r'^$', schedules),
    url(r'^(?P<schedule_id>[0-9]+)/$', single_schedule),
    url(r'^(?P<schedule_id>[0-9]+)/attendees/$', add_attendee),
    url(r'^(?P<schedule_id>[0-9]+)/attendees/(?P<attendance_id>[0-9]+)/$', delete_attendee),
)



