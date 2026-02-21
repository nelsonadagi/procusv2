from django.db import models
from django.conf import settings

class RiskScore(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='risk_profile')
    fraud_score = models.IntegerField(default=0) # 0-100, high is bad
    last_updated = models.DateTimeField(auto_now=True)

class ComplianceAlert(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=100) # PEP_MATCH, SANCTION_MATCH
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
