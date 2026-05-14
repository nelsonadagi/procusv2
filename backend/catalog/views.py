from django.db import models
from django.db.utils import DatabaseError
from django.db import transaction
from django.http import HttpResponse
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, ProductImage, ProductCertificationRegistry, ProductInventoryMovement
from .models import ProductDocument
from taxonomy.models import Category
from .serializers import (
    ProductSerializer,
    ProductListSerializer,
    ProductCreateUpdateSerializer,
    ProductImageSerializer,
    ProductDocumentSerializer,
    ProductCertificationRegistrySerializer,
    ProductInventoryMovementSerializer,
    ProductInventoryAdjustmentSerializer,
)
import csv
import io

from rbac.permissions import HasRequiredPermission, IsVendorOwner, VendorApprovedOnly
from rbac.utils import log_action
from platform_settings.utils import resolve_request_country_code

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().select_related(
        'vendor', 'category', 'country', 'vendor__country', 'vendor__location'
    ).prefetch_related(
        'images', 'certification_entries__registry', 'attribute_entries', 'documents'
    )
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__uuid', 'category__slug', 'vendor__uuid', 'vendor__country', 'status', 'brand', 'is_featured']
    search_fields = [
        'name', 'short_description', 'description',
        'vendor__business_name', 'brand',
        'vendor__location_text', 'vendor__formatted_address',
        'category__name', 'category__slug',
        'certification_entries__display_name',
        'certification_entries__registry__name',
        'certification_entries__registry__code',
    ]
    ordering_fields = ['base_price', 'created_at', 'name', 'stock_quantity']
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    permission_classes = [HasRequiredPermission]
    required_permission = 'catalog:view'
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'
    lookup_value_regex = '[0-9a-fA-F-]{36}'
    permission_map = {
        'create': 'catalog:create',
        'update': 'catalog:update',
        'partial_update': 'catalog:update',
        'destroy': 'catalog:delete',
        'import_products': 'catalog:create',
        'upload_images': 'catalog:update',
        'upload_documents': 'catalog:update',
        'adjust_inventory': 'catalog:manage_stock',
        'inventory_history': 'catalog:manage_stock',
    }

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        elif self.action == 'me':
            return ProductSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProductCreateUpdateSerializer
        elif self.action == 'inventory_history':
            return ProductInventoryMovementSerializer
        elif self.action == 'adjust_inventory':
            return ProductInventoryAdjustmentSerializer
        return ProductSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        if self.action == 'me': # 'me' action requires authentication
            return [permissions.IsAuthenticated()]
        if self.action == 'download_template':
            return [permissions.IsAuthenticated()]
        if self.action in ['create', 'import_products']:
            return [permissions.IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy', 'upload_images', 'upload_documents', 'adjust_inventory', 'inventory_history']:
            return [HasRequiredPermission(), IsVendorOwner()]
        return super().get_permissions()

    def get_queryset(self):
        qs = super().get_queryset()

        # Staff sees all product statuses (draft, active, disabled, etc.)
        # but still respects country, category, price, and other filters below.
        is_staff = self.request.user.is_staff

        # User is Authenticated Vendor
        if self.request.user.is_authenticated and hasattr(self.request.user, 'vendor_profile'):
            vendor = self.request.user.vendor_profile
            # For 'me' action, return only the vendor's products
            if self.action == 'me':
                return qs.filter(vendor=vendor)
            # Vendors see their own products + active ones; staff sees everything
            if not is_staff:
                qs = qs.filter(models.Q(status='ACTIVE') | models.Q(vendor=vendor))
        elif not is_staff:
            # Anonymous or non-vendor Buyer — only active, approved vendor products
            qs = qs.filter(status='ACTIVE', vendor__verified_status='APPROVED')

        country_code = resolve_request_country_code(self.request)
        if country_code:
            country_filter = models.Q(country__iso_code__iexact=country_code)
            vendor_filter = models.Q(vendor__country__iso_code__iexact=country_code)
            if str(country_code).isdigit():
                country_filter |= models.Q(country_id=country_code)
                vendor_filter |= models.Q(vendor__country_id=country_code)
            qs = qs.filter(country_filter | (models.Q(country__isnull=True) & vendor_filter))

        category_id = self.request.query_params.get('category')
        if category_id:
            qs = qs.filter(category__uuid=category_id)

        category_slug = self.request.query_params.get('category_slug')
        if category_slug:
            qs = qs.filter(category__slug__iexact=category_slug)

        # High-Precision Hierarchical Discovery
        county = self.request.query_params.get('county')
        if county:
            qs = qs.filter(vendor__location_hierarchy__county__iexact=county)

        subcounty = self.request.query_params.get('subcounty') or self.request.query_params.get('city')
        if subcounty:
            from django.db.models import Q
            qs = qs.filter(
                Q(vendor__location_hierarchy__district__iexact=subcounty) |
                Q(vendor__location_hierarchy__city__iexact=subcounty) |
                Q(vendor__location_hierarchy__town__iexact=subcounty) |
                Q(vendor__location_hierarchy__suburb__iexact=subcounty)
            )

        min_price = self.request.query_params.get('base_price__gte') or self.request.query_params.get('min_price')
        if min_price:
            try:
                qs = qs.filter(base_price__gte=min_price)
            except (TypeError, ValueError):
                pass

        max_price = self.request.query_params.get('base_price__lte') or self.request.query_params.get('max_price')
        if max_price:
            try:
                qs = qs.filter(base_price__lte=max_price)
            except (TypeError, ValueError):
                pass

        inventory_signal = self.request.query_params.get('inventory_signal')
        if inventory_signal == 'OUT_OF_STOCK':
            qs = qs.filter(stock_quantity__lte=0)
        elif inventory_signal == 'LOW_STOCK':
            qs = qs.filter(stock_quantity__gt=0, stock_quantity__lte=models.F('reorder_level'))
        elif inventory_signal == 'IN_STOCK':
            qs = qs.filter(stock_quantity__gt=0)

        in_stock_only = self.request.query_params.get('is_in_stock')
        if str(in_stock_only).lower() in {'true', '1', 'yes'}:
            qs = qs.filter(stock_quantity__gt=0)

        verified_only = self.request.query_params.get('is_verified')
        if str(verified_only).lower() in {'true', '1', 'yes'}:
            qs = qs.filter(vendor__verified_status='APPROVED')

        certification = self.request.query_params.get('certification')
        if certification:
            qs = qs.filter(
                models.Q(certification_entries__display_name__icontains=certification) |
                models.Q(certification_entries__registry__name__icontains=certification) |
                models.Q(certification_entries__registry__code__icontains=certification) |
                models.Q(certifications__icontains=certification)
            )

        origin = self.request.query_params.get('country_of_origin')
        if origin:
            qs = qs.filter(country_of_origin__icontains=origin)

        delivery_region = self.request.query_params.get('delivery_region')
        if delivery_region:
            qs = qs.filter(delivery_regions__icontains=delivery_region)

        brand = self.request.query_params.get('brand')
        if brand:
            qs = qs.filter(brand__icontains=brand)

        featured_only = self.request.query_params.get('is_featured')
        if str(featured_only).lower() in {'true', '1', 'yes'}:
            qs = qs.filter(is_featured=True)

        # Proximity Search (Vendor Location)
        lat = self.request.query_params.get('latitude')
        lng = self.request.query_params.get('longitude')
        radius = self.request.query_params.get('radius_km')

        if lat and lng:
            from django.contrib.gis.db.models.functions import Distance
            from django.contrib.gis.geos import Point
            from django.contrib.gis.measure import D
            try:
                user_location = Point(float(lng), float(lat), srid=4326)
                if radius:
                    qs = qs.filter(vendor__location__point__distance_lte=(user_location, D(km=float(radius))))

                qs = qs.annotate(distance=Distance('vendor__location__point', user_location)).order_by('distance')
            except (ValueError, TypeError, DatabaseError):
                pass

        return qs.distinct()

    @action(detail=False, methods=['get'])
    def locations(self, request):
        """Retrieve unique counties and cities for hierarchical filtering."""
        from vendors.models import Vendor
        country_code = resolve_request_country_code(request)

        vendors = Vendor.objects.filter(verified_status='APPROVED')
        if country_code:
            country_filter = models.Q(country__iso_code__iexact=country_code)
            if str(country_code).isdigit():
                country_filter |= models.Q(country_id=country_code)
            vendors = vendors.filter(country_filter)

        # Extract unique values from JSONField hierarchy
        # Note: In production with large data, this should be pre-aggregated or cached
        counties = set()
        districts = set()

        for v in vendors:
            h = v.location_hierarchy or {}
            c = h.get('county')
            if c: counties.add(c)

            d = h.get('district') or h.get('city') or h.get('town') or h.get('suburb')
            if d: districts.add(d)

        return Response({
            "counties": sorted(list(counties)),
            "subcounties": sorted(list(districts))
        })

    @action(detail=False, methods=['get'], url_path='certification-options')
    def certification_options(self, request):
        queryset = ProductCertificationRegistry.objects.filter(active=True).order_by('name')
        serializer = ProductCertificationRegistrySerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        if not hasattr(self.request.user, 'vendor_profile'):
            from rest_framework.exceptions import ValidationError
            raise ValidationError("User has no vendor profile.")

        product = serializer.save(vendor=self.request.user.vendor_profile)
        if product.stock_quantity:
            product.record_inventory_movement(
                movement_type=ProductInventoryMovement.MovementType.INITIAL,
                quantity_delta=product.stock_quantity,
                quantity_before=0,
                quantity_after=product.stock_quantity,
                actor=self.request.user,
                note='Initial stock created with product record.',
            )
        log_action(self.request.user, 'CREATE_PRODUCT', 'product', product.id)

    def perform_update(self, serializer):
        existing_product = self.get_object()
        previous_stock = existing_product.stock_quantity
        product = serializer.save()
        if product.stock_quantity != previous_stock:
            product.record_inventory_movement(
                movement_type=ProductInventoryMovement.MovementType.MANUAL_ADJUSTMENT,
                quantity_delta=product.stock_quantity - previous_stock,
                quantity_before=previous_stock,
                quantity_after=product.stock_quantity,
                actor=self.request.user,
                note='Inventory updated from product editor.',
            )
        log_action(self.request.user, 'UPDATE_PRODUCT', 'product', product.id)

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        """Retrieve products for the authenticated vendor."""
        if not hasattr(request.user, 'vendor_profile'):
            return Response({"detail": "User is not a vendor."}, status=status.HTTP_403_FORBIDDEN)

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='inventory-history')
    def inventory_history(self, request, pk=None):
        product = self.get_object()
        queryset = product.inventory_movements.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='adjust-inventory')
    def adjust_inventory(self, request, pk=None):
        product = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quantity_delta = serializer.validated_data['quantity_delta']
        note = serializer.validated_data.get('note', '')
        reference = serializer.validated_data.get('reference', '')

        with transaction.atomic():
            locked_product = Product.objects.select_for_update().get(pk=product.pk)
            quantity_before = locked_product.stock_quantity
            quantity_after = quantity_before + quantity_delta

            if quantity_after < 0:
                return Response(
                    {'error': 'Adjustment would make stock negative.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            locked_product.stock_quantity = quantity_after
            locked_product.save(update_fields=['stock_quantity', 'status', 'updated_at'])
            movement = locked_product.record_inventory_movement(
                movement_type=ProductInventoryMovement.MovementType.MANUAL_ADJUSTMENT,
                quantity_delta=quantity_delta,
                quantity_before=quantity_before,
                quantity_after=quantity_after,
                actor=request.user,
                note=note,
                reference=reference,
            )

        log_action(request.user, 'ADJUST_PRODUCT_INVENTORY', 'product', product.id)
        return Response({
            'product': ProductSerializer(locked_product, context={'request': request}).data,
            'movement': ProductInventoryMovementSerializer(movement).data,
        })

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

    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser], url_path='upload-documents')
    def upload_documents(self, request, pk=None):
        """Upload one or more supporting documents for a product."""
        product = self.get_object()

        if not hasattr(request.user, 'vendor_profile') or product.vendor != request.user.vendor_profile:
            return Response(
                {'error': 'You do not have permission to upload documents for this product'},
                status=status.HTTP_403_FORBIDDEN
            )

        document_files = request.FILES.getlist('documents')
        if not document_files:
            return Response(
                {'error': 'No documents provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        created_documents = []
        default_type = request.data.get('document_type', ProductDocument.DocumentType.OTHER)
        default_visibility = str(request.data.get('is_public', 'true')).lower() not in {'false', '0', 'no'}
        title_prefix = request.data.get('title_prefix', '').strip()

        for idx, document_file in enumerate(document_files):
            document = ProductDocument.objects.create(
                product=product,
                file=document_file,
                document_type=request.data.get(f'document_type_{idx}', default_type) or ProductDocument.DocumentType.OTHER,
                title=request.data.get(f'title_{idx}', '') or title_prefix or document_file.name,
                description=request.data.get(f'description_{idx}', ''),
                is_public=str(request.data.get(f'is_public_{idx}', default_visibility)).lower() not in {'false', '0', 'no'},
            )
            created_documents.append(document)

        serializer = ProductDocumentSerializer(created_documents, many=True, context={'request': request})
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

                    category_field = (row.get('category') or row.get('Category') or '').strip()
                    category = None
                    if category_field:
                        category = Category.objects.filter(
                            models.Q(name__iexact=category_field) | models.Q(slug__iexact=category_field),
                            taxonomy_type='MATERIAL'
                        ).first()
                        if not category:
                            raise ValueError(f"Category '{category_field}' not found. Please verify category name.")
                    else:
                        category = Category.objects.filter(taxonomy_type='MATERIAL', active=True).order_by('name').first()
                        if not category:
                            raise ValueError('No active material category exists for minimal import.')

                    # Create product
                    # Basic fields
                    product = Product.objects.create(
                        vendor=vendor,
                        category=category,
                        name=name.strip(),
                        description=row.get('description', '') or row.get('Description', '') or name.strip(),
                        short_description=row.get('short_description', '') or row.get('Short Description', ''),
                        unit=row.get('unit') or row.get('Unit') or 'unit',
                        currency=(row.get('currency') or row.get('Currency') or getattr(getattr(vendor, 'country', None), 'default_currency', None) or 'KES').upper(),
                        base_price=row.get('base_price') or row.get('Price', 0),
                        stock_quantity=int(row.get('stock_quantity') or row.get('Stock', 0) or 0),
                        brand=row.get('brand', '') or row.get('Brand', ''),
                        status='ACTIVE'
                    )
                    created_count += 1
                    if product.stock_quantity:
                        product.record_inventory_movement(
                            movement_type=ProductInventoryMovement.MovementType.IMPORT,
                            quantity_delta=product.stock_quantity,
                            quantity_before=0,
                            quantity_after=product.stock_quantity,
                            actor=request.user,
                            note='Stock created via CSV import.',
                            reference=file_obj.name,
                        )
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
        # The template intentionally contains only the minimal fields needed for import.
        headers = ['Name', 'Description', 'Price', 'Unit']
        writer.writerow(headers)

        example_row = [
            'Example Cement 50kg',
            'High strength portland cement for structural works',
            '650',
            'bag',
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
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'
    lookup_value_regex = '[0-9a-fA-F-]{36}'

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsVendorOwner()]
    def get_queryset(self):
        qs = super().get_queryset()

        # Filter by product if provided
        product_id = self.request.query_params.get('product')
        if product_id:
            qs = qs.filter(product__uuid=product_id)

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
