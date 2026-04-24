from rest_framework import viewsets, decorators, status
from rest_framework.response import Response
from .models import RegulatoryReport
from .serializers import RegulatoryReportSerializer
from platform_settings.views import AdminOnly
from . import analytics


class RegulatoryReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RegulatoryReport.objects.all().order_by('-generated_at')
    serializer_class = RegulatoryReportSerializer
    permission_classes = [AdminOnly]


class AnalyticsViewSet(viewsets.ViewSet):
    """
    Admin analytics aggregation endpoints.
    All endpoints accept an optional `?days=N` query parameter (default: 30).
    """
    permission_classes = [AdminOnly]

    def _get_days(self, request):
        try:
            return int(request.query_params.get('days', 30))
        except (ValueError, TypeError):
            return 30

    @decorators.action(detail=False, methods=['get'])
    def summary(self, request):
        days = self._get_days(request)
        return Response(analytics.summary_kpis(days=days))

    @decorators.action(detail=False, methods=['get'])
    def financial(self, request):
        days = self._get_days(request)
        return Response(analytics.financial_trends(days=days))

    @decorators.action(detail=False, methods=['get'])
    def marketplace(self, request):
        days = self._get_days(request)
        return Response(analytics.marketplace_analytics(days=days))

    @decorators.action(detail=False, methods=['get'])
    def users(self, request):
        days = self._get_days(request)
        return Response(analytics.user_analytics(days=days))

    @decorators.action(detail=False, methods=['get'])
    def operations(self, request):
        days = self._get_days(request)
        return Response(analytics.operations_analytics(days=days))

    @decorators.action(detail=False, methods=['get'])
    def geographic(self, request):
        return Response(analytics.geographic_analytics())

    @decorators.action(detail=False, methods=['get'])
    def property(self, request):
        days = self._get_days(request)
        return Response(analytics.property_analytics(days=days))
