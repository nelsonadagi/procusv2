from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class EscrowAccount(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', _('🔒 Funds Secured')
        RELEASED = 'RELEASED', _('✅ Funds Released')
        CLOSED = 'CLOSED', _('📁 Account Closed')

    contract = models.OneToOneField(
        'contracts.Contract', 
        on_delete=models.CASCADE, 
        related_name='escrow_account',
        verbose_name="For Contract"
    )
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='escrow_accounts',
        verbose_name="Funded By"
    )
    total_amount_held = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0.00,
        verbose_name="Amount in Escrow"
    )
    currency = models.CharField(
        max_length=10, 
        default='USD',
        verbose_name="Currency"
    )
    status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.ACTIVE,
        verbose_name="Account Status"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created On")

    class Meta:
        verbose_name = "Escrow Account"
        verbose_name_plural = "Escrow Accounts"

    def __str__(self):
        return f"Escrow #{self.id} for {self.contract.title}"


class EscrowTransaction(models.Model):
    class Type(models.TextChoices):
        DEPOSIT = 'DEPOSIT', _('💰 Fund Deposit')
        RELEASE = 'RELEASE', _('💸 Fund Release')
        REFUND = 'REFUND', _('↩️ Refund to Client')

    escrow_account = models.ForeignKey(
        EscrowAccount, 
        on_delete=models.CASCADE, 
        related_name='transactions',
        verbose_name="Escrow Account"
    )
    type = models.CharField(
        max_length=20, 
        choices=Type.choices,
        verbose_name="Transaction Type"
    )
    amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        verbose_name="Amount"
    )
    milestone = models.ForeignKey(
        'milestones.Milestone', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Related Milestone"
    )
    payment_reference = models.CharField(
        max_length=255, 
        blank=True,
        verbose_name="Payment Reference"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Transaction Date")

    class Meta:
        verbose_name = "Escrow Transaction"
        verbose_name_plural = "Escrow Transactions"


class EscrowRelease(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('⏳ Awaiting Approval')
        COMPLETED = 'COMPLETED', _('✅ Released')

    milestone = models.OneToOneField(
        'milestones.Milestone', 
        on_delete=models.CASCADE, 
        related_name='escrow_release',
        verbose_name="For Milestone"
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name="Approved By"
    )
    released_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        verbose_name="Amount Released"
    )
    release_status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.PENDING,
        verbose_name="Release Status"
    )
    released_at = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name="Released On"
    )

    class Meta:
        verbose_name = "Fund Release"
        verbose_name_plural = "Fund Releases"


class EscrowHold(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', _('🚫 On Hold')
        LIFTED = 'LIFTED', _('✅ Hold Removed')

    escrow_account = models.ForeignKey(
        EscrowAccount, 
        on_delete=models.CASCADE, 
        related_name='holds',
        verbose_name="Escrow Account"
    )
    dispute = models.ForeignKey(
        'disputes.Dispute', 
        on_delete=models.CASCADE,
        verbose_name="Related Dispute"
    )
    reason = models.TextField(verbose_name="Reason for Hold")
    status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.ACTIVE,
        verbose_name="Hold Status"
    )

    class Meta:
        verbose_name = "Payment Hold"
        verbose_name_plural = "Payment Holds"
