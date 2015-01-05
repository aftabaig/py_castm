from django.conf.urls import patterns, url

# views
from views import my_notifications

urlpatterns = patterns(
    'notifications.views',
    url(r'^/$', my_notifications),
)
