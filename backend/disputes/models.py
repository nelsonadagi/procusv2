from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Dispute(models.Model):
    class Status(models.TextChoices):
        OPENED = 'OPENED', _('🚨 Dispute Opened')
        UNDER_REVIEW = 'UNDER_REVIEW', _('🔍 Under Investigation')
        RESOLVED_RELEASE = 'RESOLVED_RELEASE', _('✅ Resolved - Release Funds')
        RESOLVED_REFUND = 'RESOLVED_REFUND', _('↩️ Resolved - Refund Client')
        CLOSED = 'CLOSED', _('📁 Case Closed')

    opened_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='opened_disputes',
        verbose_name="Opened By"
    )
    contract = models.ForeignKey(
        'contracts.Contract', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        verbose_name="Related Contract"
    )
    order = models.ForeignKey(
        'orders.Order', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        verbose_name="Related Order"
    )
    status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.OPENED,
        verbose_name="Case Status"
    )
    reason = models.TextField(
        verbose_name="Reason for Dispute",
        help_text="Describe the issue in detail"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Opened On")

    class Meta:
        verbose_name = "Dispute Case"
        verbose_name_plural = "Dispute Cases"

    def __str__(self):
        return f"Dispute #{self.id} - {self.get_status_display()}"


class EvidenceSubmission(models.Model):
    dispute = models.ForeignKey(
        Dispute, 
        on_delete=models.CASCADE, 
        related_name='evidence',
        verbose_name="For Dispute"
    )
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        verbose_name="Submitted By"
    )
    uploaded_file_url = models.URLField(
        blank=True,
        verbose_name="Document / Photo"
    )
    notes = models.TextField(
        blank=True,
        verbose_name="Explanation"
    )
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Submitted On")

    class Meta:
        verbose_name = "Evidence Document"
        verbose_name_plural = "Evidence Documents"

    def __str__(self):
        return f"Evidence from {self.submitted_by.username}"
