from django.db import models
from django.conf import settings

class ERPConnector(models.Model):
    class Type(models.TextChoices):
        SAP = 'SAP', 'SAP'
        ORACLE = 'ORACLE', 'Oracle'
        QUICKBOOKS = 'QUICKBOOKS', 'QuickBooks'

    organization = models.ForeignKey('enterprise.Organization', on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=Type.choices)
    api_endpoint = models.URLField()
    auth_credentials = models.JSONField() # Encrypt in real world
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.type} - {self.organization.name}"

class ExternalSystemSync(models.Model):
    connector = models.ForeignKey(ERPConnector, on_delete=models.CASCADE)
    entity_type = models.CharField(max_length=50) # Invoice, PO
    entity_id = models.CharField(max_length=100)
    sync_status = models.CharField(max_length=20) # SUCCESS, FAILED
    timestamp = models.DateTimeField(auto_now_add=True)
