from django.conf.urls import patterns, url

# views
from views import public_profile
from views import ResumeCategoryView

urlpatterns = patterns(
    'talent.views',
    url(r'^profile/$', public_profile),
    url(r'^profile/(?P<user_id>[0-9]+)/$', public_profile),
    url(r'^resume/categories/$', ResumeCategoryView.as_view()),
)
