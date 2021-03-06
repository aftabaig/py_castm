from django.conf.urls import patterns, url

# views
from views import get_events, my_events, user_attending_events, get_event
from views import all_talent_attendees, all_casting_attendees
from views import talent_event_info
from views import qualified_talent_attendees, qualified_casting_attendees
from views import pending_talent_attendees, pending_casting_attendees
from views import request_attendance, accept_request, reject_request
from schedules.views import get_talent_schedule
from my_messages.views import send_broadcast

urlpatterns = patterns(
    'events.views',
    url(r'^$', get_events),
    url(r'^my/$', my_events),
    url(r'^attending-events', user_attending_events),
    url(r'^(?P<event_id>[0-9]+)/$', get_event),
    url(r'^(?P<event_id>[0-9]+)/attendees/$', all_talent_attendees),
    url(r'^(?P<event_id>[0-9]+)/attendees/approved/$', qualified_talent_attendees),
    url(r'^(?P<event_id>[0-9]+)/attendees/pending/$', pending_talent_attendees),
    url(r'^(?P<event_id>[0-9]+)/attendees/(?P<talent_id>[0-9]+)/info/$', talent_event_info),
    url(r'^(?P<event_id>[0-9]+)/attendees/(?P<talent_id>[0-9]+)/schedule/$', get_talent_schedule),
    url(r'^(?P<event_id>[0-9]+)/casting/$', all_casting_attendees),
    url(r'^(?P<event_id>[0-9]+)/casting/approved/$', qualified_casting_attendees),
    url(r'^(?P<event_id>[0-9]+)/casting/pending/$', pending_casting_attendees),
    url(r'^(?P<event_id>[0-9]+)/requests/$', request_attendance),
    url(r'^(?P<event_id>[0-9]+)/requests/(?P<request_id>[0-9]+)/accept/$', accept_request),
    url(r'^(?P<event_id>[0-9]+)/requests/(?P<request_id>[0-9]+)/reject/$', reject_request),
    url(r'^(?P<event_id>[0-9]+)/broadcast/$', send_broadcast),
)

