from django.db import models
from django.conf import settings

class Organization(models.Model):
    name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='organizations')

    def __str__(self):
        return self.name

class ApprovalWorkflow(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='workflows')
    name = models.CharField(max_length=100) # e.g. "Purchase > 10k"
    threshold_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    approver_role = models.CharField(max_length=50) # e.g. "Manager", "CFO"

    def __str__(self):
        return f"{self.name} ({self.organization.name})"

class SupplierPerformance(models.Model):
    vendor = models.OneToOneField('vendors.Vendor', on_delete=models.CASCADE, related_name='performance_score')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='evaluated_vendors')
    score = models.IntegerField(default=50) # 0-100
    last_updated = models.DateTimeField(auto_now=True)
