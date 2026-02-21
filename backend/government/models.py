from django.db import models
from django.conf import settings

class PublicTender(models.Model):
    class Status(models.TextChoices):
        PUBLISHED = 'PUBLISHED', 'Published'
        OPEN = 'OPEN', 'Open for Bids'
        EVALUATION = 'EVALUATION', 'Evaluation'
        AWARDED = 'AWARDED', 'Awarded'
        COMPLETED = 'COMPLETED', 'Completed'

    title = models.CharField(max_length=255)
    description = models.TextField()
    issuing_authority = models.CharField(max_length=255) # e.g. "Ministry of Transport"
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PUBLISHED)
    bid_deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class AuditLog(models.Model):
    tender = models.ForeignKey(PublicTender, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=255)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField()
