from django.db import models
from django.conf import settings

class PredictiveModel(models.Model):
    name = models.CharField(max_length=100) # "CreditDefault_v1"
    version = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    parameters = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.name} v{self.version}"

class UnderwritingPrediction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    model = models.ForeignKey(PredictiveModel, on_delete=models.SET_NULL, null=True)
    predicted_score = models.FloatField()
    confidence = models.FloatField()
    factors = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
