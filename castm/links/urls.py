from django.conf.urls import patterns, url

# views
from views import my_links, my_talent_links, my_casting_links
from views import my_link_requests, send_link_request
from views import accept_link_request, reject_link_request
from views import search_links

urlpatterns = patterns(
    'links.views',
    url(r'^all/$', my_links),
    url(r'^talents/$', my_talent_links),
    url(r'^casting/$', my_casting_links),
    url(r'^search/$', search_links),
    url(r'^requests/$', my_link_requests),
    url(r'^(?P<user_id>[0-9]+)/send/$', send_link_request),
    url(r'^(?P<link_id>[0-9]+)/accept/$', accept_link_request),
    url(r'^(?P<link_id>[0-9]+)/reject/$', reject_link_request),
)
