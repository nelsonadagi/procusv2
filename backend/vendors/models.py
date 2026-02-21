from django.db import models
from django.conf import settings

class Vendor(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'
        SUSPENDED = 'SUSPENDED', 'Suspended'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vendor_profile')
    business_name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=100)
    verified_status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    location = models.CharField(max_length=255)
    categories_served = models.JSONField(default=list, blank=True)
    
    # Performance Metrics
    fulfillment_rate = models.FloatField(default=0.0)
    cancellation_rate = models.FloatField(default=0.0)
    delivery_timeliness = models.FloatField(default=0.0)
    average_rating = models.FloatField(default=0.0)
    total_reviews = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.business_name
