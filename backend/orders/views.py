from rest_framework import viewsets, permissions, status, decorators
from rest_framework.response import Response
from .models import Order, QuoteRequest, QuoteResponse
from .serializers import OrderSerializer, QuoteRequestSerializer, QuoteResponseSerializer, OrderItemSerializer
from rbac.permissions import HasRequiredPermission, IsVendorOwner, IsBuyer, IsOrderOwner, IsQuoteOwner
from rbac.utils import log_action
from django.db import models

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().prefetch_related('items')
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    # required_permission = 'orders:view' # Disabled to allow buyers access
    permission_map = {
        'create': 'orders:create',
        'update': 'orders:update',
        'partial_update': 'orders:update',
        'destroy': 'orders:delete',
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

    @decorators.action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsVendorOwner])
    def update_fulfillment(self, request, pk=None):
        from .tasks import notify_delivery_update
        order = self.get_object()
        new_status = request.data.get('status')
        valid_statuses = ['CONFIRMED', 'PACKING', 'SHIPPED', 'DELIVERED', 'CANCELLED']
        
        if new_status not in valid_statuses:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = new_status
        if new_status == 'SHIPPED':
            order.tracking_number = request.data.get('tracking_number', '')
        if new_status == 'CONFIRMED':
            order.estimated_delivery_at = request.data.get('estimated_delivery_at')
            
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

class QuoteRequestViewSet(viewsets.ModelViewSet):
    queryset = QuoteRequest.objects.all().prefetch_related('items')
    serializer_class = QuoteRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

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
            
        serializer = QuoteResponseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(quote_request=quote_request, vendor=vendor)
            quote_request.status = 'CONFIRMED'
            quote_request.save()
            log_action(request.user, 'CONFIRM_QUOTE', 'quote_request', quote_request.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        for item in quote_request.items.all():
            if item.product.stock_quantity < item.quantity:
                return Response({"error": f"Insufficient stock for {item.product.name}"}, status=status.HTTP_400_BAD_REQUEST)
            
            OrderItem.objects.create(
                order=order,
                product_name_snapshot=item.product.name,
                unit_price_snapshot=item.product.base_price,
                quantity=item.quantity
            )
            # Update Stock
            item.product.stock_quantity -= item.quantity
            item.product.save()
            
        # Create Payment Intent (Placeholder)
        Payment.objects.create(
            order=order,
            provider='MODERN_CHECKOUT',
            amount=total_amount,
            status='PENDING'
        )
        
        log_action(request.user, 'CHECKOUT_ORDER', 'order', order.id)
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
