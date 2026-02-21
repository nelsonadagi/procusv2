from rest_framework import viewsets, permissions
from .models import Organization, ApprovalWorkflow
from .serializers import OrganizationSerializer, ApprovalWorkflowSerializer

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]

    # MVP: Allow creation via API for testing, usually Admin only
    def perform_create(self, serializer):
        org = serializer.save()
        org.members.add(self.request.user)

class ApprovalWorkflowViewSet(viewsets.ModelViewSet):
    queryset = ApprovalWorkflow.objects.all()
    serializer_class = ApprovalWorkflowSerializer
    permission_classes = [permissions.IsAuthenticated]
