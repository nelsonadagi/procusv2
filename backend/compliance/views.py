from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import KYCVerification
from .serializers import KYCVerificationSerializer

class KYCVerificationViewSet(viewsets.ModelViewSet):
    queryset = KYCVerification.objects.all()
    serializer_class = KYCVerificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='upload-doc')
    def upload_doc(self, request):
         # Placeholder for file upload
         # In real app, handle MultiPartParser, upload to S3, return URL
         return Response({"url": "https://s3.aws.com/placeholder-doc.pdf"})
