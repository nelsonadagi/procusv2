from django.db import models
from django.conf import settings

class Dispute(models.Model):
    class Status(models.TextChoices):
        OPENED = 'OPENED', 'Opened'
        UNDER_REVIEW = 'UNDER_REVIEW', 'Under Review'
        RESOLVED_RELEASE = 'RESOLVED_RELEASE', 'Resolved Release'
        RESOLVED_REFUND = 'RESOLVED_REFUND', 'Resolved Refund'
        CLOSED = 'CLOSED', 'Closed'

    opened_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='opened_disputes')
    contract = models.ForeignKey('contracts.Contract', on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPENED)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dispute {self.id} - {self.status}"

class EvidenceSubmission(models.Model):
    dispute = models.ForeignKey(Dispute, on_delete=models.CASCADE, related_name='evidence')
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_file_url = models.URLField(blank=True) # Or FileField if using S3
    notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
