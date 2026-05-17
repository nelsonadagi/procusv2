from django.utils import timezone
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Notification, NotificationPreference


def _push_notification(notification, data=None):
    channel_layer = get_channel_layer()
    if not channel_layer:
        return

    async_to_sync(channel_layer.group_send)(
        f"user_{notification.user_id}",
        {
            "type": "notification_message",
            "message": notification.message,
            "notification_type": notification.type,
            "timestamp": notification.created_at.isoformat(),
            "data": {
                "notification_id": notification.id,
                "subject": notification.subject,
                **(data or {}),
            },
        },
    )


def notify_user(user, notification_type, subject, message, data=None):
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
    _push_notification(notification, data=data)
    return notification


def notify_users(users, notification_type, subject, message, data=None):
    notifications = []
    seen = set()
    for user in users:
        if not user or not getattr(user, "is_authenticated", False) or user.id in seen:
            continue
        seen.add(user.id)
        notifications.append(
            notify_user(
                user=user,
                notification_type=notification_type,
                subject=subject,
                message=message,
                data=data,
            )
        )
    return notifications
