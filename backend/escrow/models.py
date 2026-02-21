from django.db import models
from django.conf import settings

class EscrowAccount(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        RELEASED = 'RELEASED', 'Released'
        CLOSED = 'CLOSED', 'Closed'

    contract = models.OneToOneField('contracts.Contract', on_delete=models.CASCADE, related_name='escrow_account')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='escrow_accounts')
    total_amount_held = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=10, default='USD')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Escrow {self.id} for {self.contract.title}"

class EscrowTransaction(models.Model):
    class Type(models.TextChoices):
        DEPOSIT = 'DEPOSIT', 'Deposit'
        RELEASE = 'RELEASE', 'Release'
        REFUND = 'REFUND', 'Refund'

    escrow_account = models.ForeignKey(EscrowAccount, on_delete=models.CASCADE, related_name='transactions')
    type = models.CharField(max_length=20, choices=Type.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    milestone = models.ForeignKey('milestones.Milestone', on_delete=models.SET_NULL, null=True, blank=True)
    payment_reference = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class EscrowRelease(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        COMPLETED = 'COMPLETED', 'Completed'

    milestone = models.OneToOneField('milestones.Milestone', on_delete=models.CASCADE, related_name='escrow_release')
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    released_amount = models.DecimalField(max_digits=12, decimal_places=2)
    release_status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    released_at = models.DateTimeField(null=True, blank=True)

class EscrowHold(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        Lifted = 'LIFTED', 'Lifted'

    escrow_account = models.ForeignKey(EscrowAccount, on_delete=models.CASCADE, related_name='holds')
    dispute = models.ForeignKey('disputes.Dispute', on_delete=models.CASCADE)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
