from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class ContractorProfile(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('⏳ Application Under Review')
        APPROVED = 'APPROVED', _('✅ Verified Professional')
        REJECTED = 'REJECTED', _('❌ Application Declined')

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='contractor_profile',
        verbose_name="Account Owner"
    )
    company_name = models.CharField(max_length=255, verbose_name="Company / Business Name")
    service_categories = models.JSONField(
        help_text="List of services offered, e.g. ['Masonry', 'Electrical', 'Plumbing']",
        verbose_name="Services Offered"
    )
    
    # Location Intelligence
    country = models.ForeignKey(
        'platform_settings.Country', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='contractors',
        verbose_name="Country of Operation"
    )
    location_text = models.CharField(
        max_length=255, 
        db_column='operating_region', 
        null=True, 
        blank=True,
        verbose_name="Primary Work Area"
    )
    location = models.ForeignKey(
        'platform_settings.Location', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='contractors',
        verbose_name="Business Location"
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
    
    service_radius_km = models.PositiveIntegerField(
        default=0,
        verbose_name="Service Coverage Radius (km)"
    )
    verified_status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.PENDING,
        verbose_name="Verification Status"
    )
    rating_avg = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0.00,
        verbose_name="Average Customer Rating"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Joined On")

    class Meta:
        verbose_name = "Construction Professional"
        verbose_name_plural = "Construction Professionals"
        ordering = ['-created_at']

    def __str__(self):
        return self.company_name


class ContractorCertification(models.Model):
    contractor = models.ForeignKey(
        ContractorProfile, 
        on_delete=models.CASCADE, 
        related_name='certifications',
        verbose_name="Belongs To"
    )
    document_type = models.CharField(
        max_length=100,
        verbose_name="Certificate Type"
    )
    document_url = models.URLField(verbose_name="Document Link")
    verified = models.BooleanField(default=False, verbose_name="Verified by Admin")

    class Meta:
        verbose_name = "Professional Certification"
        verbose_name_plural = "Professional Certifications"

    def __str__(self):
        return f"{self.contractor.company_name} - {self.document_type}"
