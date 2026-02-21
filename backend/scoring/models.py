from django.db import models
from django.conf import settings

class ReliabilityScore(models.Model):
    class RiskTier(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reliability_score')
    score = models.IntegerField(default=50) # 0-100
    risk_tier = models.CharField(max_length=10, choices=RiskTier.choices, default=RiskTier.MEDIUM)
    eligibility_flag = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.score}"
