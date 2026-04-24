from rest_framework import permissions

def user_has_role(user, role):
    if not user or not user.is_authenticated:
        return False
    if getattr(user, 'role', None) == 'ADMIN':
        return True
    if getattr(user, 'role', None) == role:
        return True
    return role in (getattr(user, 'roles', None) or [])


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return user_has_role(request.user, 'ADMIN')

class IsProjectOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return user_has_role(request.user, 'PROJECT_OWNER')

class IsContractor(permissions.BasePermission):
    def has_permission(self, request, view):
        return user_has_role(request.user, 'CONTRACTOR')

class IsVendorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return user_has_role(request.user, 'VENDOR')

class IsProjectOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return user_has_role(request.user, 'PROJECT_OWNER')

class IsVendor(permissions.BasePermission):
    def has_permission(self, request, view):
        return user_has_role(request.user, 'VENDOR')

class IsInvestor(permissions.BasePermission):
    def has_permission(self, request, view):
        return user_has_role(request.user, 'INVESTOR')

class IsGovernment(permissions.BasePermission):
    def has_permission(self, request, view):
        return user_has_role(request.user, 'GOVERNMENT')

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` or `user` attribute.
    """
    def has_object_permission(self, request, view, obj):
        if user_has_role(request.user, 'ADMIN'):
            return True
            
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check both 'owner' and 'user' fields common in this project
        owner = getattr(obj, 'owner', getattr(obj, 'user', None))
        return owner == request.user
