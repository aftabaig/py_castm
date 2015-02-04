from django.conf.urls import patterns, url

# views
from views import rate_user

urlpatterns = patterns(
    'rate.views',
    url(r'^(?P<talent_id>[0-9]+)/$', rate_user),
)
