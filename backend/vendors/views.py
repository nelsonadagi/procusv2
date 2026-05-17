from rest_framework import viewsets, permissions, status, decorators
from rest_framework.response import Response
from .models import Vendor
from .serializers import VendorSerializer, VendorOnboardingSerializer
from rbac.permissions import HasRequiredPermission, IsVendorOwner
from accounts.models import User
from notifications.models import Notification
from notifications.services import notify_user

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_field = "uuid"
    permission_classes = [HasRequiredPermission]
    required_permission = 'vendors:view'
    permission_map = {
        'create': 'vendors:onboard', # Special permission for registering as vendor
        'update': 'vendors:update',
        'partial_update': 'vendors:update',
        'destroy': 'vendors:delete',
    }

    def _is_admin(self):
        user = self.request.user
        return user.is_staff or user.is_superuser or getattr(user, 'role', '') == 'ADMIN'

    def get_serializer_class(self):
        if self.action == 'create':
            return VendorOnboardingSerializer
        return VendorSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()] # Any authenticated user can apply to be a vendor
        if self.action in ['update', 'partial_update']:
            # Allow vendor owners or staff to update
            if self._is_admin():
                return [permissions.IsAuthenticated()]
            return [permissions.IsAuthenticated(), IsVendorOwner()]
        return super().get_permissions()

    def get_queryset(self):
        qs = super().get_queryset()
        
        # Staff/Admin users can see ALL vendors (including PENDING)
        if not self._is_admin():
            # Public view: Only approved vendors
            if self.action in ['list', 'retrieve']:
                qs = qs.filter(verified_status='APPROVED')
        
        # Proximity Search
        lat = self.request.query_params.get('latitude')
        lng = self.request.query_params.get('longitude')
        radius = self.request.query_params.get('radius_km')
        
        if lat and lng:
            from django.contrib.gis.db.models.functions import Distance
            from django.contrib.gis.geos import Point
            from django.contrib.gis.measure import D
            try:
                user_location = Point(float(lng), float(lat), srid=4326)
                if radius:
                    qs = qs.filter(location__point__distance_lte=(user_location, D(km=float(radius))))
                
                qs = qs.annotate(distance=Distance('location__point', user_location)).order_by('distance')
            except (ValueError, TypeError):
                pass
        
        # Delivery Eligibility Search
        d_lat = self.request.query_params.get('delivery_latitude')
        d_lng = self.request.query_params.get('delivery_longitude')
        if d_lat and d_lng:
            from django.contrib.gis.db.models.functions import Distance
            from django.contrib.gis.geos import Point
            from django.db.models import F
            try:
                target_point = Point(float(d_lng), float(d_lat), srid=4326)
                qs = qs.filter(provides_delivery=True)
                qs = qs.annotate(dist_to_user=Distance('location__point', target_point))
                # Filter vendors whose delivery_radius_km is >= distance to user
                # Note: distance is in meters by default in some PostGIS setups, 
                # but Distance function usually returns degrees or meters depending on SRID.
                # For SRID 4326, it might be degrees unless transformed.
                # Better to use Distance(..., transform=True) or similar if needed.
                # For simplicity, we'll assume the environment is set up for meter/km comparisons.
                qs = qs.filter(delivery_radius_km__gte=F('dist_to_user') / 1000)
            except (ValueError, TypeError):
                pass
                
        return qs

    def perform_update(self, serializer):
        """Allow staff to update verified_status, but restrict vendors from changing it"""
        previous_status = serializer.instance.verified_status
        if not self._is_admin():
            # Remove verified_status from validated_data if user is not staff
            if 'verified_status' in serializer.validated_data:
                serializer.validated_data.pop('verified_status')
        vendor = serializer.save()
        if self._is_admin() and previous_status != vendor.verified_status:
            if vendor.verified_status == Vendor.Status.APPROVED:
                vendor.user.grant_role(User.Role.VENDOR)
                notify_user(
                    vendor.user,
                    Notification.Type.SYSTEM,
                    "Vendor workspace approved",
                    "Your vendor profile was approved. You can now manage inventory and respond to quotes.",
                    data={"vendor_id": str(vendor.uuid)},
                )
            elif vendor.verified_status in [Vendor.Status.REJECTED, Vendor.Status.SUSPENDED]:
                vendor.user.revoke_role(User.Role.VENDOR)
                notify_user(
                    vendor.user,
                    Notification.Type.SYSTEM,
                    "Vendor workspace not approved",
                    "Your vendor profile status changed. Review your vendor onboarding details.",
                    data={"vendor_id": str(vendor.uuid), "status": vendor.verified_status},
                )

    @decorators.action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not hasattr(request.user, 'vendor_profile'):
            return Response({"detail": "User does not have a vendor profile."}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            vendor = request.user.vendor_profile
            serializer = VendorSerializer(vendor)
            return Response(serializer.data)
        except Vendor.DoesNotExist:
            return Response({"error": "No vendor profile found for this user."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Temporary: Catch any other exceptions to debug 500 errors
            return Response({"error": str(e), "message": "An unexpected error occurred while fetching vendor profile."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @decorators.action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def approve(self, request, pk=None, **kwargs):
        if not self._is_admin():
            return Response({"error": "Admin only"}, status=status.HTTP_403_FORBIDDEN)
        vendor = self.get_object()
        vendor.verified_status = Vendor.Status.APPROVED
        vendor.save(update_fields=['verified_status'])
        vendor.user.grant_role(User.Role.VENDOR)
        notify_user(
            vendor.user,
            Notification.Type.SYSTEM,
            "Vendor workspace approved",
            "Your vendor profile was approved. You can now manage inventory and respond to quotes.",
            data={"vendor_id": str(vendor.uuid)},
        )
        return Response(self.get_serializer(vendor).data)

    @decorators.action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def reject(self, request, pk=None, **kwargs):
        if not self._is_admin():
            return Response({"error": "Admin only"}, status=status.HTTP_403_FORBIDDEN)
        vendor = self.get_object()
        vendor.verified_status = Vendor.Status.REJECTED
        vendor.save(update_fields=['verified_status'])
        vendor.user.revoke_role(User.Role.VENDOR)
        notify_user(
            vendor.user,
            Notification.Type.SYSTEM,
            "Vendor workspace rejected",
            "Your vendor profile was rejected. Review your onboarding details and contact support if needed.",
            data={"vendor_id": str(vendor.uuid)},
        )
        return Response(self.get_serializer(vendor).data)
