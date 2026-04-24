from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import SecondaryTrade
from .serializers import SecondaryTradeSerializer
from rbac.permissions import HasRequiredPermission

class SecondaryTradeViewSet(viewsets.ModelViewSet):
    queryset = SecondaryTrade.objects.all()
    serializer_class = SecondaryTradeSerializer
    permission_classes = [permissions.IsAuthenticated, HasRequiredPermission]
    required_permission = 'investments:view'
    permission_map = {
        'create': 'investments:transfer_stake',
        'update': 'investments:transfer_stake',
        'partial_update': 'investments:transfer_stake',
        'destroy': 'investments:transfer_stake',
    }

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    def get_queryset(self):
         # Users see their own trades + active market requests
         return self.queryset.filter(status='REQUESTED') | self.queryset.filter(seller=self.request.user)
