from django.conf.urls import patterns, url

# views
from views import notifications_link_requests
from views import notifications_membership_requests
from views import notifications_callbacks
from views import notifications_messages
from views import mark_as_seen, action_taken

urlpatterns = patterns(
    'notifications.views',
    url(r'^link-requests/$', notifications_link_requests),
    url(r'^callbacks/$', notifications_callbacks),
    url(r'^messages/$', notifications_messages),
    url(r'^membership-requests', notifications_membership_requests),
    url(r'^seen/$', mark_as_seen),
    url(r'^(?P<link_id>[0-9]+)/responded/$', action_taken),

)
