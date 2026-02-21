from rest_framework import viewsets, permissions
from .models import Rating
from .serializers import RatingSerializer

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        from orders.tasks import update_vendor_performance_metrics
        rating = serializer.save(buyer=self.request.user, vendor=serializer.validated_data['order'].vendor)
        # Trigger async rating update
        update_vendor_performance_metrics.delay(rating.vendor.id)
