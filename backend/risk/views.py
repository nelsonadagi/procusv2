from rest_framework import viewsets, permissions
from .models import ComplianceAlert
from .serializers import ComplianceAlertSerializer

class RiskViewSet(viewsets.ReadOnlyModelViewSet):
    # Admin only usually
    queryset = ComplianceAlert.objects.all()
    serializer_class = ComplianceAlertSerializer
    permission_classes = [permissions.IsAuthenticated]
