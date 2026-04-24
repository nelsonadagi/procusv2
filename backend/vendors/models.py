from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import uuid


class Vendor(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    class Status(models.TextChoices):
        PENDING = 'PENDING', _('⏳ Awaiting Approval')
        APPROVED = 'APPROVED', _('✅ Verified Partner')
        REJECTED = 'REJECTED', _('❌ Not Approved')
        SUSPENDED = 'SUSPENDED', _('🚫 Temporarily Suspended')

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vendor_profile',
        verbose_name="Account Owner"
    )
    business_name = models.CharField(max_length=255, verbose_name="Company / Business Name")
    registration_number = models.CharField(max_length=100, verbose_name="Business Registration Number")
    verified_status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Verification Status"
    )
    country = models.ForeignKey(
        'platform_settings.Country',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='vendors',
        verbose_name="Country of Operation"
    )
    location_text = models.CharField(
        max_length=255,
        db_column='location',
        null=True,
        blank=True,
        help_text="Legacy location text",
        verbose_name="Location"
    )
    location = models.ForeignKey(
        'platform_settings.Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='vendors',
        verbose_name="Business Location"
    )

    # Advanced Spatial Intelligence
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
    location_hierarchy = models.JSONField(
        default=dict,
        blank=True,
        help_text="Stores country, state, city, neighborhood etc.",
        verbose_name="Location Details"
    )

    # Logistical Capabilities
    provides_delivery = models.BooleanField(default=False, verbose_name="Offers Delivery Service")
    delivery_radius_km = models.PositiveIntegerField(default=0, verbose_name="Delivery Coverage (km)")

    categories_served = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Product Categories Offered"
    )

    # Performance Metrics
    fulfillment_rate = models.FloatField(default=0.0, verbose_name="Order Fulfillment Rate (%)")
    cancellation_rate = models.FloatField(default=0.0, verbose_name="Order Cancellation Rate (%)")
    delivery_timeliness = models.FloatField(default=0.0, verbose_name="On-Time Delivery Score (%)")
    average_rating = models.FloatField(default=0.0, verbose_name="Customer Rating (1-5)")
    total_reviews = models.PositiveIntegerField(default=0, verbose_name="Total Customer Reviews")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Joined On")

    class Meta:
        verbose_name = "Material Supplier"
        verbose_name_plural = "Material Suppliers"
        ordering = ['-created_at']

    def __str__(self):
        return self.business_name
