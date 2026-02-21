from django.db import models
from django.conf import settings

class NotificationPreference(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification_preferences')
    email_enabled = models.BooleanField(default=True)
    sms_enabled = models.BooleanField(default=False)
    push_enabled = models.BooleanField(default=True)
    
    # Category specific preferences could go here in the future
    # e.g. bids_notifications = models.BooleanField(default=True)

    def __str__(self):
        return f"Preferences for {self.user.username}"

class Notification(models.Model):
    class Type(models.TextChoices):
        BID = 'BID', 'New Bid'
        MILESTONE = 'MILESTONE', 'Milestone Update'
        PAYMENT = 'PAYMENT', 'Payment Status'
        ESCROW = 'ESCROW', 'Escrow Status'
        DISPUTE = 'DISPUTE', 'Dispute Update'
        SYSTEM = 'SYSTEM', 'System Alert'

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        SENT = 'SENT', 'Sent'
        FAILED = 'FAILED', 'Failed'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=20, choices=Type.choices, default=Type.SYSTEM)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    # Audit trail for channel
    sent_via_email = models.BooleanField(default=False)
    sent_via_sms = models.BooleanField(default=False)
    sent_via_push = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.type} for {self.user.username} - {self.subject}"
