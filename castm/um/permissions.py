import logging

from rest_framework import permissions
from models import MyUser

logger = logging.getLogger(__name__)


class IsTalent(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        is_authenticated = super(IsTalent, self).has_permission(request, view)
        if not is_authenticated:
            return False
        my_user = MyUser.objects.get(user_id=request.user.id)
        return my_user.type == 'T'


class IsCasting(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        is_authenticated = super(IsCasting, self).has_permission(request, view)
        if not is_authenticated:
            return False
        my_user = MyUser.objects.get(user_id=request.user.id)
        return my_user.type == 'C'


class IsTalentOrCasting(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        is_authenticated = super(IsTalentOrCasting, self).has_permission(request, view)
        if not is_authenticated:
            return False
        my_user = MyUser.objects.get(user_id=request.user.id)
        return my_user.type == 'T' or my_user.type == 'C'
