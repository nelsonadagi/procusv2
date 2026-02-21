from rest_framework import viewsets, permissions
from .models import RegulatoryReport
from .serializers import RegulatoryReportSerializer

class RegulatoryReportViewSet(viewsets.ReadOnlyModelViewSet):
    # Admin only usually
    queryset = RegulatoryReport.objects.all().order_by('-generated_at')
    serializer_class = RegulatoryReportSerializer
    permission_classes = [permissions.IsAuthenticated] # Restrict to admin in real world
