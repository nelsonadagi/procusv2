from django.db import models
from django.conf import settings

class PropertyListing(models.Model):
    class Type(models.TextChoices):
        LAND = 'LAND', 'Land'
        RESIDENTIAL = 'RESIDENTIAL', 'Residential'
        COMMERCIAL = 'COMMERCIAL', 'Commercial'
        RENOVATION = 'RENOVATION', 'Renovation'

    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        SOLD = 'SOLD', 'Sold'
        INACTIVE = 'INACTIVE', 'Inactive'

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    asset_type = models.CharField(max_length=20, choices=Type.choices)
    price_estimate = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class DevelopmentMetadata(models.Model):
    property = models.OneToOneField(PropertyListing, on_delete=models.CASCADE, related_name='development_metadata')
    zoning_info = models.CharField(max_length=255)
    build_ready = models.BooleanField(default=False)
    utilities_available = models.JSONField(default=list) # e.g. ["Water", "Power"]

class PropertyProjectLink(models.Model):
    property = models.ForeignKey(PropertyListing, on_delete=models.CASCADE, related_name='linked_projects')
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='linked_properties')
