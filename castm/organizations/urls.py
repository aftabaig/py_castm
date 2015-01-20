from django.conf.urls import patterns, url

# views
from views import add_or_get_organizations, get_or_update_organization
from views import upload_logo, get_organization_members
from views import invite_user, accept_invitation, reject_invitation
from views import request_membership, accept_request, reject_request

urlpatterns = patterns(
    'organizations.views',
    url(r'^$', add_or_get_organizations),
    url(r'^(?P<organization_id>[0-9]+)/$', get_or_update_organization),
    url(r'^(?P<organization_id>[0-9]+)/members/$', get_organization_members),
    url(r'^(?P<organization_id>[0-9]+)/logo/$', upload_logo),
    url(r'^(?P<organization_id>[0-9]+)/invitations/$', invite_user),
    url(r'^(?P<organization_id>[0-9]+)/invitations/(?P<invitation_id>[0-9]+)/accept/$', accept_invitation),
    url(r'^(?P<organization_id>[0-9]+)/invitations/(?P<invitation_id>[0-9]+)/reject/$', reject_invitation),
    url(r'^(?P<organization_id>[0-9]+)/requests/$', request_membership),
    url(r'^(?P<organization_id>[0-9]+)/requests/(?P<request_id>[0-9]+)/accept/$', accept_request),
    url(r'^(?P<organization_id>[0-9]+)/requests/(?P<request_id>[0-9]+)/reject/$', reject_request),
)

