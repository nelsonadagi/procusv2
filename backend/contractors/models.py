from django.db import models
from django.conf import settings

class ContractorProfile(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contractor_profile')
    company_name = models.CharField(max_length=255)
    service_categories = models.JSONField(help_text="List of service categories e.g. ['Masonry', 'Electrical']")
    operating_region = models.CharField(max_length=255)
    verified_status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    rating_avg = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name

class ContractorCertification(models.Model):
    contractor = models.ForeignKey(ContractorProfile, on_delete=models.CASCADE, related_name='certifications')
    document_type = models.CharField(max_length=100)
    document_url = models.URLField()
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.contractor.company_name} - {self.document_type}"
