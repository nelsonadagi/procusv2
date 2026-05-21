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
from .models import ProductDocument, StockAlert
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
from notifications.services import notify_user

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
        'validate_import': 'catalog:create',
        'upload_images': 'catalog:update',
        'upload_documents': 'catalog:update',
        'adjust_inventory': 'catalog:manage_stock',
        'inventory_history': 'catalog:manage_stock',
        'category_price_stats': 'catalog:view',
        'stock_out_prediction': 'catalog:view',
        'daily_stats': 'catalog:view',
        'subscribe_stock_alert': 'catalog:view',
        'unsubscribe_stock_alert': 'catalog:view',
        'check_stock_alert': 'catalog:view',
        'similar_products': 'catalog:view',
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
            return [permissions.IsAuthenticated(), VendorApprovedOnly(), HasRequiredPermission()]
        if self.action in ['update', 'partial_update', 'destroy', 'upload_images', 'upload_documents', 'adjust_inventory', 'inventory_history']:
            return [HasRequiredPermission(), IsVendorOwner(), VendorApprovedOnly()]
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
        user = self.request.user
        if not hasattr(user, 'vendor_profile'):
            from rest_framework.exceptions import ValidationError
            raise ValidationError("User has no vendor profile.")

        vendor = user.vendor_profile
        if vendor.verified_status != 'APPROVED':
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Vendor account must be approved before publishing materials.")

        product = serializer.save(vendor=vendor)
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

    @action(detail=False, methods=['get'], url_path='dashboard-stats')
    def dashboard_stats(self, request):
        """Return aggregated vendor catalog statistics for the workspace."""
        if not hasattr(request.user, 'vendor_profile'):
            return Response({"detail": "User is not a vendor."}, status=status.HTTP_403_FORBIDDEN)

        vendor = request.user.vendor_profile
        products_qs = Product.objects.filter(vendor=vendor)
        from orders.models import QuoteItem, OrderItem, QuoteResponse

        total = products_qs.count()
        active = products_qs.filter(status='ACTIVE').count()
        draft = products_qs.filter(status='DRAFT').count()
        disabled = products_qs.filter(status='DISABLED').count()
        low_stock = products_qs.filter(status='ACTIVE', stock_quantity__gt=0, stock_quantity__lte=models.F('reorder_level')).count()
        out_of_stock = products_qs.filter(status='ACTIVE', stock_quantity__lte=0).count()
        with_images = products_qs.filter(images__isnull=False).distinct().count()
        with_certs = products_qs.filter(certification_entries__isnull=False).distinct().count()

        # Performance metrics: views, quotes, conversion
        from django.db.models import Avg
        from django.utils import timezone
        from datetime import timedelta

        thirty_days_ago = timezone.now() - timedelta(days=30)
        seven_days_ago = timezone.now() - timedelta(days=7)

        # Product views approximated from quote request volume per product
        product_uuids = list(products_qs.values_list('uuid', flat=True))
        quote_items_month = QuoteItem.objects.filter(
            product__vendor=vendor,
            quote_request__requested_at__gte=thirty_days_ago
        )
        quote_items_week = QuoteItem.objects.filter(
            product__vendor=vendor,
            quote_request__requested_at__gte=seven_days_ago
        )
        quotes_this_month = quote_items_month.values('quote_request').distinct().count()
        views_this_week = quote_items_week.values('quote_request').distinct().count()

        # Conversion: quotes that became orders
        converted_orders = OrderItem.objects.filter(
            product__vendor=vendor,
            order__created_at__gte=thirty_days_ago
        ).values('order').distinct().count()

        conversion_rate = round((converted_orders / max(quotes_this_month, 1)) * 100, 1)

        # Average quote response time
        responses = QuoteResponse.objects.filter(
            quote_request__items__product__vendor=vendor,
            confirmed_at__gte=thirty_days_ago
        )
        avg_response_time = None
        if responses.exists():
            response_times = []
            for resp in responses.select_related('quote_request'):
                if resp.quote_request.requested_at:
                    delta = (resp.confirmed_at - resp.quote_request.requested_at).total_seconds() / 3600
                    if delta >= 0:
                        response_times.append(delta)
            if response_times:
                avg_response_time = round(sum(response_times) / len(response_times), 1)

        return Response({
            'total_products': total,
            'active_products': active,
            'draft_products': draft,
            'disabled_products': disabled,
            'low_stock_count': low_stock,
            'out_of_stock_count': out_of_stock,
            'products_with_images': with_images,
            'products_with_certifications': with_certs,
            'views_this_week': views_this_week,
            'views_this_month': products_qs.filter(created_at__gte=thirty_days_ago).count(),  # Proxy metric
            'quotes_this_month': quotes_this_month,
            'conversion_rate': conversion_rate,
            'avg_response_time_hours': avg_response_time,
        })

    @action(detail=False, methods=['get'], url_path='daily-stats')
    def daily_stats(self, request):
        """Return daily quote and view counts for the last 30 days for charting."""
        if not hasattr(request.user, 'vendor_profile'):
            return Response({"detail": "User is not a vendor."}, status=status.HTTP_403_FORBIDDEN)

        vendor = request.user.vendor_profile
        from django.utils import timezone
        from datetime import timedelta
        from orders.models import QuoteItem

        days = 30
        result = []
        for i in range(days - 1, -1, -1):
            day_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=i)
            day_end = day_start + timedelta(days=1)

            quote_count = QuoteItem.objects.filter(
                product__vendor=vendor,
                quote_request__requested_at__gte=day_start,
                quote_request__requested_at__lt=day_end,
            ).values('quote_request').distinct().count()

            # Proxy views with quote requests (no separate view tracking yet)
            view_count = quote_count

            result.append({
                'date': day_start.strftime('%Y-%m-%d'),
                'quotes': quote_count,
                'views': view_count,
            })

        return Response(result)

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

    @action(detail=True, methods=['get'], url_path='timeline')
    def timeline(self, request, pk=None):
        """Return a chronological operational timeline for this product."""
        product = self.get_object()
        events = []

        # Product creation
        events.append({
            'id': f'created-{product.id}',
            'type': 'CREATED',
            'icon': '📝',
            'title': 'Product created',
            'description': f"'{product.name}' was added to your catalog.",
            'timestamp': product.created_at.isoformat() if product.created_at else None,
            'actor': None,
        })

        # Inventory movements
        for movement in product.inventory_movements.all().order_by('-created_at')[:20]:
            events.append({
                'id': f'movement-{movement.id}',
                'type': 'INVENTORY',
                'icon': '📦',
                'title': f"{movement.get_movement_type_display()}: {movement.quantity_delta:+d}",
                'description': f"Stock changed from {movement.quantity_before} to {movement.quantity_after}.",
                'timestamp': movement.created_at.isoformat() if movement.created_at else None,
                'actor': movement.actor.get_full_name() or movement.actor.username if movement.actor else None,
            })

        # Images uploaded
        for image in product.images.all().order_by('-uploaded_at')[:10]:
            events.append({
                'id': f'image-{image.id}',
                'type': 'MEDIA',
                'icon': '📸',
                'title': 'Image uploaded',
                'description': image.alt_text or 'Product image added.',
                'timestamp': image.uploaded_at.isoformat() if image.uploaded_at else None,
                'actor': None,
            })

        # Certifications
        for cert in product.certification_entries.all().order_by('-id')[:10]:
            events.append({
                'id': f'cert-{cert.id}',
                'type': 'COMPLIANCE',
                'icon': '📋',
                'title': f"Certification: {cert.display_name or cert.registry.name if cert.registry else 'Custom'}",
                'description': f"Status: {cert.get_status_display()}.",
                'timestamp': cert.issued_on.isoformat() if cert.issued_on else None,
                'actor': None,
            })

        # Stock status events
        if product.stock_quantity <= 0 and product.status == 'ACTIVE':
            events.append({
                'id': f'oos-{product.id}',
                'type': 'OUT_OF_STOCK',
                'icon': '🚫',
                'title': 'Out of stock',
                'description': f"'{product.name}' is out of stock and hidden from buyers.",
                'timestamp': product.updated_at.isoformat() if product.updated_at else None,
                'actor': None,
            })
        elif product.inventory_signal == 'LOW_STOCK':
            events.append({
                'id': f'low-{product.id}',
                'type': 'STOCK_LOW',
                'icon': '⚠️',
                'title': 'Low stock warning',
                'description': f"'{product.name}' stock is low ({product.stock_quantity} remaining).",
                'timestamp': product.updated_at.isoformat() if product.updated_at else None,
                'actor': None,
            })

        # Certification expiry events
        from django.utils import timezone
        from datetime import timedelta
        for cert in product.certification_entries.filter(expires_on__lte=timezone.now() + timedelta(days=30)):
            events.append({
                'id': f'cert-expiry-{cert.id}',
                'type': 'CERT_EXPIRING',
                'icon': '⏳',
                'title': 'Certification expiring soon',
                'description': f"{cert.display_name or cert.registry.name if cert.registry else 'Certification'} expires on {cert.expires_on}.",
                'timestamp': cert.expires_on.isoformat() if cert.expires_on else None,
                'actor': None,
            })

        # Sort by timestamp descending
        events.sort(key=lambda e: e['timestamp'] or '', reverse=True)

        return Response({'events': events})

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

        # Notify vendor if stock is now low or out of stock
        if locked_product.inventory_signal == 'LOW_STOCK':
            notify_user(
                locked_product.vendor.user,
                'SYSTEM',
                f"Low stock alert: {locked_product.name}",
                f"You have {locked_product.stock_quantity} {locked_product.unit} left. Restock soon to avoid going out of stock.",
                data={"product_uuid": str(locked_product.uuid), "action": "restock"},
            )
        elif locked_product.inventory_signal == 'OUT_OF_STOCK':
            notify_user(
                locked_product.vendor.user,
                'SYSTEM',
                f"Out of stock: {locked_product.name}",
                f"This product is now hidden from buyers. Restock to reactivate.",
                data={"product_uuid": str(locked_product.uuid), "action": "restock"},
            )

        # Notify buyers who subscribed to stock alerts when product comes back in stock
        was_out_of_stock = quantity_before <= 0
        is_now_in_stock = quantity_after > 0
        if was_out_of_stock and is_now_in_stock:
            alerts = StockAlert.objects.filter(product=locked_product, notified_at__isnull=True)
            for alert in alerts:
                notify_user(
                    alert.user,
                    'SYSTEM',
                    f"{locked_product.name} is back in stock",
                    f"The product you were watching now has {locked_product.stock_quantity} {locked_product.unit} available. Request a quote before it sells out again.",
                    data={"product_uuid": str(locked_product.uuid), "action": "view_product"},
                )
            alerts.update(notified_at=timezone.now())

        return Response({
            'product': ProductSerializer(locked_product, context={'request': request}).data,
            'movement': ProductInventoryMovementSerializer(movement).data,
        })

    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def upload_images(self, request, pk=None):
        """Upload multiple images for a product"""
        product = self.get_object()

        # Check ownership and approval
        if not hasattr(request.user, 'vendor_profile') or product.vendor != request.user.vendor_profile:
            return Response(
                {'error': 'You do not have permission to upload images for this product'},
                status=status.HTTP_403_FORBIDDEN
            )
        if request.user.vendor_profile.verified_status != 'APPROVED':
            return Response(
                {'error': 'Vendor account must be approved to upload images.'},
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
        if request.user.vendor_profile.verified_status != 'APPROVED':
            return Response(
                {'error': 'Vendor account must be approved to upload documents.'},
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

    @action(detail=True, methods=['post'], url_path='remove-document')
    def remove_document(self, request, pk=None):
        """Remove an existing document from a product."""
        product = self.get_object()
        if not hasattr(request.user, 'vendor_profile') or product.vendor != request.user.vendor_profile:
            return Response(
                {'error': 'You do not have permission to remove documents from this product'},
                status=status.HTTP_403_FORBIDDEN
            )
        if request.user.vendor_profile.verified_status != 'APPROVED':
            return Response(
                {'error': 'Vendor account must be approved to remove documents.'},
                status=status.HTTP_403_FORBIDDEN
            )

        doc_uuid = request.data.get('document_uuid')
        if not doc_uuid:
            return Response({'error': 'document_uuid is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            document = product.documents.get(uuid=doc_uuid)
            document.delete()
            return Response({'message': 'Document removed successfully.'}, status=status.HTTP_200_OK)
        except ProductDocument.DoesNotExist:
            return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser, FormParser], url_path='validate-import')
    def validate_import(self, request):
        """Validate a CSV import before committing. Returns parsed rows + errors."""
        if not hasattr(request.user, 'vendor_profile'):
            return Response({'error': 'Only vendors can validate imports'}, status=status.HTTP_403_FORBIDDEN)

        vendor = request.user.vendor_profile
        if vendor.verified_status != 'APPROVED':
            return Response({'error': 'Vendor account must be approved before importing materials.'}, status=status.HTTP_403_FORBIDDEN)

        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        if not file_obj.name.lower().endswith('.csv'):
            return Response({'error': 'Only CSV files are supported.'}, status=status.HTTP_400_BAD_REQUEST)

        def _get_val(row, *keys, default=''):
            for k in keys:
                if k in row and row[k] is not None and str(row[k]).strip() != '':
                    return str(row[k]).strip()
            return default

        def _parse_int(row, *keys, default=None):
            val = _get_val(row, *keys, default='')
            if val == '':
                return default
            try:
                return int(float(val))
            except (ValueError, TypeError):
                return default

        def _parse_decimal(row, *keys, default=None):
            val = _get_val(row, *keys, default='')
            if val == '':
                return default
            try:
                return Decimal(val.replace(',', ''))
            except (ValueError, TypeError, InvalidOperation):
                return default

        def _parse_bool(row, *keys, default=False):
            val = _get_val(row, *keys, default='').lower()
            if val in ('1', 'true', 'yes', 'y'):
                return True
            if val in ('0', 'false', 'no', 'n'):
                return False
            return default

        try:
            from decimal import Decimal, InvalidOperation
            decoded_file = file_obj.read().decode('utf-8-sig')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)

            valid_rows = []
            errors = []

            for row_idx, row in enumerate(reader, start=1):
                row_errors = []
                name = _get_val(row, 'Name', 'name', 'Product Name')
                if not name:
                    row_errors.append('Product Name is required')

                category_field = _get_val(row, 'Category', 'category')
                category = None
                if category_field:
                    category = Category.objects.filter(
                        models.Q(name__iexact=category_field) | models.Q(slug__iexact=category_field),
                        taxonomy_type='MATERIAL'
                    ).first()
                    if not category:
                        row_errors.append(f"Category '{category_field}' not found")

                base_price = _parse_decimal(row, 'Price', 'Base Price', 'base_price')
                if base_price is None or base_price < 0:
                    row_errors.append('Base Price must be a positive number')

                stock = _parse_int(row, 'Stock', 'Stock Quantity', 'stock_quantity', default=0)
                if stock is None or stock < 0:
                    row_errors.append('Stock Quantity must be a non-negative integer')

                if row_errors:
                    errors.append({'row': row_idx, 'product_name': name or '(unnamed)', 'errors': row_errors})
                else:
                    valid_rows.append({
                        'row': row_idx,
                        'name': name,
                        'category': category.name if category else category_field,
                        'base_price': str(base_price) if base_price else '0',
                        'stock_quantity': stock or 0,
                    })

            return Response({
                'valid': len(errors) == 0,
                'valid_count': len(valid_rows),
                'total_rows': len(valid_rows) + len(errors),
                'preview': valid_rows[:5],
                'errors': errors,
            })

        except Exception as e:
            return Response({'error': f'Failed to process file: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    # ------------------------------------------------------------------
    # CSV import helpers (shared between validate and import)
    # ------------------------------------------------------------------
    @staticmethod
    def _csv_get_val(row, *keys, default=''):
        for k in keys:
            if k in row and row[k] is not None and str(row[k]).strip() != '':
                return str(row[k]).strip()
        return default

    @classmethod
    def _csv_parse_int(cls, row, *keys, default=None):
        val = cls._csv_get_val(row, *keys, default='')
        if val == '':
            return default
        try:
            return int(float(val))
        except (ValueError, TypeError):
            return default

    @classmethod
    def _csv_parse_decimal(cls, row, *keys, default=None):
        from decimal import Decimal, InvalidOperation
        val = cls._csv_get_val(row, *keys, default='')
        if val == '':
            return default
        try:
            return Decimal(val.replace(',', ''))
        except (ValueError, TypeError, InvalidOperation):
            return default

    @classmethod
    def _csv_parse_bool(cls, row, *keys, default=False):
        val = cls._csv_get_val(row, *keys, default='').lower()
        if val in ('1', 'true', 'yes', 'y'):
            return True
        if val in ('0', 'false', 'no', 'n'):
            return False
        return default

    @classmethod
    def _csv_parse_date(cls, row, *keys, default=None):
        from datetime import datetime
        val = cls._csv_get_val(row, *keys, default='')
        if not val:
            return default
        for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y'):
            try:
                return datetime.strptime(val, fmt).date()
            except ValueError:
                continue
        return default

    def _parse_csv_rows(self, file_obj, vendor, dry_run=False):
        """Parse CSV rows and return (valid_rows, errors). If dry_run=True, no DB writes."""
        from decimal import Decimal
        from datetime import datetime

        decoded_file = file_obj.read().decode('utf-8-sig')
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string)

        valid_rows = []
        errors = []
        created_count = 0

        for row_idx, row in enumerate(reader, start=1):
            try:
                name = self._csv_get_val(row, 'Name', 'name', 'Product Name')
                if not name:
                    continue

                category_field = self._csv_get_val(row, 'Category', 'category')
                category = None
                if category_field:
                    category = Category.objects.filter(
                        models.Q(name__iexact=category_field) | models.Q(slug__iexact=category_field),
                        taxonomy_type='MATERIAL'
                    ).first()
                    if not category:
                        raise ValueError(f"Category '{category_field}' not found.")
                else:
                    category = Category.objects.filter(taxonomy_type='MATERIAL', active=True).order_by('name').first()
                    if not category:
                        raise ValueError('No active material category exists for import.')

                product_data = {
                    'vendor': vendor,
                    'category': category,
                    'name': name,
                    'description': self._csv_get_val(row, 'Description', 'description') or name,
                    'short_description': self._csv_get_val(row, 'Short Description', 'short_description'),
                    'unit': self._csv_get_val(row, 'Unit', 'unit') or 'unit',
                    'currency': (self._csv_get_val(row, 'Currency', 'currency') or getattr(getattr(vendor, 'country', None), 'default_currency', None) or 'KES').upper(),
                    'base_price': self._csv_parse_decimal(row, 'Price', 'Base Price', 'base_price', default=Decimal('0')),
                    'stock_quantity': self._csv_parse_int(row, 'Stock', 'Stock Quantity', 'stock_quantity', default=0) or 0,
                    'brand': self._csv_get_val(row, 'Brand', 'brand'),
                    'status': self._csv_get_val(row, 'Status', 'status') or 'ACTIVE',
                    'min_order_quantity': self._csv_parse_int(row, 'Min Order Quantity', 'min_order_quantity', 'Min Order', default=1),
                    'max_order_quantity': self._csv_parse_int(row, 'Max Order Quantity', 'max_order_quantity', 'Max Order'),
                    'bulk_price': self._csv_parse_decimal(row, 'Bulk Price', 'bulk_price'),
                    'bulk_threshold': self._csv_parse_int(row, 'Bulk Threshold', 'bulk_threshold'),
                    'reorder_level': self._csv_parse_int(row, 'Reorder Level', 'reorder_level', default=0),
                    'quality_grade': self._csv_get_val(row, 'Quality Grade', 'quality_grade'),
                    'model_number': self._csv_get_val(row, 'Model Number', 'model_number', 'SKU'),
                    'country_of_origin': self._csv_get_val(row, 'Country of Origin', 'country_of_origin'),
                    'packaging_details': self._csv_get_val(row, 'Packaging Details', 'packaging_details'),
                    'weight': self._csv_parse_decimal(row, 'Weight', 'weight'),
                    'dimensions': self._csv_get_val(row, 'Dimensions', 'dimensions'),
                    'color': self._csv_get_val(row, 'Color', 'color'),
                    'material_composition': self._csv_get_val(row, 'Material Composition', 'material_composition'),
                    'estimated_delivery_days': self._csv_parse_int(row, 'Estimated Delivery Days', 'estimated_delivery_days'),
                    'handling_instructions': self._csv_get_val(row, 'Handling Instructions', 'handling_instructions'),
                    'features': self._csv_get_val(row, 'Features', 'features'),
                    'applications': self._csv_get_val(row, 'Applications', 'applications'),
                    'certifications': self._csv_get_val(row, 'Certifications', 'certifications'),
                    'warranty_period': self._csv_get_val(row, 'Warranty Period', 'warranty_period'),
                    'meta_keywords': self._csv_get_val(row, 'Meta Keywords', 'meta_keywords'),
                    'is_featured': self._csv_parse_bool(row, 'Is Featured', 'is_featured'),
                    'is_new_arrival': self._csv_parse_bool(row, 'Is New Arrival', 'is_new_arrival'),
                    'is_on_sale': self._csv_parse_bool(row, 'Is On Sale', 'is_on_sale'),
                    'requires_special_handling': self._csv_parse_bool(row, 'Requires Special Handling', 'requires_special_handling'),
                    'shipping_weight': self._csv_parse_decimal(row, 'Shipping Weight', 'shipping_weight'),
                    'manufacturing_date': self._csv_parse_date(row, 'Manufacturing Date', 'manufacturing_date'),
                    'expiry_date': self._csv_parse_date(row, 'Expiry Date', 'expiry_date'),
                }

                # Remove None values so model defaults apply
                product_data = {k: v for k, v in product_data.items() if v is not None}

                if dry_run:
                    valid_rows.append({
                        'row': row_idx,
                        'name': name,
                        'category': category.name if category else None,
                        'base_price': str(product_data.get('base_price', '')),
                        'stock_quantity': product_data.get('stock_quantity', 0),
                        'currency': product_data.get('currency', 'KES'),
                    })
                else:
                    product = Product.objects.create(**product_data)
                    created_count += 1
                    if product.stock_quantity:
                        product.record_inventory_movement(
                            movement_type=ProductInventoryMovement.MovementType.IMPORT,
                            quantity_delta=product.stock_quantity,
                            quantity_before=0,
                            quantity_after=product.stock_quantity,
                            actor=self.request.user,
                            note='Stock created via CSV import.',
                            reference=file_obj.name,
                        )
            except Exception as e:
                errors.append({'row': row_idx, 'message': str(e)})

        return valid_rows, errors, created_count

    @action(detail=False, methods=['post'], url_path='validate-import', parser_classes=[MultiPartParser, FormParser])
    def validate_import(self, request):
        """Validate CSV import without creating products. Returns preview + errors."""
        if not hasattr(request.user, 'vendor_profile'):
            return Response({'error': 'Only vendors can validate imports'}, status=status.HTTP_403_FORBIDDEN)

        vendor = request.user.vendor_profile
        if vendor.verified_status != 'APPROVED':
            return Response({'error': 'Vendor account must be approved before importing materials.'}, status=status.HTTP_403_FORBIDDEN)

        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        if not file_obj.name.lower().endswith('.csv'):
            return Response({'error': 'Only CSV files are supported at this time.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            valid_rows, errors, _ = self._parse_csv_rows(file_obj, vendor, dry_run=True)
            return Response({
                'valid': len(errors) == 0,
                'valid_rows': valid_rows[:5],
                'total_rows': len(valid_rows),
                'errors': errors,
            })
        except Exception as e:
            return Response({'error': f'Failed to process file: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def import_products(self, request):
        """Import products from CSV file"""
        if not hasattr(request.user, 'vendor_profile'):
            return Response({'error': 'Only vendors can import products'}, status=status.HTTP_403_FORBIDDEN)

        vendor = request.user.vendor_profile
        if vendor.verified_status != 'APPROVED':
            return Response({'error': 'Vendor account must be approved before importing materials.'}, status=status.HTTP_403_FORBIDDEN)

        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        if not file_obj.name.lower().endswith('.csv'):
            return Response({'error': 'Only CSV files are supported at this time.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            _, errors, created_count = self._parse_csv_rows(file_obj, vendor, dry_run=False)
            return Response({
                'message': f'Successfully imported {created_count} products.',
                'created_count': created_count,
                'errors': errors
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': f'Failed to process file: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='category-price-stats')
    def category_price_stats(self, request):
        """Return price statistics per category for anomaly detection."""
        from django.db.models import Avg, Min, Max, Count

        stats = Product.objects.filter(
            status=Product.Status.ACTIVE,
            base_price__gt=0
        ).values('category__name', 'category__uuid', 'category_id').annotate(
            median_price=Avg('base_price'),  # Fallback to Avg; true Median needs raw SQL
            min_price=Min('base_price'),
            max_price=Max('base_price'),
            product_count=Count('id'),
            avg_price=Avg('base_price'),
        ).order_by('category__name')

        # Compute true median via raw SQL for each category
        from django.db import connection
        is_postgres = connection.vendor == 'postgresql'
        
        result = []
        for row in stats:
            cat_uuid = row['category__uuid']
            cat_id = row['category_id']
            median = None
            if is_postgres:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT percentile_cont(0.5) WITHIN GROUP (ORDER BY base_price)
                        FROM catalog_product
                        WHERE category_id = %s AND status = %s AND base_price > 0
                    """, [cat_id, Product.Status.ACTIVE])
                    median = cursor.fetchone()[0]

            result.append({
                'category': row['category__name'],
                'category_uuid': cat_uuid,
                'median_price': round(float(median or row['avg_price'] or 0), 2),
                'average_price': round(float(row['avg_price'] or 0), 2),
                'min_price': round(float(row['min_price'] or 0), 2),
                'max_price': round(float(row['max_price'] or 0), 2),
                'product_count': row['product_count'],
            })

        return Response(result)

    @action(detail=True, methods=['get'], url_path='stock-out-prediction')
    def stock_out_prediction(self, request, pk=None):
        """Predict days until stock runs out based on recent quote volume."""
        from django.utils import timezone
        from datetime import timedelta
        from django.db.models import Sum

        product = self.get_object()

        # Look at quote requests in the last 30 days
        since = timezone.now() - timedelta(days=30)
        quote_items = product.quoteitem_set.filter(
            quote_request__requested_at__gte=since
        )

        total_quoted_qty = quote_items.aggregate(total=Sum('quantity'))['total'] or 0
        days = 30

        if total_quoted_qty <= 0:
            return Response({
                'current_stock': product.stock_quantity,
                'daily_quote_rate': 0,
                'days_until_stockout': None,
                'message': 'No recent quote activity. Stock level is stable.',
            })

        daily_rate = total_quoted_qty / days
        days_left = product.stock_quantity / daily_rate if daily_rate > 0 else None

        return Response({
            'current_stock': product.stock_quantity,
            'daily_quote_rate': round(daily_rate, 2),
            'days_until_stockout': round(days_left, 1) if days_left is not None else None,
            'message': (
                f"At current quote volume, you'll run out in ~{round(days_left)} days."
                if days_left and days_left <= 14 else
                f"Stock healthy. ~{round(days_left)} days remaining at current quote rate."
                if days_left else "Stock level stable."
            ),
        })

    @action(detail=True, methods=['post'], url_path='subscribe-stock-alert', permission_classes=[permissions.IsAuthenticated])
    def subscribe_stock_alert(self, request, pk=None):
        """Subscribe to be notified when this product comes back in stock."""
        product = self.get_object()
        alert, created = StockAlert.objects.get_or_create(
            product=product,
            user=request.user,
        )
        return Response({
            'status': 'subscribed',
            'created': created,
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='unsubscribe-stock-alert', permission_classes=[permissions.IsAuthenticated])
    def unsubscribe_stock_alert(self, request, pk=None):
        """Unsubscribe from stock alerts for this product."""
        product = self.get_object()
        deleted, _ = StockAlert.objects.filter(product=product, user=request.user).delete()
        return Response({
            'status': 'unsubscribed',
            'deleted': deleted > 0,
        })

    @action(detail=True, methods=['get'], url_path='check-stock-alert', permission_classes=[permissions.IsAuthenticated])
    def check_stock_alert(self, request, pk=None):
        """Check if the current user is subscribed to stock alerts for this product."""
        product = self.get_object()
        is_subscribed = StockAlert.objects.filter(product=product, user=request.user).exists()
        return Response({'is_subscribed': is_subscribed})

    @action(detail=True, methods=['get'], url_path='similar-products')
    def similar_products(self, request, pk=None):
        """Return similar products when this one is out of stock."""
        product = self.get_object()
        qs = Product.objects.filter(
            status=Product.Status.ACTIVE,
            category=product.category,
        ).exclude(
            pk=product.pk
        ).exclude(
            stock_quantity__lte=0
        ).select_related('vendor', 'category').prefetch_related('images')[:6]

        serializer = ProductListSerializer(qs, many=True, context={'request': request})
        return Response({'matches': serializer.data})

    @action(detail=False, methods=['get'])
    def download_template(self, request):
        """Download a comprehensive CSV template for product import"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="product_import_template.csv"'

        writer = csv.writer(response)

        headers = [
            'Name', 'Category', 'Description', 'Short Description',
            'Unit', 'Currency', 'Price', 'Stock',
            'Brand', 'Status', 'Min Order Quantity', 'Max Order Quantity',
            'Bulk Price', 'Bulk Threshold', 'Reorder Level',
            'Quality Grade', 'Model Number', 'Country of Origin',
            'Packaging Details', 'Weight', 'Dimensions', 'Color',
            'Material Composition', 'Estimated Delivery Days',
            'Handling Instructions', 'Features', 'Applications',
            'Certifications', 'Warranty Period', 'Meta Keywords',
            'Is Featured', 'Is New Arrival', 'Is On Sale',
            'Requires Special Handling', 'Shipping Weight',
            'Manufacturing Date', 'Expiry Date',
        ]
        writer.writerow(headers)

        # Example row 1: Construction material
        writer.writerow([
            'Portland Cement 50kg', 'Cement', 'High-strength Portland cement suitable for structural concrete, mortar, and plastering works. Complies with BS EN 197-1.',
            'Premium Portland cement for construction',
            'bag', 'KES', '750', '120',
            'Bamburi Cement', 'ACTIVE', '10', '500',
            '720', '50', '20',
            'Grade A', 'CEM-50-STD', 'Kenya',
            '50kg paper bag, palletized 40 bags per pallet',
            '50', '60x40x15', 'Grey',
            'Clinker (95%), Gypsum (5%)',
            '2',
            'Store in dry conditions. Avoid moisture contact.',
            'High early strength|Low alkali|Consistent quality',
            'Structural concrete|Block making|Plastering',
            'KEBS Certified|ISO 9001',
            '12 months',
            'cement, portland, construction, building material, bamburi',
            'TRUE', 'FALSE', 'FALSE',
            'FALSE', '52',
            '2024-01-15', '2025-01-15',
        ])

        # Example row 2: Hardware
        writer.writerow([
            'Galvanized Roofing Nails 3 Inch', 'Hardware', 'Hot-dip galvanized roofing nails with large flat head for secure sheet metal fastening. Rust-resistant.',
            'Rust-resistant galvanized roofing nails',
            'kg', 'KES', '180', '50',
            'Devki Steel', 'ACTIVE', '1', '100',
            '160', '10', '5',
            'Standard', 'RN-3-GALV', 'Kenya',
            '1kg box, 25 boxes per carton',
            '1', '8x8x10', 'Silver',
            'Carbon steel, zinc coating',
            '1',
            'Keep dry to prevent surface oxidation.',
            'Corrosion resistant|Large flat head|Sharp point',
            'Roofing installation|Sheet metal work',
            'KEBS Certified',
            '6 months',
            'roofing nails, galvanized, hardware, steel nails',
            'FALSE', 'TRUE', 'FALSE',
            'FALSE', '1.2',
            '', '',
        ])

        # Example row 3: Minimal required fields only
        writer.writerow([
            'Timber Pine Plank 2x4', 'Timber', 'Kiln-dried pine timber plank suitable for framing and general carpentry.',
            '',
            'piece', 'KES', '450', '0',
            '', 'ACTIVE', '1', '',
            '', '', '',
            '', '', '',
            '', '', '',
            '', '', '',
            '', '', '',
            '', '', '',
            '', '', '',
            'FALSE', 'FALSE', 'FALSE',
            'FALSE', '',
            '', '',
        ])

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
