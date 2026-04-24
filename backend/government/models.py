from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class PublicTender(models.Model):
    class Status(models.TextChoices):
        PUBLISHED = 'PUBLISHED', _('📢 Just Published')
        OPEN = 'OPEN', _('✅ Accepting Bids')
        EVALUATION = 'EVALUATION', _('🔍 Evaluating Bids')
        AWARDED = 'AWARDED', _('🏆 Contract Awarded')
        COMPLETED = 'COMPLETED', _('✅ Project Complete')

    title = models.CharField(max_length=255, verbose_name="Tender Title")
    description = models.TextField(verbose_name="Project Details")
    issuing_authority = models.CharField(
        max_length=255,
        verbose_name="Government Agency"
    )
    location = models.ForeignKey(
        'platform_settings.Location', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='tenders',
        verbose_name="Project Location"
    )
    status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.PUBLISHED,
        verbose_name="Tender Status"
    )
    bid_deadline = models.DateTimeField(verbose_name="Bid Submission Deadline")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Published On")

    class Meta:
        verbose_name = "Government Tender"
        verbose_name_plural = "Government Tenders"

    def __str__(self):
        return self.title


class AuditLog(models.Model):
    tender = models.ForeignKey(
        PublicTender, 
        on_delete=models.CASCADE, 
        related_name='audit_logs',
        verbose_name="Tender"
    )
    action = models.CharField(max_length=255, verbose_name="Action Taken")
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name="Performed By"
    )
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="When")
    details = models.TextField(verbose_name="Additional Details")

    class Meta:
        verbose_name = "Audit Log Entry"
        verbose_name_plural = "Audit Log Entries"

    def __str__(self):
        return f"{self.action} on {self.tender.title}"
