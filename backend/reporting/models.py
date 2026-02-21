from django.db import models
from django.conf import settings

class RegulatoryReport(models.Model):
    class Type(models.TextChoices):
        AML_SAR = 'AML_SAR', 'Suspicious Activity Report'
        TAX_VAT = 'TAX_VAT', 'VAT Filing'
        AUDIT_LOG = 'AUDIT_LOG', 'Audit Log'

    type = models.CharField(max_length=20, choices=Type.choices)
    jurisdiction = models.CharField(max_length=100)
    report_data = models.JSONField()
    generated_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, default='GENERATED')

class TaxFiling(models.Model):
    organization = models.ForeignKey('enterprise.Organization', on_delete=models.CASCADE)
    period = models.CharField(max_length=50) # Q1 2026
    tax_amount = models.DecimalField(max_digits=14, decimal_places=2)
    filing_reference = models.CharField(max_length=255)
