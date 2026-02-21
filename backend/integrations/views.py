from rest_framework import viewsets, permissions
from .models import ERPConnector
from .serializers import ERPConnectorSerializer

class ERPConnectorViewSet(viewsets.ModelViewSet):
    queryset = ERPConnector.objects.all()
    serializer_class = ERPConnectorSerializer
    permission_classes = [permissions.IsAuthenticated]
