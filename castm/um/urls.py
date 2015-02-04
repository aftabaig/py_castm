from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView
from views import sign_up
from views import authenticate, logout
from views import change_password
from views import forgot_password
from views import activate_user

urlpatterns = patterns(
    'um.views',
    url(r'^register/$', sign_up),
    url(r'^authenticate/$', authenticate),
    url(r'^logout/$', logout),
    url(r'^change-password/$', change_password),
    url(r'^forgot-password/$', forgot_password),
    url(r'^activate/(?P<activation_key>\w+)/$', activate_user),
)
