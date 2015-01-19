from django.conf.urls import patterns, include, url
from rest_framework.routers import DefaultRouter

# views
from views import my_profile
from views import upload_thumbnail
from views import public_profile, public_headshots
from views import HeadshotViewSet

router = DefaultRouter()
router.register(r'headshots', HeadshotViewSet)


urlpatterns = patterns(
    'talent.views',
    url(r'^profile/$', my_profile),
    url(r'^profile/thumbnail/$', upload_thumbnail),
    url(r'^profile/(?P<user_id>[0-9]+)/$', public_profile),
    url(r'^(?P<user_id>[0-9]+)/headshots/$', public_headshots),
    url(r'', include(router.urls)),
)
