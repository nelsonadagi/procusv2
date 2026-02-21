from django.db import models
from django.http import HttpResponse
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, ProductImage
from taxonomy.models import Category
from .serializers import (
    ProductSerializer, 
    ProductListSerializer,
    ProductCreateUpdateSerializer,
    ProductImageSerializer
)
import csv
import io

from rbac.permissions import HasRequiredPermission, IsVendorOwner, VendorApprovedOnly
from rbac.utils import log_action

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().select_related('vendor', 'category').prefetch_related('images')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'category__slug', 'vendor', 'status', 'brand', 'is_featured']
    search_fields = ['name', 'short_description', 'description', 'vendor__business_name', 'brand']
    ordering_fields = ['base_price', 'created_at', 'name', 'stock_quantity']
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    permission_classes = [HasRequiredPermission]
    required_permission = 'catalog:view'
    permission_map = {
        'create': 'catalog:create',
        'update': 'catalog:update',
        'partial_update': 'catalog:update',
        'destroy': 'catalog:delete',
        'import_products': 'catalog:create',
        'upload_images': 'catalog:update',
    }

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProductCreateUpdateSerializer
        return ProductSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        if self.action == 'download_template':
            return [permissions.IsAuthenticated()]
        if self.action in ['create', 'import_products']:
            return [permissions.IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy', 'upload_images']:
            return [HasRequiredPermission(), IsVendorOwner()]
        return super().get_permissions()

    def get_queryset(self):
        qs = super().get_queryset()
        
        # User is Staff
        if self.request.user.is_staff:
            return qs
            
        # User is Authenticated Vendor
        if self.request.user.is_authenticated and hasattr(self.request.user, 'vendor_profile'):
            vendor = self.request.user.vendor_profile
            return qs.filter(models.Q(status='ACTIVE') | models.Q(vendor=vendor))
            
        # Anonymous or non-vendor Buyer
        qs = qs.filter(status='ACTIVE', vendor__verified_status='APPROVED')
        
        region = self.request.query_params.get('region')
        if region:
            # Simple check for region in delivery_regions list
            qs = qs.filter(delivery_regions__contains=region)
            
        return qs

    def perform_create(self, serializer):
        if not hasattr(self.request.user, 'vendor_profile'):
            from rest_framework.exceptions import ValidationError
            raise ValidationError("User has no vendor profile.")
            
        product = serializer.save(vendor=self.request.user.vendor_profile)
        log_action(self.request.user, 'CREATE_PRODUCT', 'product', product.id)
    
    def perform_update(self, serializer):
        product = serializer.save()
        log_action(self.request.user, 'UPDATE_PRODUCT', 'product', product.id)
    
    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def upload_images(self, request, pk=None):
        """Upload multiple images for a product"""
        product = self.get_object()
        
        # Check if user owns this product
        if not hasattr(request.user, 'vendor_profile') or product.vendor != request.user.vendor_profile:
            return Response(
                {'error': 'You do not have permission to upload images for this product'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        images_data = request.FILES.getlist('images')
        if not images_data:
            return Response(
                {'error': 'No images provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        created_images = []
        for idx, image_file in enumerate(images_data):
            # Create ProductImage instance
            product_image = ProductImage.objects.create(
                product=product,
                image=image_file,
                alt_text=request.data.get(f'alt_text_{idx}', f'{product.name} - Image {idx + 1}'),
                display_order=idx,
                is_primary=(idx == 0 and not product.images.exists())  # First image is primary if no images exist
            )
            created_images.append(product_image)
        
        serializer = ProductImageSerializer(created_images, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def import_products(self, request):
        """Import products from CSV file"""
        # Ensure user is a vendor (redundant with permission classes but safe)
        if not hasattr(request.user, 'vendor_profile'):
             return Response({'error': 'Only vendors can import products'}, status=status.HTTP_403_FORBIDDEN)
        
        file_obj = request.FILES.get('file')
        if not file_obj:
             return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
             
        # Check file extension
        # Using encoding='utf-8-sig' to handle BOM if present
        if not file_obj.name.lower().endswith('.csv'):
             return Response({'error': 'Only CSV files are supported at this time.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Decode file content
            decoded_file = file_obj.read().decode('utf-8-sig')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            
            created_count = 0
            errors = []
            
            # Get vendor profile
            vendor = request.user.vendor_profile
            
            for row_idx, row in enumerate(reader, start=1):
                try:
                    name = row.get('name') or row.get('Name') or row.get('Product Name')
                    if not name:
                        continue # Skip empty rows or rows without name

                    category_field = row.get('category') or row.get('Category')
                    if not category_field:
                        raise ValueError("Category is required")
                        
                    # Find category by name (case insensitive) or slug
                    # Also try to clean up the category name e.g. "Materials" -> "Materials"
                    category_field = category_field.strip()
                    category = Category.objects.filter(
                        models.Q(name__iexact=category_field) | models.Q(slug__iexact=category_field),
                        taxonomy_type='MATERIAL'
                    ).first()
                    
                    if not category:
                        # Try to find by partial match if exact fails? No, too risky.
                         raise ValueError(f"Category '{category_field}' not found. Please verify category name.")
                         
                    # Create product
                    # Basic fields
                    Product.objects.create(
                        vendor=vendor,
                        category=category,
                        name=name.strip(),
                        description=row.get('description', '') or row.get('Description', ''),
                        short_description=row.get('short_description', '') or row.get('Short Description', ''),
                        unit=row.get('unit', '') or row.get('Unit', 'unit'),
                        base_price=row.get('base_price') or row.get('Price', 0),
                        stock_quantity=row.get('stock_quantity') or row.get('Stock', 0),
                        brand=row.get('brand', '') or row.get('Brand', ''),
                        status='ACTIVE'
                    )
                    created_count += 1
                except Exception as e:
                    errors.append(f"Row {row_idx}: {str(e)}")
            
            return Response({
                'message': f'Successfully imported {created_count} products.',
                'created_count': created_count,
                'errors': errors
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            # Catch file reading errors
            return Response({'error': f'Failed to process file: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def download_template(self, request):
        """Download a CSV template for product import"""
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="product_import_template.csv"'

        writer = csv.writer(response)
        # Headers should match the expected import format
        headers = ['Name', 'Category', 'Price', 'Unit', 'Stock', 'Brand', 'Description', 'Short Description']
        writer.writerow(headers)
        
        # Add an example row
        example_row = [
            'Example Cement 50kg', 
            'Cement', 
            '650', 
            'bag', 
            '100', 
            'Simba', 
            'High strength portland cement', 
            '50kg bag'
        ]
        writer.writerow(example_row)

        return response


class ProductImageViewSet(viewsets.ModelViewSet):
    """ViewSet for managing product images"""
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [HasRequiredPermission]
    required_permission = 'catalog:view'
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsVendorOwner()]    
    def get_queryset(self):
        qs = super().get_queryset()
        
        # Filter by product if provided
        product_id = self.request.query_params.get('product')
        if product_id:
            qs = qs.filter(product_id=product_id)
        
        # Vendors can only see their own product images
        if hasattr(self.request.user, 'vendor_profile'):
            qs = qs.filter(product__vendor=self.request.user.vendor_profile)
        elif not self.request.user.is_staff:
            # Non-vendors can only see images of active products
            qs = qs.filter(product__status='ACTIVE')
        
        return qs
    
    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        
        # Check if user owns this product
        if not hasattr(self.request.user, 'vendor_profile') or product.vendor != self.request.user.vendor_profile:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You do not have permission to add images to this product")
        
        serializer.save()
    
    def perform_update(self, serializer):
        image = self.get_object()
        
        # Check if user owns this product
        if not hasattr(self.request.user, 'vendor_profile') or image.product.vendor != self.request.user.vendor_profile:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You do not have permission to update this image")
        
        serializer.save()
    
    def perform_destroy(self, instance):
        # Check if user owns this product
        if not hasattr(self.request.user, 'vendor_profile') or instance.product.vendor != self.request.user.vendor_profile:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You do not have permission to delete this image")
        
        instance.delete()
    
    @action(detail=True, methods=['post'])
    def set_primary(self, request, pk=None):
        """Set this image as the primary image for the product"""
        image = self.get_object()
        
        # Check ownership
        if not hasattr(request.user, 'vendor_profile') or image.product.vendor != request.user.vendor_profile:
            return Response(
                {'error': 'You do not have permission to modify this image'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Unset other primary images
        ProductImage.objects.filter(product=image.product, is_primary=True).update(is_primary=False)
        
        # Set this as primary
        image.is_primary = True
        image.save()
        
        serializer = self.get_serializer(image)
        return Response(serializer.data)
