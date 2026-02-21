from rest_framework import viewsets, permissions
from .models import Category
from .serializers import CategorySerializer
from rbac.permissions import HasRequiredPermission

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [HasRequiredPermission]
    required_permission = 'taxonomy:view'
    permission_map = {
        'create': 'taxonomy:manage',
        'update': 'taxonomy:manage',
        'partial_update': 'taxonomy:manage',
        'destroy': 'taxonomy:manage',
    }

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return super().get_permissions()

    def get_queryset(self):
        # Admins see everything
        if self.request.user.is_staff:
            return Category.objects.all()
            
        # Public view: Only active categories
        queryset = Category.objects.filter(active=True)
        taxonomy_type = self.request.query_params.get('taxonomy_type')
        if taxonomy_type:
            queryset = queryset.filter(taxonomy_type=taxonomy_type)
        
        is_tree = self.request.query_params.get('tree', 'false').lower() == 'true'
        if is_tree:
            queryset = queryset.filter(parent=None)
            
        return queryset
