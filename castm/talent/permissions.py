from um.permissions import IsTalent, IsCasting
from rest_framework.permissions import BasePermission
SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']


class IsTalentOrAnonymous(IsTalent):

    def has_permission(self, request, view, obj=None):
        is_talent = super(IsTalentOrAnonymous, self).has_permission(request, view)
        if is_talent or request.method in SAFE_METHODS:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        is_safe = request.method in SAFE_METHODS
        is_owner = (obj.my_user == request.user.id)
        return is_safe or is_owner



