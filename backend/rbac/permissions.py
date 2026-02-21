from rest_framework import permissions
from django.contrib.auth.models import Group

class HasRequiredPermission(permissions.BasePermission):
    """
    Generic permission check against the logical namespace system.
    Usage:
    permission_classes = [HasRequiredPermission]
    required_permission = 'contracts:post_contract'
    """
    def has_permission(self, request, view):
        # Allow read-only access for unauthenticated users (Public Marketplace)
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user or not request.user.is_authenticated:
            return False
        
        # Superuser has all permissions
        if request.user.is_superuser:
            return True

        permission_map = getattr(view, 'permission_map', {})
        action = getattr(view, 'action', None)
        
        required_perm = permission_map.get(action)
        if not required_perm:
            required_perm = getattr(view, 'required_permission', None)

        if not required_perm:
            return True

        # Map 'contracts:post_contract' to 'rbac.contracts_post_contract'
        app_label = 'rbac'
        codename = required_perm.replace(':', '_')
        perm_string = f"{app_label}.{codename}"
        
        return request.user.has_perm(perm_string)

class IsOrganizationAdmin(permissions.BasePermission):
    """
    Scoped permission for Phase 5 Enterprise Org admins.
    Checks if user is member of the organization they are trying to manage.
    """
    def has_object_permission(self, request, view, obj):
        # Implementation depends on Organization models existing
        # return obj.admins.filter(id=request.user.id).exists()
        return True # Placeholder for logic expansion

class IsVendorOwner(permissions.BasePermission):
    """
    Checks if the user is the owner of the vendor profile for the object.
    Works for Product and Order models.
    """
    def has_object_permission(self, request, view, obj):
        if not hasattr(request.user, 'vendor_profile'):
            return False
        
        vendor = request.user.vendor_profile
        # If object is a Product
        if hasattr(obj, 'vendor'):
            return obj.vendor == vendor
        # If object is a Vendor profile itself
        if hasattr(obj, 'user'):
            return obj.user == request.user
            
        return False

class VendorApprovedOnly(permissions.BasePermission):
    """
    Checks if the vendor is approved.
    """
    def has_permission(self, request, view):
        if not hasattr(request.user, 'vendor_profile'):
            return False
        return request.user.vendor_profile.verified_status == 'APPROVED'

class IsBuyer(permissions.BasePermission):
    """
    Checks if the user has a role that can act as a buyer.
    In Phase 1, PROJECT_OWNER and CONTRACTOR are primary buyers.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role in ['PROJECT_OWNER', 'CONTRACTOR', 'ADMIN']

class IsOrderOwner(permissions.BasePermission):
    """
    Checks if the user is the buyer or the vendor of the order.
    """
    def has_object_permission(self, request, view, obj):
        if obj.buyer == request.user:
            return True
        if hasattr(request.user, 'vendor_profile') and obj.vendor == request.user.vendor_profile:
            return True
        return False

class IsQuoteOwner(permissions.BasePermission):
    """
    Checks if the user is the buyer who requested the quote or the vendor responding.
    """
    def has_object_permission(self, request, view, obj):
        # QuoteRequest has a buyer
        if hasattr(obj, 'buyer') and obj.buyer == request.user:
            return True
        # QuoteRequest items? (not usually checked per item but per request)
        
        # Responses?
        if hasattr(obj, 'quote_request') and obj.quote_request.buyer == request.user:
            return True
        if hasattr(obj, 'vendor') and hasattr(request.user, 'vendor_profile') and obj.vendor == request.user.vendor_profile:
            return True
        return False
