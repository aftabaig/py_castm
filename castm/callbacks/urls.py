from django.conf.urls import patterns, url

# views
from views import get_callbacks, get_callback_detail
from views import add_talent_to_queue, remove_talent_from_queue
from views import send_callbacks_to_event_organization, send_callbacks_to_talent

urlpatterns = patterns(
    'callbacks.views',
    url(r'^$', get_callbacks),
    url(r'^(?P<talent_callback_id>[0-9]+)/$', get_callback_detail),
    url(r'^queue/$', add_talent_to_queue),
    url(r'^queue/(?P<talent_callback_id>[0-9]+)/$', remove_talent_from_queue),
    url(r'^send/$', send_callbacks_to_event_organization),
    url(r'^send-to-talent/$', send_callbacks_to_talent),
)



