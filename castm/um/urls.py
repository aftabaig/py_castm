from django.conf.urls import patterns, url
from views import sign_up
from views import authenticate
from views import change_password
from views import forgot_password

urlpatterns = patterns(
    'um.views',
    url(r'^register/$', sign_up),
    url(r'^authenticate/$', authenticate),
    url(r'^change-password/$', change_password),
    url(r'^forgot-password/$', forgot_password),
)
