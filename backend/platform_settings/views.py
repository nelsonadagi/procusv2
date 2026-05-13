from rest_framework import viewsets, views, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from rbac.permission_catalog import get_permission_catalog
from .models import PlatformSettings, FeatureFlag, CurrencyRate, Country, PaymentGatewayConfig, ExchangeRateConfig
from .serializers import (
    PlatformSettingsSerializer,
    FeatureFlagSerializer,
    CurrencyRateSerializer,
    CountrySerializer,
    PaymentGatewayConfigSerializer,
    PaymentGatewayPublicSerializer,
    ExchangeRateConfigSerializer,
)
from .services import ensure_default_countries

User = get_user_model()


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            request.user.is_staff or request.user.is_superuser or getattr(request.user, 'role', '') == 'ADMIN'
        )


class PlatformConfigView(views.APIView):
    permission_classes = [permissions.AllowAny]

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

    def get_queryset(self):
        ensure_default_countries()
        return super().get_queryset()

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [permissions.AllowAny()]
        return [AdminOnly()]

    @action(detail=True, methods=['post'])
    def set_default(self, request, pk=None):
        """Mark this country as the platform default."""
        country = self.get_object()
        country.is_default = True
        country.save(update_fields=['is_default'])
        return Response(CountrySerializer(country).data)


class FeatureFlagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FeatureFlag.objects.filter(active=True)
    serializer_class = FeatureFlagSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'key'


class PaymentGatewayConfigViewSet(viewsets.ModelViewSet):
    queryset = PaymentGatewayConfig.objects.all().order_by('display_order', 'label')
    serializer_class = PaymentGatewayConfigSerializer
    permission_classes = [AdminOnly]


class PaymentMethodCatalogView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        methods = PaymentGatewayConfig.objects.filter(active=True).order_by('display_order', 'label')
        serializer = PaymentGatewayPublicSerializer(methods, many=True)
        return Response(serializer.data)


class ExchangeRateConfigViewSet(viewsets.ModelViewSet):
    queryset = ExchangeRateConfig.objects.all().order_by('-active', 'label')
    serializer_class = ExchangeRateConfigSerializer
    permission_classes = [AdminOnly]


# ── User Management (admin read-all) ──
class AdminUserViewSet(viewsets.ReadOnlyModelViewSet):
    """Full user list for admin config panel."""
    permission_classes = [AdminOnly]
    VALID_ROLES = {choice[0] for choice in User.Role.choices}
    NON_ADMIN_ROLES = VALID_ROLES - {User.Role.ADMIN}

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
                'groups': list(u.groups.values_list('name', flat=True)),
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
        if u.pk == request.user.pk:
            return Response({'detail': 'You cannot deactivate your own admin session.'}, status=status.HTTP_400_BAD_REQUEST)
        u.is_active = not u.is_active
        u.save(update_fields=['is_active'])
        return Response({'id': u.id, 'is_active': u.is_active})

    @action(detail=True, methods=['patch'])
    def set_role(self, request, pk=None):
        u = User.objects.get(pk=pk)
        new_role = request.data.get('role')
        if not new_role:
            return Response({'detail': 'Role is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if new_role not in self.VALID_ROLES:
            return Response({'detail': f'Invalid role: {new_role}.'}, status=status.HTTP_400_BAD_REQUEST)
        if u.pk == request.user.pk and new_role != User.Role.ADMIN:
            return Response({'detail': 'You cannot remove your own admin role from this screen.'}, status=status.HTTP_400_BAD_REQUEST)

        u.role = new_role
        u.is_staff = new_role == User.Role.ADMIN
        if new_role == User.Role.ADMIN:
            u.roles = []
            u.save(update_fields=['role', 'roles', 'is_staff'])
        else:
            u.roles = [role for role in (u.roles or []) if role in self.NON_ADMIN_ROLES and role != new_role]
            u.save(update_fields=['role', 'roles', 'is_staff'])
        return Response({'id': u.id, 'role': u.role, 'roles': u.roles, 'is_staff': u.is_staff})

    @action(detail=True, methods=['patch'])
    def set_additional_roles(self, request, pk=None):
        u = User.objects.get(pk=pk)
        new_roles = request.data.get('roles')
        if not isinstance(new_roles, list):
            return Response({'detail': 'Roles must be provided as a list.'}, status=status.HTTP_400_BAD_REQUEST)
        if u.role == User.Role.ADMIN:
            return Response({'detail': 'Admin accounts cannot hold additional non-admin roles.'}, status=status.HTTP_400_BAD_REQUEST)

        normalized_roles = []
        for role in new_roles:
            if role not in self.NON_ADMIN_ROLES:
                return Response({'detail': f'Invalid additional role: {role}.'}, status=status.HTTP_400_BAD_REQUEST)
            if role == u.role or role in normalized_roles:
                continue
            normalized_roles.append(role)

        u.roles = normalized_roles
        u.save(update_fields=['roles'])
        return Response({'id': u.id, 'role': u.role, 'roles': u.roles})


# ── Role / Group Management ──
class AdminRoleViewSet(viewsets.ViewSet):
    """Manage Django Groups used as roles."""
    permission_classes = [AdminOnly]

    def _rbac_content_type(self):
        from django.contrib.contenttypes.models import ContentType
        return ContentType.objects.get_or_create(app_label='rbac', model='permission_logical')[0]

    def list(self, request):
        groups = Group.objects.prefetch_related('permissions').all()
        data = [
            {
                'id': g.id,
                'name': g.name,
                'permissions_count': g.permissions.count(),
                'permissions': [
                    {
                        'id': perm.id,
                        'codename': perm.codename,
                        'name': perm.name,
                    }
                    for perm in g.permissions.all().order_by('codename')
                ]
            }
            for g in groups
        ]
        return Response(data)

    def create(self, request):
        name = request.data.get('name', '').strip()
        if not name:
            return Response({'error': 'Name required'}, status=400)
        g, created = Group.objects.get_or_create(name=name)
        return Response({'id': g.id, 'name': g.name, 'permissions_count': g.permissions.count(), 'permissions': []}, status=201 if created else 200)

    @action(detail=False, methods=['get'])
    def permission_catalog(self, request):
        seeded_permissions = {
            perm.codename: perm
            for perm in Permission.objects.filter(content_type__app_label='rbac').order_by('codename')
        }
        data = []
        for definition in get_permission_catalog():
            permission = seeded_permissions.get(definition['codename'])
            data.append({
                'id': permission.id if permission else None,
                'codename': definition['codename'],
                'name': definition['name'],
                'description': definition['description'],
                'namespace': definition['namespace'],
                'action': definition['action'],
                'default_roles': definition['default_roles'],
                'seeded': permission is not None,
            })
        return Response(data)

    @action(detail=False, methods=['post'], url_path='permissions')
    def create_permission(self, request):
        return Response(
            {'detail': 'Permissions are predefined by the platform catalog. Admins can assign them to roles but cannot create new ones here.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @action(detail=False, methods=['patch'], url_path=r'permissions/(?P<permission_id>[^/.]+)')
    def update_permission(self, request, permission_id=None):
        return Response(
            {'detail': 'Permissions are predefined by the platform catalog and cannot be edited from admin settings.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @action(detail=False, methods=['delete'], url_path=r'permissions/(?P<permission_id>[^/.]+)')
    def delete_permission(self, request, permission_id=None):
        return Response(
            {'detail': 'Permissions are predefined by the platform catalog and cannot be deleted from admin settings.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @action(detail=True, methods=['patch'])
    def set_permissions(self, request, pk=None):
        try:
            group = Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            return Response({'error': 'Not found'}, status=404)

        permission_ids = request.data.get('permission_ids')
        if not isinstance(permission_ids, list):
            return Response({'detail': 'permission_ids must be provided as a list.'}, status=status.HTTP_400_BAD_REQUEST)

        predefined_codenames = {definition['codename'] for definition in get_permission_catalog()}
        permissions_qs = Permission.objects.filter(
            id__in=permission_ids,
            content_type__app_label='rbac',
            codename__in=predefined_codenames,
        )
        if permissions_qs.count() != len(set(permission_ids)):
            return Response({'detail': 'One or more permissions are invalid or not part of the predefined RBAC catalog.'}, status=status.HTTP_400_BAD_REQUEST)

        group.permissions.set(permissions_qs)
        return Response({
            'id': group.id,
            'name': group.name,
            'permissions_count': group.permissions.count(),
            'permissions': [
                {
                    'id': perm.id,
                    'codename': perm.codename,
                    'name': perm.name,
                }
                for perm in group.permissions.all().order_by('codename')
            ]
        })

    def destroy(self, request, pk=None):
        try:
            Group.objects.get(pk=pk).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Group.DoesNotExist:
            return Response({'error': 'Not found'}, status=404)
