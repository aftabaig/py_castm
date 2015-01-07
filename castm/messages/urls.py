from django.conf.urls import patterns, url

# views
from views import send_message
from views import my_link_requests, send_link_request
from views import accept_link_request, reject_link_request
from views import search_links

urlpatterns = patterns(
    'messages.views',
    url(r'^send/$', send_message),
    url(r'^thread/(?P<user_id>[0-9]+)/$', send_link_request),
)
