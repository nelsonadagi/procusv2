from .models import Notification, NotificationPreference
from django.utils import timezone

def notify_user(user, notification_type, subject, message):
    """
    Central entry point for sending notifications.
    It checks preferences and logs the notification.
    """
    prefs, _ = NotificationPreference.objects.get_or_create(user=user)
    
    notification = Notification.objects.create(
        user=user,
        type=notification_type,
        subject=subject,
        message=message,
        status='PENDING'
    )
    
    # In a real system, these would trigger Celery tasks
    sent_via = []
    
    if prefs.email_enabled:
        # send_email_task.delay(user.email, subject, message)
        notification.sent_via_email = True
        sent_via.append('EMAIL')
        
    if prefs.sms_enabled and user.phone:
        # send_sms_task.delay(user.phone, message)
        notification.sent_via_sms = True
        sent_via.append('SMS')
        
    if prefs.push_enabled:
        # send_push_task.delay(user.id, subject, message)
        notification.sent_via_push = True
        sent_via.append('PUSH')
        
    if sent_via:
        notification.status = 'SENT'
        notification.sent_at = timezone.now()
    else:
        notification.status = 'FAILED'
        
    notification.save()
    return notification
