from django.db import models
from django.conf import settings

class BankAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bank_accounts')
    bank_name = models.CharField(max_length=255)
    account_number_last4 = models.CharField(max_length=4)
    routing_number = models.CharField(max_length=100)
    currency = models.CharField(max_length=10, default='USD')
    is_verified = models.BooleanField(default=False)
    external_id = models.CharField(max_length=255, blank=True) # Stripe/Plaid ID

    def __str__(self):
        return f"{self.bank_name} ****{self.account_number_last4}"

class SettlementTransaction(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PROCESSED = 'PROCESSED', 'Processed'
        FAILED = 'FAILED', 'Failed'

    escrow_transaction = models.ForeignKey('escrow.EscrowTransaction', on_delete=models.SET_NULL, null=True, blank=True)
    destination_account = models.ForeignKey(BankAccount, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    reference = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
