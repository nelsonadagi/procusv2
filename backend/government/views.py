from rest_framework import viewsets, permissions
from .models import PublicTender
from .serializers import PublicTenderSerializer
from accounts.permissions import IsGovernment

from rbac.permissions import HasRequiredPermission
from rbac.utils import log_action

class PublicTenderViewSet(viewsets.ModelViewSet):
    queryset = PublicTender.objects.all().order_by('-created_at')
    serializer_class = PublicTenderSerializer
    permission_classes = [HasRequiredPermission]
    required_permission = 'government:view'
    permission_map = {
        'create': 'government:publish_tender',
        'update': 'government:publish_tender',
        'partial_update': 'government:publish_tender',
        'destroy': 'government:publish_tender',
    }
    
    def perform_create(self, serializer):
        tender = serializer.save()
        log_action(self.request.user, 'PUBLISH_TENDER', 'tender', tender.id)
