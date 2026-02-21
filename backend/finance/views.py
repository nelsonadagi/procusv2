from rest_framework import viewsets, permissions
from .models import FinanceProduct, FinanceApplication
from .serializers import FinanceProductSerializer, FinanceApplicationSerializer

class FinanceProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FinanceProduct.objects.filter(active=True)
    serializer_class = FinanceProductSerializer
    permission_classes = [permissions.AllowAny]

class FinanceApplicationViewSet(viewsets.ModelViewSet):
    queryset = FinanceApplication.objects.all()
    serializer_class = FinanceApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user)
    
    def get_queryset(self):
        if self.request.user.role == 'ADMIN':
            return self.queryset
        return self.queryset.filter(applicant=self.request.user)
