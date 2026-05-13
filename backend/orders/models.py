from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class QuoteRequest(models.Model):
    class Status(models.TextChoices):
        REQUESTED = 'REQUESTED', _('📤 Quote Requested')
        CONFIRMED = 'CONFIRMED', _('✅ Quote Received')
        REJECTED = 'REJECTED', _('❌ Request Declined')

    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='quote_requests',
        verbose_name="Requested By"
    )
    status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.REQUESTED,
        verbose_name="Request Status"
    )
    requested_at = models.DateTimeField(auto_now_add=True, verbose_name="Requested On")

    class Meta:
        verbose_name = "Price Quote Request"
        verbose_name_plural = "Price Quote Requests"


class QuoteItem(models.Model):
    quote_request = models.ForeignKey(
        QuoteRequest, 
        on_delete=models.CASCADE, 
        related_name='items',
        verbose_name="Quote Request"
    )
    product = models.ForeignKey(
        'catalog.Product', 
        on_delete=models.CASCADE,
        verbose_name="Product"
    )
    quantity = models.IntegerField(verbose_name="Quantity Needed")

    class Meta:
        verbose_name = "Quote Item"
        verbose_name_plural = "Quote Items"


class QuoteResponse(models.Model):
    quote_request = models.ForeignKey(
        QuoteRequest, 
        on_delete=models.CASCADE, 
        related_name='responses',
        verbose_name="Original Request"
    )
    vendor = models.ForeignKey(
        'vendors.Vendor', 
        on_delete=models.CASCADE,
        verbose_name="Quoted By"
    )
    confirmed_price = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        verbose_name="Quoted Price"
    )
    delivery_fee = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0.00,
        verbose_name="Delivery Fee"
    )
    expires_at = models.DateTimeField(verbose_name="Quote Expires On")
    confirmed_at = models.DateTimeField(auto_now_add=True, verbose_name="Quote Provided On")

    class Meta:
        verbose_name = "Vendor Quote"
        verbose_name_plural = "Vendor Quotes"


class QuoteResponseItem(models.Model):
    quote_response = models.ForeignKey(
        QuoteResponse, 
        on_delete=models.CASCADE, 
        related_name='items',
        verbose_name="Quote"
    )
    quote_item = models.ForeignKey(
        QuoteItem, 
        on_delete=models.CASCADE,
        verbose_name="Item"
    )
    unit_price = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        verbose_name="Unit Price"
    )
    availability_notes = models.TextField(
        blank=True,
        verbose_name="Availability / Delivery Notes"
    )

    class Meta:
        verbose_name = "Quote Line Item"
        verbose_name_plural = "Quote Line Items"


class Order(models.Model):
    class Status(models.TextChoices):
        PLACED = 'PLACED', _('🛒 Order Placed')
        CONFIRMED = 'CONFIRMED', _('✅ Confirmed by Seller')
        PACKING = 'PACKING', _('📦 Being Prepared')
        SHIPPED = 'SHIPPED', _('🚚 Out for Delivery')
        DELIVERED = 'DELIVERED', _('📬 Delivered')
        COMPLETED = 'COMPLETED', _('✨ Completed')
        CANCELLED = 'CANCELLED', _('❌ Cancelled')

    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='orders',
        verbose_name="Customer"
    )
    vendor = models.ForeignKey(
        'vendors.Vendor', 
        on_delete=models.CASCADE, 
        related_name='orders',
        verbose_name="Sold By"
    )
    quote_response = models.OneToOneField(
        QuoteResponse, 
        on_delete=models.PROTECT, 
        null=True, 
        blank=True,
        verbose_name="Based on Quote"
    )
    status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.PLACED,
        verbose_name="Order Status"
    )
    total_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        verbose_name="Total Amount"
    )
    payment_status = models.CharField(
        max_length=20, 
        default='UNPAID',
        verbose_name="Payment Status"
    )  # UNPAID, PENDING, PAID, FAILED
    delivery_location = models.ForeignKey(
        'platform_settings.Location', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='orders',
        verbose_name="Delivery Location"
    )
    
    # Fulfillment Details
    estimated_delivery_at = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name="Estimated Delivery Date"
    )
    tracking_number = models.CharField(
        max_length=100, 
        blank=True,
        verbose_name="Tracking Number"
    )
    buyer_confirmed_delivery = models.BooleanField(
        default=False,
        verbose_name="Customer Confirmed Receipt"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ordered On")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    class Meta:
        verbose_name = "Customer Order"
        verbose_name_plural = "Customer Orders"
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.buyer.username}"

    @property
    def latest_payment(self):
        return self.payments.order_by('-id').first()


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='items',
        verbose_name="Order"
    )
    product = models.ForeignKey(
        'catalog.Product',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='order_items',
        verbose_name="Product"
    )
    product_name_snapshot = models.CharField(
        max_length=255,
        verbose_name="Product Name (at time of order)"
    )
    unit_price_snapshot = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        verbose_name="Unit Price Paid"
    )
    quantity = models.IntegerField(verbose_name="Quantity")

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"

    def __str__(self):
        return f"{self.quantity} x {self.product_name_snapshot}"
