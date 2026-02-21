from django.db import models
from django.conf import settings

class KYCVerification(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        SUBMITTED = 'SUBMITTED', 'Submitted'
        VERIFIED = 'VERIFIED', 'Verified'
        REJECTED = 'REJECTED', 'Rejected'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='kyc_records')
    document_type = models.CharField(max_length=50) # Passport, ID
    document_number = models.CharField(max_length=100)
    document_url = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    submitted_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True, blank=True)

class JurisdictionRule(models.Model):
    region_code = models.CharField(max_length=10) # US, KE, UK
    currency = models.CharField(max_length=10) # USD, KES
    vat_rate = models.DecimalField(max_digits=5, decimal_places=2) # 16.00
    data_residency_required = models.BooleanField(default=False)
