from django.conf.urls import patterns, include, url
from rest_framework.routers import DefaultRouter

from views import RatingFormViewSet

forms = RatingFormViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'put': 'update',
})

router = DefaultRouter()
router.register(r'', RatingFormViewSet)

urlpatterns = patterns(
    'forms.views',
    url(r'', include(router.urls)),
)
