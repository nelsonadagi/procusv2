from rest_framework import viewsets, permissions
from .models import ThrottledRequest
from .serializers import ThrottledRequestSerializer
from rbac.permissions import HasRequiredPermission

class ThrottledRequestViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ThrottledRequest.objects.all()
    serializer_class = ThrottledRequestSerializer
    permission_classes = [HasRequiredPermission]
    required_permission = 'security:monitor'
