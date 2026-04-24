from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from .models import KYCVerification, JurisdictionRule
from .serializers import KYCVerificationSerializer, JurisdictionRuleSerializer
from rbac.permissions import HasRequiredPermission

class KYCVerificationViewSet(viewsets.ModelViewSet):
    queryset = KYCVerification.objects.all()
    serializer_class = KYCVerificationSerializer
    permission_classes = [permissions.IsAuthenticated, HasRequiredPermission]
    required_permission = 'compliance:view'
    permission_map = {
        'create': 'investments:onboard',
        'update': 'investments:onboard',
        'partial_update': 'investments:onboard',
        'approve': 'compliance:verify_kyc',
        'reject': 'compliance:verify_kyc',
        'upload_doc': 'investments:onboard',
    }

    def _is_admin(self):
        user = self.request.user
        return user.is_staff or user.is_superuser or getattr(user, 'role', '') == 'ADMIN'

    def get_queryset(self):
        if self._is_admin():
            return self.queryset.order_by('-submitted_at')
        return self.queryset.filter(user=self.request.user).order_by('-submitted_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status=KYCVerification.Status.SUBMITTED)

    @action(detail=False, methods=['post'], url_path='upload-doc')
    def upload_doc(self, request):
         # Placeholder for file upload
         # In real app, handle MultiPartParser, upload to S3, return URL
         return Response({"url": "https://s3.aws.com/placeholder-doc.pdf"})

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        if not self._is_admin():
            return Response({"error": "Admin only"}, status=status.HTTP_403_FORBIDDEN)
        record = self.get_object()
        record.status = KYCVerification.Status.VERIFIED
        record.verified_at = timezone.now()
        record.save(update_fields=['status', 'verified_at'])
        return Response(self.get_serializer(record).data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        if not self._is_admin():
            return Response({"error": "Admin only"}, status=status.HTTP_403_FORBIDDEN)
        record = self.get_object()
        record.status = KYCVerification.Status.REJECTED
        record.verified_at = None
        record.save(update_fields=['status', 'verified_at'])
        return Response(self.get_serializer(record).data)

class JurisdictionRuleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = JurisdictionRule.objects.all()
    serializer_class = JurisdictionRuleSerializer
    permission_classes = [permissions.AllowAny]
