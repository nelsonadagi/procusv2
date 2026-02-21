from rest_framework import viewsets, serializers
from .models import AuditLog
from .permissions import HasRequiredPermission

class AuditLogSerializer(serializers.ModelSerializer):
    actor_name = serializers.CharField(source='actor.username', read_only=True)
    
    class Meta:
        model = AuditLog
        fields = ['id', 'actor', 'actor_name', 'action', 'resource_type', 'resource_id', 'timestamp', 'metadata']

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all().order_by('-timestamp')
    serializer_class = AuditLogSerializer
    permission_classes = [HasRequiredPermission]
    required_permission = 'compliance:view'
