from django.conf.urls import patterns, url

# views
from views import my_profile
from views import public_profile

urlpatterns = patterns(
    'talent.views',
    url(r'^profile/$', my_profile),
    url(r'^profile/(?P<user_id>[0-9]+)/$', public_profile),
)
