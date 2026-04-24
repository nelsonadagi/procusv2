from rest_framework import serializers
from .models import ChatRoom, ChatMessage, ChatAttachment
from accounts.serializers import UserSerializer # Assuming UserSerializer exists for sender details

class ChatAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatAttachment
        fields = '__all__'
        read_only_fields = ('message', 'uploaded_at')

class ChatMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True) # Nested serializer for sender details
    attachments = ChatAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = ChatMessage
        fields = '__all__'
        read_only_fields = ('room', 'sender', 'timestamp')

class ChatRoomSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True) # Nested serializer for messages
    participants = UserSerializer(many=True, read_only=True) # Nested serializer for participants

    class Meta:
        model = ChatRoom
        fields = '__all__'
        read_only_fields = ('created_at',)
