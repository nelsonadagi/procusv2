from rest_framework import viewsets, permissions
from .models import ERPConnector
from .serializers import ERPConnectorSerializer
from rbac.permissions import HasRequiredPermission

class ERPConnectorViewSet(viewsets.ModelViewSet):
    queryset = ERPConnector.objects.all()
    serializer_class = ERPConnectorSerializer
    permission_classes = [permissions.IsAuthenticated, HasRequiredPermission]
    required_permission = 'integrations:view'
    permission_map = {
        'create': 'integrations:manage_api_keys',
        'update': 'integrations:manage_api_keys',
        'partial_update': 'integrations:manage_api_keys',
        'destroy': 'integrations:manage_api_keys',
    }
