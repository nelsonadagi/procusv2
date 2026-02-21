from django.db import models
from django.conf import settings

class SecondaryTrade(models.Model):
    class Status(models.TextChoices):
        REQUESTED = 'REQUESTED', 'Requested'
        APPROVED = 'APPROVED', 'Approved'
        COMPLETED = 'COMPLETED', 'Completed'
        REJECTED = 'REJECTED', 'Rejected'

    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sales')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='purchases', null=True)
    investment_agreement = models.ForeignKey('regulation.InvestmentAgreement', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.REQUESTED)
    created_at = models.DateTimeField(auto_now_add=True)

class StakeTransfer(models.Model):
    trade = models.OneToOneField(SecondaryTrade, on_delete=models.CASCADE)
    executed_at = models.DateTimeField(auto_now_add=True)
    regulatory_approval_reference = models.CharField(max_length=255)
