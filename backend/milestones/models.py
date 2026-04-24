from django.db import models
from django.utils.translation import gettext_lazy as _


class Milestone(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('📋 Not Started')
        COMPLETED = 'COMPLETED', _('✅ Work Completed')
        APPROVED = 'APPROVED', _('👍 Client Approved')
        PAID = 'PAID', _('💰 Payment Released')

    contract = models.ForeignKey(
        'contracts.Contract', 
        on_delete=models.CASCADE, 
        related_name='milestones',
        verbose_name="Part of Contract"
    )
    title = models.CharField(max_length=255, verbose_name="Milestone Name")
    description = models.TextField(
        blank=True,
        verbose_name="What's to be Delivered"
    )
    amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        verbose_name="Payment Amount"
    )
    due_date = models.DateField(verbose_name="Expected Completion Date")
    status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.PENDING,
        verbose_name="Milestone Status"
    )

    class Meta:
        verbose_name = "Project Milestone"
        verbose_name_plural = "Project Milestones"

    def __str__(self):
        return f"{self.title} ({self.contract.title})"


class MilestonePayment(models.Model):
    milestone = models.OneToOneField(
        Milestone, 
        on_delete=models.CASCADE, 
        related_name='payment',
        verbose_name="Milestone"
    )
    payment_reference = models.CharField(
        max_length=255, 
        blank=True,
        verbose_name="Payment Reference Number"
    )
    release_status = models.CharField(
        max_length=50, 
        default='PENDING',
        verbose_name="Payment Status"
    )

    class Meta:
        verbose_name = "Milestone Payment"
        verbose_name_plural = "Milestone Payments"

    def __str__(self):
        return f"Payment for {self.milestone.title}"
