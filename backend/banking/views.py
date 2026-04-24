from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import BankAccount, SettlementTransaction
from .serializers import BankAccountSerializer, SettlementTransactionSerializer
from rbac.permissions import HasRequiredPermission

class BankAccountViewSet(viewsets.ModelViewSet):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    permission_classes = [permissions.IsAuthenticated, HasRequiredPermission]
    required_permission = 'banking:view'
    permission_map = {
        'create': 'banking:manage_accounts',
        'update': 'banking:manage_accounts',
        'partial_update': 'banking:manage_accounts',
        'destroy': 'banking:manage_accounts',
    }

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SettlementTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SettlementTransaction.objects.all()
    serializer_class = SettlementTransactionSerializer
    permission_classes = [permissions.IsAuthenticated, HasRequiredPermission]
    required_permission = 'banking:view'
