from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import uuid


class CourierProfile(models.Model):
    """
    Represents a self-registered courier/logistics provider.
    This links to the Auth User and extends the concept of a 'Carrier'.
    """
    STATUS_CHOICES = [
        ('DRAFT', '📝 Draft - Incomplete'),
        ('PENDING', '⏳ Awaiting Review'),
        ('UNDER_REVIEW', '🔍 Under Review'),
        ('APPROVED', '✅ Verified Partner'),
        ('REJECTED', '❌ Application Declined'),
        ('SUSPENDED', '🚫 Account Suspended')
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='courier_profile',
        verbose_name="Account Owner"
    )
    company_name = models.CharField(max_length=255, verbose_name="Company Name")
    registration_number = models.CharField(
        max_length=100,
        verbose_name="Business Registration Number"
    )
    tax_pin = models.CharField(
        max_length=50, 
        blank=True,
        verbose_name="Tax PIN / VAT Number"
    )
    
    # Coverage & Contact
    support_email = models.EmailField(verbose_name="Customer Support Email")
    support_phone = models.CharField(
        max_length=20,
        verbose_name="Customer Support Phone"
    )
    website = models.URLField(blank=True, verbose_name="Company Website")
    
    # Geospatial Identity
    country = models.ForeignKey(
        'platform_settings.Country', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='couriers',
        verbose_name="Country of Operation"
    )
    location = models.ForeignKey(
        'platform_settings.Location', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='couriers',
        verbose_name="Business Location"
    )
    location_text = models.CharField(
        max_length=255, 
        null=True, 
        blank=True, 
        help_text="Operational base city or region",
        verbose_name="Primary Operating Region"
    )
    
    latitude = models.DecimalField(
        max_digits=12, 
        decimal_places=9, 
        null=True, 
        blank=True,
        verbose_name="GPS Latitude"
    )
    longitude = models.DecimalField(
        max_digits=12, 
        decimal_places=9, 
        null=True, 
        blank=True,
        verbose_name="GPS Longitude"
    )
    formatted_address = models.TextField(blank=True, verbose_name="Full Address")
    
    # Operational Status
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='DRAFT',
        verbose_name="Account Status"
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name="Active for Deliveries"
    )
    
    # Validation Trail
    submitted_at = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name="Application Submitted On"
    )
    reviewed_at = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name="Review Completed On"
    )
    rejection_reason = models.TextField(
        blank=True,
        verbose_name="Reason (if rejected)"
    )
    
    logo_url = models.URLField(blank=True, verbose_name="Company Logo")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Joined On")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    class Meta:
        verbose_name = "Logistics Partner"
        verbose_name_plural = "Logistics Partners"

    def __str__(self):
        return self.company_name


class CourierDocument(models.Model):
    TYPE_CHOICES = [
        ('LICENSE', '🚛 Transport License'),
        ('INSURANCE', '🛡️ Insurance Certificate'),
        ('REGISTRATION', '📄 Business Registration'),
        ('OTHER', '📎 Other Document')
    ]
    
    courier = models.ForeignKey(
        CourierProfile, 
        on_delete=models.CASCADE, 
        related_name='documents',
        verbose_name="Belongs To"
    )
    document_type = models.CharField(
        max_length=20, 
        choices=TYPE_CHOICES,
        verbose_name="Document Type"
    )
    file = models.FileField(
        upload_to='courier_docs/',
        verbose_name="Document File"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Uploaded On")
    
    # Admin Verification
    is_verified = models.BooleanField(
        default=False,
        verbose_name="Verified by Admin"
    )
    expiry_date = models.DateField(
        null=True, 
        blank=True,
        verbose_name="Document Expires On"
    )
    admin_notes = models.TextField(blank=True, verbose_name="Admin Review Notes")

    class Meta:
        verbose_name = "Courier Document"
        verbose_name_plural = "Courier Documents"

    def __str__(self):
        return f"{self.courier.company_name} - {self.get_document_type_display()}"


class CourierApiConfig(models.Model):
    """
    Stores API credentials and endpoint mapping for a Courier's system.
    Sensitive fields should be encrypted in a real deployment (using django-fernet-fields).
    """
    courier = models.OneToOneField(
        CourierProfile, 
        on_delete=models.CASCADE, 
        related_name='api_config',
        verbose_name="For Courier"
    )
    
    # Connectivity
    base_url = models.URLField(
        help_text="Base URL for the Courier's API",
        verbose_name="API Base URL"
    )
    api_key = models.CharField(
        max_length=255, 
        blank=True, 
        help_text="Header: Authorization / X-API-Key",
        verbose_name="API Key"
    )
    api_secret = models.CharField(
        max_length=255, 
        blank=True, 
        help_text="Used for signature generation if required",
        verbose_name="API Secret"
    )
    
    # Webhook Config
    webhook_url = models.URLField(
        blank=True, 
        help_text="Where we send updates TO the courier (optional)",
        verbose_name="Our Webhook to Courier"
    )
    webhook_secret = models.CharField(
        max_length=255, 
        blank=True, 
        help_text="Secret to validate incoming webhooks FROM courier",
        verbose_name="Incoming Webhook Secret"
    )
    
    # Endpoint Mapping (Relative paths)
    create_order_endpoint = models.CharField(
        max_length=255, 
        default='/orders', 
        help_text="POST endpoint to create shipment",
        verbose_name="Create Order Endpoint"
    )
    cancel_order_endpoint = models.CharField(
        max_length=255, 
        default='/orders/cancel', 
        help_text="POST/DELETE endpoint to cancel",
        verbose_name="Cancel Order Endpoint"
    )
    track_order_endpoint = models.CharField(
        max_length=255, 
        default='/track', 
        help_text="GET endpoint to fetch status",
        verbose_name="Track Order Endpoint"
    )
    
    # Data Mapping (JSON)
    field_mapping = models.JSONField(
        default=dict, 
        blank=True, 
        help_text="Map internal fields to external API payload keys",
        verbose_name="Field Mapping"
    )
    status_mapping = models.JSONField(
        default=dict, 
        blank=True, 
        help_text="Map external status codes to internal choices",
        verbose_name="Status Code Mapping"
    )
    
    is_active = models.BooleanField(default=False, verbose_name="Active")

    class Meta:
        verbose_name = "Courier API Configuration"
        verbose_name_plural = "Courier API Configurations"

    def __str__(self):
        return f"API Config for {self.courier.company_name}"


class PricingZone(models.Model):
    TYPE_CHOICES = [
        ('POLYGON', '📍 Custom Area (Polygon)'),
        ('RADIUS', '⭕ Radius Circle')
    ]
    
    courier = models.ForeignKey(
        CourierProfile, 
        on_delete=models.CASCADE, 
        related_name='pricing_zones',
        verbose_name="For Courier"
    )
    name = models.CharField(max_length=100, verbose_name="Zone Name")
    zone_type = models.CharField(
        max_length=20, 
        choices=TYPE_CHOICES, 
        default='RADIUS',
        verbose_name="Zone Type"
    )
    
    # Geometry
    center_lat = models.FloatField(null=True, blank=True, verbose_name="Center Latitude")
    center_lng = models.FloatField(null=True, blank=True, verbose_name="Center Longitude")
    radius_km = models.FloatField(default=10.0, verbose_name="Radius (km)")
    geometry = models.JSONField(
        null=True, 
        blank=True, 
        help_text="GeoJSON Polygon if type is Polygon",
        verbose_name="Zone Geometry"
    )
    
    description = models.TextField(blank=True, verbose_name="Zone Description")

    class Meta:
        verbose_name = "Delivery Zone"
        verbose_name_plural = "Delivery Zones"

    def __str__(self):
        return f"{self.courier.company_name} - {self.name}"


class PricingRule(models.Model):
    courier = models.ForeignKey(
        CourierProfile, 
        on_delete=models.CASCADE, 
        related_name='pricing_rules',
        verbose_name="For Courier"
    )
    zone = models.ForeignKey(
        PricingZone, 
        on_delete=models.CASCADE, 
        related_name='rules',
        verbose_name="Delivery Zone"
    )
    
    # Base Cost
    base_cost = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Minimum cost for this zone",
        verbose_name="Base Delivery Fee"
    )
    
    # Weight Slabs
    min_weight = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        verbose_name="Minimum Weight (kg)"
    )
    max_weight = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=1000.00,
        verbose_name="Maximum Weight (kg)"
    )
    per_kg_cost = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        verbose_name="Price per kg"
    )
    
    # Surcharges
    express_multiplier = models.DecimalField(
        max_digits=4, 
        decimal_places=2, 
        default=1.50,
        verbose_name="Express Delivery Multiplier"
    )
    same_day_multiplier = models.DecimalField(
        max_digits=4, 
        decimal_places=2, 
        default=2.00,
        verbose_name="Same-Day Delivery Multiplier"
    )
    
    is_active = models.BooleanField(default=True, verbose_name="Active")

    class Meta:
        verbose_name = "Pricing Rule"
        verbose_name_plural = "Pricing Rules"

    def __str__(self):
        return f"{self.zone.name} ({self.min_weight}-{self.max_weight}kg)"


class Carrier(models.Model):
    name = models.CharField(max_length=100, verbose_name="Carrier Name")
    code = models.CharField(max_length=20, unique=True, verbose_name="Carrier Code")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    profile = models.OneToOneField(
        CourierProfile, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='legacy_carrier',
        verbose_name="Linked Courier Profile"
    )

    class Meta:
        verbose_name = "Legacy Carrier"
        verbose_name_plural = "Legacy Carriers"

    def __str__(self):
        return self.name


class Shipment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('📦 Awaiting Pickup')
        TRANSIT = 'IN_TRANSIT', _('🚚 In Transit')
        OUT_FOR_DELIVERY = 'OUT_FOR_DELIVERY', _('🏃 Out for Delivery')
        DELIVERED = 'DELIVERED', _('✅ Delivered')
        FAILED = 'FAILED', _('❌ Delivery Failed')
        RETURNED = 'RETURNED', _('↩️ Returned to Sender')

    order = models.OneToOneField(
        'orders.Order', 
        on_delete=models.CASCADE, 
        related_name='shipment',
        verbose_name="For Order"
    )
    
    carrier = models.ForeignKey(
        Carrier, 
        on_delete=models.PROTECT, 
        null=True, 
        blank=True,
        verbose_name="Carrier"
    )
    courier = models.ForeignKey(
        CourierProfile, 
        on_delete=models.PROTECT, 
        null=True, 
        blank=True,
        verbose_name="Logistics Partner"
    )
    
    tracking_number = models.CharField(
        max_length=100, 
        unique=True, 
        blank=True,
        verbose_name="Tracking Number"
    )
    status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.PENDING,
        verbose_name="Shipment Status"
    )
    
    # Addresses
    origin_address = models.TextField(verbose_name="Pickup Address")
    destination_address = models.TextField(verbose_name="Delivery Address")
    recipient_name = models.CharField(max_length=255, verbose_name="Recipient Name")
    recipient_phone = models.CharField(max_length=20, verbose_name="Recipient Phone")
    
    # Metrics
    weight = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        verbose_name="Package Weight (kg)"
    )
    volume = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        verbose_name="Package Volume (m³)"
    )
    service_level = models.CharField(
        max_length=50, 
        default='STANDARD',
        verbose_name="Service Level"
    )
    external_tracking_id = models.CharField(
        max_length=100, 
        blank=True,
        verbose_name="Carrier Tracking ID"
    )

    # Tracking
    current_lat = models.FloatField(null=True, blank=True, verbose_name="Current Latitude")
    current_lng = models.FloatField(null=True, blank=True, verbose_name="Current Longitude")
    last_location_update = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name="Location Last Updated"
    )
    
    expected_delivery = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name="Expected Delivery"
    )
    delivered_at = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name="Actually Delivered On"
    )
    
    class Meta:
        verbose_name = "Shipment"
        verbose_name_plural = "Shipments"

    def save(self, *args, **kwargs):
        if not self.tracking_number:
            self.tracking_number = f"PZ-{uuid.uuid4().hex[:12].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Shipment {self.tracking_number}"


class TrackingEvent(models.Model):
    shipment = models.ForeignKey(
        Shipment, 
        on_delete=models.CASCADE, 
        related_name='events',
        verbose_name="Shipment"
    )
    status = models.CharField(max_length=50, verbose_name="Status Update")
    location = models.CharField(max_length=255, verbose_name="Location")
    description = models.TextField(verbose_name="Details")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="When")
    latitude = models.FloatField(null=True, blank=True, verbose_name="GPS Latitude")
    longitude = models.FloatField(null=True, blank=True, verbose_name="GPS Longitude")
    
    # Raw payload for debugging integration issues
    raw_payload = models.JSONField(
        null=True, 
        blank=True,
        verbose_name="Raw Data (for debugging)"
    )

    class Meta:
        verbose_name = "Tracking Event"
        verbose_name_plural = "Tracking Events"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.shipment.tracking_number} - {self.status}"


class WebhookLog(models.Model):
    """
    Audit trail for incoming/outgoing webhooks to help debugging.
    """
    courier = models.ForeignKey(
        CourierProfile, 
        on_delete=models.CASCADE,
        verbose_name="Courier"
    )
    direction = models.CharField(
        max_length=10, 
        choices=[('IN', '⬇️ Incoming'), ('OUT', '⬆️ Outgoing')],
        verbose_name="Direction"
    )
    url = models.URLField(verbose_name="URL")
    payload = models.JSONField(verbose_name="Payload")
    response_code = models.IntegerField(null=True, verbose_name="Response Code")
    response_body = models.TextField(blank=True, verbose_name="Response Body")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="When")
    success = models.BooleanField(default=False, verbose_name="Successful")

    class Meta:
        verbose_name = "Webhook Log"
        verbose_name_plural = "Webhook Logs"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.direction} webhook to {self.courier.company_name}"
