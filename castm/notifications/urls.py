from django.conf.urls import patterns, url

# views
from views import my_notifications
from views import my_links, my_link_requests
from views import accept_link_request, reject_link_request

urlpatterns = patterns(
    'notifications.views',
    url(r'^/$', my_notifications),
    url(r'^links/$', my_links),
    url(r'^links/requests/$', my_link_requests),
    url(r'^links/(?P<link_id>[0-9]+)/accept/$', accept_link_request),
    url(r'^links/(?P<link_id>[0-9]+)/reject/$', reject_link_request),
)
