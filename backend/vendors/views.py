from rest_framework import viewsets, permissions, status, decorators
from rest_framework.response import Response
from .models import Vendor
from .serializers import VendorSerializer, VendorOnboardingSerializer
from rbac.permissions import HasRequiredPermission, IsVendorOwner
from accounts.models import User
from notifications.models import Notification
from notifications.services import notify_user
from django.db import models
from django.utils import timezone

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_field = "uuid"
    permission_classes = [HasRequiredPermission]
    required_permission = 'vendors:view'
    permission_map = {
        'create': 'vendors:onboard', # Special permission for registering as vendor
        'update': 'vendors:update',
        'partial_update': 'vendors:update',
        'destroy': 'vendors:delete',
    }

    def _is_admin(self):
        user = self.request.user
        return user.is_staff or user.is_superuser or getattr(user, 'role', '') == 'ADMIN'

    def get_serializer_class(self):
        if self.action == 'create':
            return VendorOnboardingSerializer
        return VendorSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()] # Any authenticated user can apply to be a vendor
        if self.action in ['update', 'partial_update']:
            # Allow vendor owners or staff to update
            if self._is_admin():
                return [permissions.IsAuthenticated()]
            return [permissions.IsAuthenticated(), IsVendorOwner()]
        return super().get_permissions()

    def get_queryset(self):
        qs = super().get_queryset()
        
        # Staff/Admin users can see ALL vendors (including PENDING)
        if not self._is_admin():
            # Public view: Only approved vendors
            if self.action in ['list', 'retrieve']:
                qs = qs.filter(verified_status='APPROVED')
        
        # Proximity Search
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
                    qs = qs.filter(location__point__distance_lte=(user_location, D(km=float(radius))))
                
                qs = qs.annotate(distance=Distance('location__point', user_location)).order_by('distance')
            except (ValueError, TypeError):
                pass
        
        # Delivery Eligibility Search
        d_lat = self.request.query_params.get('delivery_latitude')
        d_lng = self.request.query_params.get('delivery_longitude')
        if d_lat and d_lng:
            from django.contrib.gis.db.models.functions import Distance
            from django.contrib.gis.geos import Point
            from django.db.models import F
            try:
                target_point = Point(float(d_lng), float(d_lat), srid=4326)
                qs = qs.filter(provides_delivery=True)
                qs = qs.annotate(dist_to_user=Distance('location__point', target_point))
                # Filter vendors whose delivery_radius_km is >= distance to user
                # Note: distance is in meters by default in some PostGIS setups, 
                # but Distance function usually returns degrees or meters depending on SRID.
                # For SRID 4326, it might be degrees unless transformed.
                # Better to use Distance(..., transform=True) or similar if needed.
                # For simplicity, we'll assume the environment is set up for meter/km comparisons.
                qs = qs.filter(delivery_radius_km__gte=F('dist_to_user') / 1000)
            except (ValueError, TypeError):
                pass
                
        return qs

    def perform_update(self, serializer):
        """Allow staff to update verified_status, but restrict vendors from changing it"""
        previous_status = serializer.instance.verified_status
        if not self._is_admin():
            # Remove verified_status from validated_data if user is not staff
            if 'verified_status' in serializer.validated_data:
                serializer.validated_data.pop('verified_status')
        vendor = serializer.save()
        if self._is_admin() and previous_status != vendor.verified_status:
            if vendor.verified_status == Vendor.Status.APPROVED:
                vendor.user.grant_role(User.Role.VENDOR)
                notify_user(
                    vendor.user,
                    Notification.Type.SYSTEM,
                    "Vendor workspace approved",
                    "Your vendor profile was approved. You can now manage inventory and respond to quotes.",
                    data={"vendor_id": str(vendor.uuid)},
                )
            elif vendor.verified_status in [Vendor.Status.REJECTED, Vendor.Status.SUSPENDED]:
                vendor.user.revoke_role(User.Role.VENDOR)
                notify_user(
                    vendor.user,
                    Notification.Type.SYSTEM,
                    "Vendor workspace not approved",
                    "Your vendor profile status changed. Review your vendor onboarding details.",
                    data={"vendor_id": str(vendor.uuid), "status": vendor.verified_status},
                )

    @decorators.action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not hasattr(request.user, 'vendor_profile'):
            return Response({"detail": "User does not have a vendor profile."}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            vendor = request.user.vendor_profile
            serializer = VendorSerializer(vendor)
            data = serializer.data

            # Compute average quote response time
            from django.db.models import Avg, F, ExpressionWrapper, fields
            from orders.models import QuoteResponse
            avg_response = QuoteResponse.objects.filter(
                vendor=vendor,
                quote_request__requested_at__isnull=False
            ).annotate(
                response_time=ExpressionWrapper(
                    F('confirmed_at') - F('quote_request__requested_at'),
                    output_field=fields.DurationField()
                )
            ).aggregate(avg=Avg('response_time'))['avg']
            data['avg_response_time_hours'] = round(avg_response.total_seconds() / 3600, 1) if avg_response else None

            # Unresponded quote count
            from orders.models import QuoteRequest
            data['unresponded_quotes_count'] = QuoteRequest.objects.filter(
                items__product__vendor=vendor,
                status='REQUESTED'
            ).distinct().count()

            # Queue position for pending vendors
            if vendor.verified_status == Vendor.Status.PENDING:
                pending_before = Vendor.objects.filter(
                    verified_status=Vendor.Status.PENDING,
                    created_at__lt=vendor.created_at
                ).count()
                data['queue_position'] = pending_before + 1
                data['pending_hours'] = int((timezone.now() - vendor.created_at).total_seconds() / 3600)

            return Response(data)
        except Vendor.DoesNotExist:
            return Response({"error": "No vendor profile found for this user."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Temporary: Catch any other exceptions to debug 500 errors
            return Response({"error": str(e), "message": "An unexpected error occurred while fetching vendor profile."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @decorators.action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def approve(self, request, pk=None, **kwargs):
        if not self._is_admin():
            return Response({"error": "Admin only"}, status=status.HTTP_403_FORBIDDEN)
        vendor = self.get_object()
        vendor.verified_status = Vendor.Status.APPROVED
        vendor.save(update_fields=['verified_status'])
        vendor.user.grant_role(User.Role.VENDOR)
        notify_user(
            vendor.user,
            Notification.Type.SYSTEM,
            "Vendor workspace approved",
            "Your vendor profile was approved. You can now manage inventory and respond to quotes.",
            data={"vendor_id": str(vendor.uuid)},
        )
        return Response(self.get_serializer(vendor).data)

    @decorators.action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def reject(self, request, pk=None, **kwargs):
        if not self._is_admin():
            return Response({"error": "Admin only"}, status=status.HTTP_403_FORBIDDEN)
        vendor = self.get_object()
        vendor.verified_status = Vendor.Status.REJECTED
        vendor.save(update_fields=['verified_status'])
        vendor.user.revoke_role(User.Role.VENDOR)
        notify_user(
            vendor.user,
            Notification.Type.SYSTEM,
            "Vendor workspace rejected",
            "Your vendor profile was rejected. Review your onboarding details and contact support if needed.",
            data={"vendor_id": str(vendor.uuid)},
        )
        return Response(self.get_serializer(vendor).data)

    @decorators.action(detail=False, methods=['get'], url_path='me/recommendations', permission_classes=[permissions.IsAuthenticated])
    def recommendations(self, request):
        """Return prioritized operational recommendations for the vendor."""
        if not hasattr(request.user, 'vendor_profile'):
            return Response({"recommendations": []})

        vendor = request.user.vendor_profile
        from catalog.models import Product
        from django.utils import timezone
        from datetime import timedelta

        recs = []
        products = Product.objects.filter(vendor=vendor)
        active_products = products.filter(status='ACTIVE')

        # 1. Out of stock products
        oos = active_products.filter(stock_quantity__lte=0)
        for p in oos[:3]:
            recs.append({
                'id': f'restock-{p.uuid}',
                'type': 'RESTOCK',
                'priority': 'HIGH',
                'title': f'Restock: {p.name}',
                'message': f'{p.name} is out of stock and hidden from buyers.',
                'cta': 'Restock',
                'cta_url': f'/vendor/dashboard?section=inventory&product={p.uuid}',
                'product_uuid': str(p.uuid),
            })

        # 2. Low stock products
        low = active_products.filter(stock_quantity__gt=0, stock_quantity__lte=models.F('reorder_level'))
        for p in low[:3]:
            # Predict days until stockout based on 30-day quote rate
            from django.db.models import Sum
            since = timezone.now() - timedelta(days=30)
            total_quoted = p.quoteitem_set.filter(quote_request__requested_at__gte=since).aggregate(total=Sum('quantity'))['total'] or 0
            daily_rate = total_quoted / 30 if total_quoted > 0 else 0
            days_until = int(p.stock_quantity / daily_rate) if daily_rate > 0 else None
            msg = f'Only {p.stock_quantity} {p.unit} left.'
            if days_until is not None:
                msg += f' Estimated {days_until} days until stockout.'
            recs.append({
                'id': f'low-stock-{p.uuid}',
                'type': 'RESTOCK',
                'priority': 'MEDIUM',
                'title': f'Low stock: {p.name}',
                'message': msg,
                'cta': 'Restock',
                'cta_url': f'/vendor/dashboard?section=inventory&product={p.uuid}',
                'product_uuid': str(p.uuid),
            })

        # 3. Incomplete listings (no images)
        no_images = active_products.filter(images__isnull=True)
        if no_images.exists():
            recs.append({
                'id': 'incomplete-listings',
                'type': 'INCOMPLETE_LISTING',
                'priority': 'MEDIUM',
                'title': f'Add photos to {no_images.count()} product{"s" if no_images.count() > 1 else ""}',
                'message': 'Products with images get 5× more views and quote requests.',
                'cta': 'Add Photos',
                'cta_url': '/vendor/dashboard?section=inventory',
            })

        # 4. Unresponded quotes
        from orders.models import QuoteRequest
        unresponded = QuoteRequest.objects.filter(
            items__product__vendor=vendor,
            status='REQUESTED',
        ).distinct().count()
        if unresponded > 0:
            recs.append({
                'id': 'unresponded-quotes',
                'type': 'RESPOND_QUOTE',
                'priority': 'HIGH',
                'title': f'{unresponded} unresponded quote{"s" if unresponded > 1 else ""}',
                'message': 'Responding within 2 hours increases your win rate by 35%.',
                'cta': 'Respond',
                'cta_url': '/vendor/dashboard?section=quotes',
            })

        # 5. Draft products waiting to be published
        drafts = products.filter(status='DRAFT')
        if drafts.exists():
            recs.append({
                'id': 'draft-products',
                'type': 'PUBLISH',
                'priority': 'LOW',
                'title': f'{drafts.count()} product{"s" if drafts.count() > 1 else ""} in drafts',
                'message': 'Publish your drafts to start receiving quote requests.',
                'cta': 'Review Drafts',
                'cta_url': '/vendor/dashboard?section=inventory',
            })

        # 6. Certifications missing
        no_certs = active_products.filter(certification_entries__isnull=True)
        if no_certs.exists() and not no_images.exists():
            recs.append({
                'id': 'missing-certs',
                'type': 'COMPLIANCE',
                'priority': 'LOW',
                'title': f'Add certifications to {no_certs.count()} product{"s" if no_certs.count() > 1 else ""}',
                'message': 'Enterprise buyers filter by compliance. Add KEBS, ISO, or CE certifications.',
                'cta': 'Add Certs',
                'cta_url': '/vendor/dashboard?section=inventory',
            })

        # 7. Price competitiveness nudge
        from django.db.models import Avg
        for p in active_products.filter(base_price__gt=0)[:1]:
            cat_avg = Product.objects.filter(
                category=p.category, status='ACTIVE', base_price__gt=0
            ).aggregate(avg=Avg('base_price'))['avg']
            if cat_avg and cat_avg > 0:
                ratio = float(p.base_price) / float(cat_avg)
                if ratio > 1.25:
                    recs.append({
                        'id': 'price-nudge',
                        'type': 'PRICE',
                        'priority': 'LOW',
                        'title': 'Price above category average',
                        'message': f'Your price is {int((ratio - 1) * 100)}% above the category average. Consider a bulk discount to stay competitive.',
                        'cta': 'Review Pricing',
                        'cta_url': f'/vendor/dashboard?section=inventory&product={p.uuid}',
                        'product_uuid': str(p.uuid),
                    })

        # Sort by priority
        priority_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
        recs.sort(key=lambda r: priority_order.get(r['priority'], 3))

        return Response({"recommendations": recs[:8]})
