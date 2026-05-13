from rest_framework import permissions
from rbac.permissions import user_has_role


class IsProjectOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow owners of a project or admins to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or user_has_role(request.user, 'ADMIN'):
            return True
        return obj.owner == request.user
