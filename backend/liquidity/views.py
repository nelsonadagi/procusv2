from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import SecondaryTrade
from .serializers import SecondaryTradeSerializer

class SecondaryTradeViewSet(viewsets.ModelViewSet):
    queryset = SecondaryTrade.objects.all()
    serializer_class = SecondaryTradeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    def get_queryset(self):
         # Users see their own trades + active market requests
         return self.queryset.filter(status='REQUESTED') | self.queryset.filter(seller=self.request.user)
