from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import ReliabilityScore
from .serializers import ReliabilityScoreSerializer

class ScoringViewSet(viewsets.ReadOnlyModelViewSet):
    # Admin can see all, User sees own
    queryset = ReliabilityScore.objects.all()
    serializer_class = ReliabilityScoreSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'ADMIN':
            return self.queryset
        return self.queryset.filter(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='recalculate')
    def recalculate(self, request):
        if request.user.role != 'ADMIN':
             return Response({"error": "Admin only"}, status=status.HTTP_403_FORBIDDEN)
        
        # Placeholder for rules logic
        # In real app: iterate users, check DB stats, update score
        return Response({"status": "Recalculation started (mock)"})
