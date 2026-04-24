import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()
            return

        self.group_name = f"user_{self.user.id}"

        # Join room group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group (only if we successfully connected)
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    # Receive message from WebSocket (client to server)
    # Typically notifications are server-to-client only, so this might not be used much
    async def receive(self, text_data):
        pass

    # Receive message from group (server to client via channel layer)
    async def notification_message(self, event):
        message = event['message']
        notification_type = event.get('notification_type', 'SYSTEM')
        data = event.get('data', {})
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'type': notification_type,
            'timestamp': event.get('timestamp'),
            'data': data
        }))
