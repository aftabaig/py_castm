from django.conf.urls import patterns, url

# views
from views import notifications_link_requests
from views import notifications_callbacks
from views import notifications_messages

urlpatterns = patterns(
    'notifications.views',
    url(r'^link-requests/$', notifications_link_requests),
    url(r'^callbacks/$', notifications_callbacks),
    url(r'^messages/$', notifications_messages),
)
