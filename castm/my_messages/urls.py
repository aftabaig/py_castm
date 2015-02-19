from django.conf.urls import patterns, url

# views
from views import send_message
from views import message_thread
from views import message_detail
from views import all_user_messages

urlpatterns = patterns(
    'messages.views',
    url(r'^send/$', send_message),
    url(r'^all/$', all_user_messages),
    url(r'^(?P<message_id>[0-9]+)/$', message_detail),
    url(r'^thread/(?P<user_id>[0-9]+)/$', message_thread),
)
