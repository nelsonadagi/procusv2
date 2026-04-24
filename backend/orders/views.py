from rest_framework import viewsets, permissions, status, decorators
from rest_framework.response import Response
from django.http import HttpResponse # Import HttpResponse for the test view
from django.utils import timezone
from datetime import timedelta
from .models import Order, QuoteRequest, QuoteResponse, QuoteItem, QuoteResponseItem
from .serializers import OrderSerializer, QuoteRequestSerializer, QuoteResponseSerializer, OrderItemSerializer
from rbac.permissions import HasRequiredPermission, IsVendorOwner, IsBuyer, IsOrderOwner, IsQuoteOwner
from rbac.utils import log_action
from django.db import models, transaction
from decimal import Decimal
from catalog.models import ProductInventoryMovement, Product
import json

# Temporary test view for debugging
def test_vendor_orders_view(request):
    return HttpResponse("Test View for Vendor Orders Hit!", status=200)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().prefetch_related('items')
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, HasRequiredPermission]
    required_permission = 'orders:view'
    permission_map = {
        'create': 'orders:create',
        'update': 'orders:update',
        'partial_update': 'orders:update',
        'destroy': 'orders:cancel',
    }

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_staff:
            return qs

        # Vendors see only orders assigned to them
        if hasattr(self.request.user, 'vendor_profile'):
            return qs.filter(vendor=self.request.user.vendor_profile)

        # Buyers see only their own orders
        return qs.filter(buyer=self.request.user)

    def perform_create(self, serializer):
        from .tasks import notify_vendor_new_order
        order = serializer.save(buyer=self.request.user)
        log_action(self.request.user, 'CREATE_ORDER', 'order', order.id)
        notify_vendor_new_order.delay(order.id)

    def _resolve_vendor_origin_address(self, order):
        vendor = order.vendor
        return (
            vendor.formatted_address
            or getattr(vendor.location, 'address', None)
            or getattr(vendor.location, 'city', None)
            or vendor.location_text
            or 'Vendor dispatch location pending'
        )

    def _resolve_tracking_event_location(self, order):
        vendor = order.vendor
        return (
            vendor.location_text
            or getattr(vendor.location, 'city', None)
            or getattr(vendor.country, 'name', None)
            or 'Dispatch hub'
        )[:255]

    def _resolve_destination_address(self, order):
        if order.delivery_location:
            return (
                order.delivery_location.address
                or order.delivery_location.city
                or str(order.delivery_location)
            )

        if hasattr(order.buyer, 'buyer_profile') and order.buyer.buyer_profile.preferred_region:
            return order.buyer.buyer_profile.preferred_region

        if order.buyer.addresses.exists():
            addr = order.buyer.addresses.filter(is_default=True).first() or order.buyer.addresses.first()
            return str(addr)

        return 'Buyer delivery location pending'

    @decorators.action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsVendorOwner])
    def update_fulfillment(self, request, pk=None):
        from .tasks import notify_delivery_update
        from logistics.models import Shipment, Carrier, TrackingEvent
        order = self.get_object()
        new_status = request.data.get('status')
        valid_statuses = ['CONFIRMED', 'PACKING', 'SHIPPED', 'DELIVERED', 'CANCELLED']

        if new_status not in valid_statuses:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        order.status = new_status
        if new_status == 'SHIPPED':
            carrier_code = request.data.get('carrier_code', 'G4S')
            try:
                carrier = Carrier.objects.get(code=carrier_code)
            except Carrier.DoesNotExist:
                return Response({"error": "Invalid carrier"}, status=status.HTTP_400_BAD_REQUEST)

            destination_address = self._resolve_destination_address(order)
            origin_address = self._resolve_vendor_origin_address(order)
            tracking_event_location = self._resolve_tracking_event_location(order)

            # Create Shipment Node
            shipment, created = Shipment.objects.get_or_create(
                order=order,
                defaults={
                    'carrier': carrier,
                    'origin_address': origin_address,
                    'destination_address': destination_address,
                    'recipient_name': f"{order.buyer.first_name} {order.buyer.last_name}",
                    'recipient_phone': order.buyer.phone or "Unknown"
                }
            )
            if request.data.get('tracking_number'):
                shipment.tracking_number = request.data.get('tracking_number')
                shipment.save(update_fields=['tracking_number'])
            order.tracking_number = shipment.tracking_number

            # Initialize first tracking event
            TrackingEvent.objects.create(
                shipment=shipment,
                status='PENDING',
                location=tracking_event_location,
                description="Package received by carrier. Initializing dispatch sequence."
            )

        if new_status == 'CONFIRMED':
            order.estimated_delivery_at = (
                request.data.get('estimated_delivery_at')
                or request.data.get('estimated_delivery')
            )

        order.save()
        log_action(request.user, f'ORDER_FULFILLMENT_{new_status}', 'order', order.id)
        notify_delivery_update.delay(order.id, new_status)
        if new_status == 'CONFIRMED':
            from .tasks import notify_buyer_order_confirmed
            notify_buyer_order_confirmed.delay(order.id)

        return Response(OrderSerializer(order).data)

    @decorators.action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def confirm_delivery(self, request, pk=None):
        from .tasks import update_vendor_performance_metrics
        # Only buyer can confirm delivery
        order = self.get_object()
        if order.buyer != request.user:
            return Response({"error": "Only buyer can confirm delivery"}, status=status.HTTP_403_FORBIDDEN)

        order.buyer_confirmed_delivery = True
        order.status = 'COMPLETED'
        order.save()
        log_action(request.user, 'ORDER_COMPLETED', 'order', order.id)
        update_vendor_performance_metrics.delay(order.vendor.id)
        return Response(OrderSerializer(order).data)

    @decorators.action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsOrderOwner])
    def cancel_order(self, request, pk=None):
        order = self.get_object()
        if order.status not in ['PLACED', 'CONFIRMED']:
            return Response({"error": "Cannot cancel order in current state"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            for item in order.items.select_related('product').all():
                if not item.product:
                    continue

                locked_product = Product.objects.select_for_update().get(pk=item.product.pk)
                quantity_before = locked_product.stock_quantity
                quantity_after = quantity_before + item.quantity
                locked_product.stock_quantity = quantity_after
                locked_product.save(update_fields=['stock_quantity', 'status', 'updated_at'])
                locked_product.record_inventory_movement(
                    movement_type=ProductInventoryMovement.MovementType.ORDER_RESTOCK,
                    quantity_delta=item.quantity,
                    quantity_before=quantity_before,
                    quantity_after=quantity_after,
                    actor=request.user,
                    note=f'Stock restored from cancelled order #{order.id}.',
                    reference=f'order:{order.id}',
                )

            order.status = 'CANCELLED'
            order.save()
        log_action(request.user, 'ORDER_CANCELLED', 'order', order.id)
        return Response(OrderSerializer(order).data)

    @decorators.action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsOrderOwner])
    def initiate_dispute(self, request, pk=None):
        from disputes.models import Dispute
        order = self.get_object()
        reason = request.data.get('reason')
        if not reason:
            return Response({"error": "Reason is required"}, status=status.HTTP_400_BAD_REQUEST)

        dispute = Dispute.objects.create(
            opened_by=request.user,
            order=order,
            reason=reason
        )
        log_action(request.user, 'DISPUTE_OPENED', 'order', order.id)
        return Response({"id": dispute.id, "status": dispute.status}, status=status.HTTP_201_CREATED)

    @decorators.action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def vendor_orders(self, request):
        """Retrieve orders for the authenticated vendor."""
        if not hasattr(request.user, 'vendor_profile'):
            return Response({"detail": "User is not a vendor."}, status=status.HTTP_403_FORBIDDEN)

        vendor = request.user.vendor_profile
        queryset = self.filter_queryset(Order.objects.filter(vendor=vendor))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class QuoteRequestViewSet(viewsets.ModelViewSet):
    queryset = QuoteRequest.objects.all().prefetch_related('items')
    serializer_class = QuoteRequestSerializer
    permission_classes = [permissions.IsAuthenticated, HasRequiredPermission]
    required_permission = 'orders:view'
    permission_map = {
        'create': 'orders:create',
    }

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        if hasattr(self.request.user, 'vendor_profile'):
            return self.queryset.filter(items__product__vendor=self.request.user.vendor_profile).distinct()
        return self.queryset.filter(buyer=self.request.user)

    @decorators.action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def respond(self, request, pk=None):
        quote_request = self.get_object()

        if not hasattr(request.user, 'vendor_profile'):
            return Response({"error": "User is not a vendor"}, status=status.HTTP_403_FORBIDDEN)

        vendor = request.user.vendor_profile
        if vendor.verified_status != 'APPROVED':
            return Response({"error": "Vendor not approved"}, status=status.HTTP_403_FORBIDDEN)

        items_data = request.data.get('items', [])
        valid_until = request.data.get('valid_until')

        if isinstance(items_data, str):
            try:
                items_data = json.loads(items_data)
            except json.JSONDecodeError:
                items_data = []

        if not items_data:
            return Response({"error": "No items provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate total and validate individual items
        total_price = Decimal('0.00')
        for item in items_data:
            # item is expected to be { id: quote_item_id, unit_price: ..., availability_notes: ... }
            try:
                quote_item = QuoteItem.objects.get(id=item['id'])
                qty = quote_item.quantity
                total_price += Decimal(str(item['unit_price'])) * qty
            except QuoteItem.DoesNotExist:
                 return Response({"error": f"Quote Item {item.get('id')} not found"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the Response
        quote_response = QuoteResponse.objects.create(
            quote_request=quote_request,
            vendor=vendor,
            confirmed_price=total_price,
            delivery_fee=request.data.get('delivery_fee', 0),
            expires_at=valid_until or (timezone.now() + timedelta(days=7))
        )

        # Create Response Items
        for item in items_data:
            QuoteResponseItem.objects.create(
                quote_response=quote_response,
                quote_item_id=item['id'],
                unit_price=item['unit_price'],
                availability_notes=item.get('availability_notes', '')
            )

        quote_request.status = 'CONFIRMED'
        quote_request.save()

        log_action(request.user, 'CONFIRM_QUOTE', 'quote_request', quote_request.id)

        return Response(QuoteResponseSerializer(quote_response).data, status=status.HTTP_201_CREATED)

    @decorators.action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsQuoteOwner])
    def checkout(self, request, pk=None):
        from .models import Order, OrderItem
        from payments.models import Payment
        quote_request = self.get_object()
        response_id = request.data.get('response_id')

        try:
            quote_response = quote_request.responses.get(id=response_id)
        except QuoteResponse.DoesNotExist:
            return Response({"error": "Quote response not found"}, status=status.HTTP_404_NOT_FOUND)

        if Order.objects.filter(quote_response=quote_response).exists():
            return Response({"error": "An order has already been placed for this quote response."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            quote_items = []
            for item in quote_request.items.select_related('product').all():
                locked_product = Product.objects.select_for_update().get(pk=item.product.pk)
                if locked_product.stock_quantity < item.quantity:
                    return Response({"error": f"Insufficient stock for {locked_product.name}"}, status=status.HTTP_400_BAD_REQUEST)
                quote_items.append((item, locked_product))

            # Create Order
            total_amount = quote_response.confirmed_price + quote_response.delivery_fee
            order = Order.objects.create(
                buyer=request.user,
                vendor=quote_response.vendor,
                quote_response=quote_response,
                total_amount=total_amount,
                status='PLACED',
                payment_status='UNPAID'
            )

            # Validate Stock and Create OrderItems
            for item, locked_product in quote_items:
                OrderItem.objects.create(
                    order=order,
                    product=locked_product,
                    product_name_snapshot=locked_product.name,
                    unit_price_snapshot=locked_product.base_price,
                    quantity=item.quantity
                )
                quantity_before = locked_product.stock_quantity
                quantity_after = quantity_before - item.quantity
                locked_product.stock_quantity = quantity_after
                locked_product.save(update_fields=['stock_quantity', 'status', 'updated_at'])
                locked_product.record_inventory_movement(
                    movement_type=ProductInventoryMovement.MovementType.ORDER_COMMIT,
                    quantity_delta=-item.quantity,
                    quantity_before=quantity_before,
                    quantity_after=quantity_after,
                    actor=request.user,
                    note=f'Stock committed through checkout for order #{order.id}.',
                    reference=f'order:{order.id}',
                )

            # Create Payment Intent (Placeholder)
            Payment.objects.create(
                order=order,
                provider='MODERN_CHECKOUT',
                amount=total_amount,
                status='PENDING'
            )

        log_action(request.user, 'CHECKOUT_ORDER', 'order', order.id)
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    @decorators.action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def vendor_quotes(self, request):
        """Retrieve quote requests relevant to the authenticated vendor."""
        if not hasattr(request.user, 'vendor_profile'):
            return Response({"detail": "User is not a vendor."}, status=status.HTTP_403_FORBIDDEN)

        vendor = request.user.vendor_profile
        queryset = self.filter_queryset(QuoteRequest.objects.filter(items__product__vendor=vendor).distinct())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
