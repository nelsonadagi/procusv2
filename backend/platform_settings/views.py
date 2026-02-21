from rest_framework import viewsets, views, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import PlatformSettings, FeatureFlag, CurrencyRate, Country
from .serializers import PlatformSettingsSerializer, FeatureFlagSerializer, CurrencyRateSerializer, CountrySerializer

User = get_user_model()


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            request.user.is_staff or request.user.is_superuser or getattr(request.user, 'role', '') == 'ADMIN'
        )


class PlatformConfigView(views.APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [AdminOnly()]

    def get(self, request):
        settings = PlatformSettings.objects.filter(is_active=True).first()
        if not settings:
            return Response({
                "platform_name": "Ujenzi Marketplace",
                "default_currency": "KES",
                "default_region": "KE",
            })
        return Response(PlatformSettingsSerializer(settings).data)

    def patch(self, request):
        settings = PlatformSettings.objects.filter(is_active=True).first()
        if not settings:
            settings = PlatformSettings.objects.create(is_active=True)
        serializer = PlatformSettingsSerializer(settings, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrencyRateViewSet(viewsets.ModelViewSet):
    queryset = CurrencyRate.objects.all()
    serializer_class = CurrencyRateSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [permissions.AllowAny()]
        return [AdminOnly()]


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [permissions.AllowAny()]
        return [AdminOnly()]

    @action(detail=True, methods=['post'])
    def set_default(self, request, pk=None):
        """Mark this country as the platform default."""
        country = self.get_object()
        country.is_default = True
        country.save()
        return Response(CountrySerializer(country).data)


class FeatureFlagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FeatureFlag.objects.filter(active=True)
    serializer_class = FeatureFlagSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'key'


# ── User Management (admin read-all) ──
class AdminUserViewSet(viewsets.ReadOnlyModelViewSet):
    """Full user list for admin config panel."""
    permission_classes = [AdminOnly]

    def get_queryset(self):
        return User.objects.all().order_by('-date_joined')

    def list(self, request):
        qs = self.get_queryset()
        data = [
            {
                'id': u.id,
                'username': u.username,
                'email': u.email,
                'first_name': u.first_name,
                'last_name': u.last_name,
                'role': getattr(u, 'role', ''),
                'roles': getattr(u, 'roles', []),
                'is_active': u.is_active,
                'is_staff': u.is_staff,
                'date_joined': u.date_joined,
            }
            for u in qs
        ]
        return Response(data)

    @action(detail=True, methods=['patch'])
    def toggle_active(self, request, pk=None):
        u = User.objects.get(pk=pk)
        u.is_active = not u.is_active
        u.save()
        return Response({'id': u.id, 'is_active': u.is_active})

    @action(detail=True, methods=['patch'])
    def set_role(self, request, pk=None):
        u = User.objects.get(pk=pk)
        new_role = request.data.get('role')
        if new_role:
            u.role = new_role
            u.save()
        return Response({'id': u.id, 'role': u.role})


# ── Role / Group Management ──
class AdminRoleViewSet(viewsets.ViewSet):
    """Manage Django Groups used as roles."""
    permission_classes = [AdminOnly]

    def list(self, request):
        groups = Group.objects.prefetch_related('permissions').all()
        data = [
            {'id': g.id, 'name': g.name, 'permissions_count': g.permissions.count()}
            for g in groups
        ]
        return Response(data)

    def create(self, request):
        name = request.data.get('name', '').strip()
        if not name:
            return Response({'error': 'Name required'}, status=400)
        g, created = Group.objects.get_or_create(name=name)
        return Response({'id': g.id, 'name': g.name}, status=201 if created else 200)

    def destroy(self, request, pk=None):
        try:
            Group.objects.get(pk=pk).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Group.DoesNotExist:
            return Response({'error': 'Not found'}, status=404)
