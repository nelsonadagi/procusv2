from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import PropertyListing, PropertyProjectLink
from .serializers import PropertyListingSerializer
from projects.models import Project

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = PropertyListing.objects.all().order_by('-created_at')
    serializer_class = PropertyListingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], url_path='link-project')
    def link_project(self, request, pk=None):
        prop = self.get_object()
        if prop.owner != request.user:
             return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
             
        project_id = request.data.get('project_id')
        project = get_object_or_404(Project, id=project_id)
        
        link, _ = PropertyProjectLink.objects.get_or_create(property=prop, project=project)
        return Response({"status": "Linked"})
