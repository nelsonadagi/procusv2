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
    
    def get_queryset(self):
        qs = super().get_queryset()
        
        # Proximity Search
        lat = self.request.query_params.get('latitude')
        lng = self.request.query_params.get('longitude')
        radius = self.request.query_params.get('radius_km')
        
        if lat and lng:
            from django.contrib.gis.db.models.functions import Distance
            from django.contrib.gis.geos import Point
            from django.contrib.gis.measure import D
            try:
                user_location = Point(float(lng), float(lat), srid=4326)
                if radius:
                    qs = qs.filter(location__point__distance_lte=(user_location, D(km=float(radius))))
                
                qs = qs.annotate(distance=Distance('location__point', user_location)).order_by('distance')
            except (ValueError, TypeError):
                pass
                
        return qs

    def perform_create(self, serializer):
        tender = serializer.save()
        log_action(self.request.user, 'PUBLISH_TENDER', 'tender', tender.id)
