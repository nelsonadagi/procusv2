from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from .models import InvestorProfile, InvestmentAgreement
from .serializers import InvestorProfileSerializer, InvestmentAgreementSerializer

class InvestorProfileViewSet(viewsets.ModelViewSet):
    queryset = InvestorProfile.objects.all()
    serializer_class = InvestorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
         if self.request.user.role == 'ADMIN': return self.queryset
         return self.queryset.filter(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='onboard')
    def onboard(self, request):
        if hasattr(request.user, 'investor_profile'):
             return Response({"error": "Profile exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
             serializer.save(user=request.user)
             return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InvestmentAgreementViewSet(viewsets.ModelViewSet):
    queryset = InvestmentAgreement.objects.all()
    serializer_class = InvestmentAgreementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(investor=self.request.user)
        
    @action(detail=True, methods=['post'], url_path='sign')
    def sign(self, request, pk=None):
        agreement = self.get_object()
        if agreement.investor != request.user:
             return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        
        agreement.status = InvestmentAgreement.Status.SIGNED
        agreement.signed_at = timezone.now()
        agreement.save()
        return Response({"status": "Signed", "timestamp": agreement.signed_at})
