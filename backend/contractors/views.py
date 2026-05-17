from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import ContractorProfile
from .serializers import ContractorProfileSerializer
from accounts.permissions import user_has_role
from accounts.models import User
from rbac.permissions import HasRequiredPermission
from notifications.models import Notification
from notifications.services import notify_user

class IsContractor(permissions.BasePermission):
    def has_permission(self, request, view):
        return user_has_role(request.user, 'CONTRACTOR')

class ContractorViewSet(viewsets.ModelViewSet):
    queryset = ContractorProfile.objects.all()
    serializer_class = ContractorProfileSerializer
    permission_classes = [HasRequiredPermission]
    required_permission = 'contractors:view'
    permission_map = {
        'create': 'contractors:onboard',
        'register': 'contractors:onboard',
        'update': 'contractors:update',
        'partial_update': 'contractors:update',
        'destroy': 'contractors:update',
        'approve': 'contractors:approve',
        'reject': 'contractors:approve',
    }

    def _is_admin(self):
        user = self.request.user
        return user.is_staff or user.is_superuser or getattr(user, 'role', '') == 'ADMIN'

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        if self.action in ['create', 'register', 'me']:
            return [permissions.IsAuthenticated(), HasRequiredPermission()]
        return [permissions.IsAuthenticated(), HasRequiredPermission()]

    def get_queryset(self):
        qs = super().get_queryset()

        if not self._is_admin():
            if self.action in ['list', 'retrieve']:
                qs = qs.filter(verified_status='APPROVED')
            elif hasattr(self.request.user, 'contractor_profile'):
                qs = qs.filter(user=self.request.user)

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

        return qs

    def perform_update(self, serializer):
        previous_status = serializer.instance.verified_status
        if not self._is_admin() and 'verified_status' in serializer.validated_data:
            serializer.validated_data.pop('verified_status')
        contractor = serializer.save()
        if self._is_admin() and previous_status != contractor.verified_status:
            if contractor.verified_status == ContractorProfile.Status.APPROVED:
                contractor.user.grant_role(User.Role.CONTRACTOR)
                notify_user(
                    contractor.user,
                    Notification.Type.SYSTEM,
                    "Contractor workspace approved",
                    "Your contractor profile was approved. You can now bid on eligible contracts.",
                    data={"contractor_id": contractor.id},
                )
            elif contractor.verified_status == ContractorProfile.Status.REJECTED:
                contractor.user.revoke_role(User.Role.CONTRACTOR)
                notify_user(
                    contractor.user,
                    Notification.Type.SYSTEM,
                    "Contractor workspace rejected",
                    "Your contractor profile was rejected. Review your onboarding details and contact support if needed.",
                    data={"contractor_id": contractor.id},
                )

    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        user = request.user
        if hasattr(user, 'contractor_profile'):
            return Response({"error": "Profile already exists"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated], url_path='me')
    def me(self, request):
        if not hasattr(request.user, 'contractor_profile'):
            return Response({"detail": "User does not have a contractor profile."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(request.user.contractor_profile)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        if not self._is_admin():
            return Response({"error": "Admin only"}, status=status.HTTP_403_FORBIDDEN)
        contractor = self.get_object()
        contractor.verified_status = ContractorProfile.Status.APPROVED
        contractor.save(update_fields=['verified_status'])
        contractor.user.grant_role(User.Role.CONTRACTOR)
        notify_user(
            contractor.user,
            Notification.Type.SYSTEM,
            "Contractor workspace approved",
            "Your contractor profile was approved. You can now bid on eligible contracts.",
            data={"contractor_id": contractor.id},
        )
        return Response(self.get_serializer(contractor).data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        if not self._is_admin():
            return Response({"error": "Admin only"}, status=status.HTTP_403_FORBIDDEN)
        contractor = self.get_object()
        contractor.verified_status = ContractorProfile.Status.REJECTED
        contractor.save(update_fields=['verified_status'])
        contractor.user.revoke_role(User.Role.CONTRACTOR)
        notify_user(
            contractor.user,
            Notification.Type.SYSTEM,
            "Contractor workspace rejected",
            "Your contractor profile was rejected. Review your onboarding details and contact support if needed.",
            data={"contractor_id": contractor.id},
        )
        return Response(self.get_serializer(contractor).data)
