from django.conf.urls import patterns, url

# views
from views import organizations, members
from views import invite_user, accept_invitation, reject_invitation
from views import request_membership, accept_request, reject_request

urlpatterns = patterns(
    'organizations.views',
    url(r'^$', organizations),
    url(r'^(?P<organization_id>[0-9]+)/$', organizations),
    url(r'^(?P<organization_id>[0-9]+)/members/$', members),
    url(r'^(?P<organization_id>[0-9]+)/invitations/$', invite_user),
    url(r'^(?P<organization_id>[0-9]+)/invitations/(?P<invitation_id>[0-9]+)/accept/$', accept_invitation),
    url(r'^(?P<organization_id>[0-9]+)/invitations/(?P<invitation_id>[0-9]+)/reject/$', reject_invitation),
    url(r'^(?P<organization_id>[0-9]+)/requests/$', request_membership),
    url(r'^(?P<organization_id>[0-9]+)/requests/(?P<request_id>[0-9]+)/accept/$', accept_request),
    url(r'^(?P<organization_id>[0-9]+)/requests/(?P<request_id>[0-9]+)/reject/$', reject_request),
)

