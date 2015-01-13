from django.conf.urls import patterns, url

# views
from views import events, qualified_talent_attendees, qualified_casting_attendees
from views import pending_talent_attendees, pending_casting_attendees
from views import request_attendance, accept_request, reject_request

urlpatterns = patterns(
    'events.views',
    url(r'^$', events),
    url(r'^(?P<event_id>[0-9]+)/$', events),
    url(r'^(?P<event_id>[0-9]+)/attendees/$', qualified_talent_attendees),
    url(r'^(?P<event_id>[0-9]+)/attendees/pending/$', pending_talent_attendees),
    url(r'^(?P<event_id>[0-9]+)/casting/$', qualified_casting_attendees),
    url(r'^(?P<event_id>[0-9]+)/casting/pending/$', pending_casting_attendees),
    url(r'^(?P<event_id>[0-9]+)/requests/$', request_attendance),
    url(r'^(?P<event_id>[0-9]+)/requests/(?P<request_id>[0-9]+)/accept/$', accept_request),
    url(r'^(?P<event_id>[0-9]+)/requests/(?P<request_id>[0-9]+)/reject/$', reject_request),
)

