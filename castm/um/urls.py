from django.conf.urls import patterns, url
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = patterns(
    'um.views',
    url(r'^register/$', 'sign_up'),
    url(r'^authenticate/$', obtain_auth_token),
    url(r'^change-password/$', 'change_password'),
    url(r'^forgot-password/$', 'forgot_password'),
)
