from rest_framework import serializers
from .models import Notification, NotificationPreference

class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = ['email_enabled', 'sms_enabled', 'push_enabled']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'type', 'subject', 'message', 'status', 'created_at', 'sent_at']
        read_only_fields = ['id', 'status', 'created_at', 'sent_at']
