from rest_framework import viewsets, permissions
from .models import Organization, ApprovalWorkflow
from .serializers import OrganizationSerializer, ApprovalWorkflowSerializer
from rbac.permissions import HasRequiredPermission

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated, HasRequiredPermission]
    required_permission = 'enterprise:view'
    permission_map = {
        'create': 'enterprise:manage_org',
        'update': 'enterprise:manage_org',
        'partial_update': 'enterprise:manage_org',
        'destroy': 'enterprise:manage_org',
    }

    # MVP: Allow creation via API for testing, usually Admin only
    def perform_create(self, serializer):
        org = serializer.save()
        org.members.add(self.request.user)

class ApprovalWorkflowViewSet(viewsets.ModelViewSet):
    queryset = ApprovalWorkflow.objects.all()
    serializer_class = ApprovalWorkflowSerializer
    permission_classes = [permissions.IsAuthenticated, HasRequiredPermission]
    required_permission = 'enterprise:view'
    permission_map = {
        'create': 'enterprise:request_approval',
        'update': 'enterprise:approve_request',
        'partial_update': 'enterprise:approve_request',
        'destroy': 'enterprise:approve_request',
    }
