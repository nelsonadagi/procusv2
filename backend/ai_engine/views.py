from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import UnderwritingPrediction
from .serializers import UnderwritingPredictionSerializer

class PredictionViewSet(viewsets.ReadOnlyModelViewSet):
    # Admin only usually
    queryset = UnderwritingPrediction.objects.all()
    serializer_class = UnderwritingPredictionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='predict-default')
    def predict_default(self, request):
         # Mock AI prediction
         return Response({
             "user_id": request.data.get('user_id'),
             "risk_score": 0.15,
             "confidence": 0.92,
             "factors": ["High leverage", "New account"]
         })
