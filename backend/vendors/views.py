from rest_framework import viewsets, permissions, status, decorators
from rest_framework.response import Response
from .models import Vendor
from .serializers import VendorSerializer, VendorOnboardingSerializer
from rbac.permissions import HasRequiredPermission, IsVendorOwner

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [HasRequiredPermission]
    required_permission = 'vendors:view'
    permission_map = {
        'create': 'vendors:onboard', # Special permission for registering as vendor
        'update': 'vendors:update',
        'partial_update': 'vendors:update',
        'destroy': 'vendors:delete',
    }

    def get_serializer_class(self):
        if self.action == 'create':
            return VendorOnboardingSerializer
        return VendorSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()] # Any authenticated user can apply to be a vendor
        if self.action in ['update', 'partial_update']:
            # Allow vendor owners or staff to update
            if self.request.user.is_staff:
                return [permissions.IsAuthenticated()]
            return [permissions.IsAuthenticated(), IsVendorOwner()]
        return super().get_permissions()

    def get_queryset(self):
        qs = super().get_queryset()
        
        # Staff/Admin users can see ALL vendors (including PENDING)
        if self.request.user.is_staff:
            return qs
        
        # Public view: Only approved vendors
        if self.action in ['list', 'retrieve']:
            return qs.filter(verified_status='APPROVED')
            
        return qs

    def perform_update(self, serializer):
        """Allow staff to update verified_status, but restrict vendors from changing it"""
        if not self.request.user.is_staff:
            # Remove verified_status from validated_data if user is not staff
            if 'verified_status' in serializer.validated_data:
                serializer.validated_data.pop('verified_status')
        serializer.save()

    @decorators.action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        try:
            vendor = request.user.vendor_profile
            serializer = VendorSerializer(vendor)
            return Response(serializer.data)
        except Vendor.DoesNotExist:
            return Response({"error": "No vendor profile found"}, status=status.HTTP_404_NOT_FOUND)
