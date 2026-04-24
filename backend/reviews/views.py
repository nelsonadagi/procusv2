from rest_framework import viewsets, permissions
from .models import Rating
from .serializers import RatingSerializer
from rbac.permissions import HasRequiredPermission

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated, HasRequiredPermission]
    required_permission = 'reviews:view'
    permission_map = {
        'create': 'reviews:create',
        'update': 'reviews:create',
        'partial_update': 'reviews:create',
        'destroy': 'reviews:create',
    }

    def perform_create(self, serializer):
        from orders.tasks import update_vendor_performance_metrics
        rating = serializer.save(buyer=self.request.user, vendor=serializer.validated_data['order'].vendor)
        # Trigger async rating update
        update_vendor_performance_metrics.delay(rating.vendor.id)
