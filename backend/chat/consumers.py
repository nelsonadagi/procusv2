import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatRoom, ChatMessage, ChatAttachment
from notifications.models import Notification

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        print(f"WS Connecting: Room={self.room_name}, User={self.scope['user']}")

        # Check if the user is authenticated
        if not self.scope["user"].is_authenticated:
            await self.close()
            return

        # Fetch the chat room
        self.room = await self.get_chat_room(self.room_name)
        if not self.room:
            await self.close()
            return
        
        # Check if the user is a participant in the room
        is_participant = await self.is_user_participant(self.room, self.scope["user"])
        if not is_participant:
            await self.close()
            return

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message_content = text_data_json.get("message", "") # Default to empty string
            attachment_id = text_data_json.get("attachment_id")
            
            if not self.scope["user"].is_authenticated:
                return

            if message_content or attachment_id: # Only proceed if there's content or an attachment
                # Save message to database
                message_obj, attachment_data, recipient_ids = await self.save_message(
                    self.room, 
                    self.scope["user"], 
                    message_content, 
                    attachment_id
                )

                # Send message to room group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "chat_message",
                        "message_id": message_obj.id,
                        "content": message_obj.content,
                        "sender_username": message_obj.sender.username,
                        "timestamp": message_obj.timestamp.isoformat(),
                        "attachment": attachment_data,
                    },
                )
                
                # Send notifications to recipients
                for recipient_id in recipient_ids:
                    await self.channel_layer.group_send(
                        f"user_{recipient_id}",
                        {
                            "type": "notification_message",
                            "message": f"New message from {self.scope['user'].username}",
                            "notification_type": "CHAT",
                            "timestamp": message_obj.timestamp.isoformat(),
                            "data": { "room_id": self.room.id }
                        }
                    )
        except Exception as e:
            print(f"Error in receive: {e}")
            # Optionally send error back to client
            # await self.send(text_data=json.dumps({"error": str(e)}))

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message_id": event["message_id"],
            "content": event["content"],
            "sender_username": event["sender_username"],
            "timestamp": event["timestamp"],
            "attachment": event.get("attachment"), # Include attachment data
        }))

    @database_sync_to_async
    def get_chat_room(self, room_name):
        try:
            return ChatRoom.objects.get(id=room_name)
        except ChatRoom.DoesNotExist:
            return None

    @database_sync_to_async
    def is_user_participant(self, room, user):
        return room.participants.filter(id=user.id).exists()

    @database_sync_to_async
    def save_message(self, room, sender, content, attachment_id=None):
        message = ChatMessage.objects.create(room=room, sender=sender, content=content)
        attachment_data = None
        
        if attachment_id:
            try:
                attachment = ChatAttachment.objects.get(id=attachment_id)
                # Link orphaned attachment to message
                attachment.message = message
                attachment.save()
                
                attachment_data = {
                    "id": attachment.id,
                    "file_url": attachment.file.url,
                    "file_type": attachment.file_type,
                }
            except ChatAttachment.DoesNotExist:
                print(f"Attachment {attachment_id} not found")
                pass 
                
        # Get recipients (all participants except sender)
        recipients = list(room.participants.exclude(id=sender.id))
        
        # Create notifications
        for recipient in recipients:
            Notification.objects.create(
                user=recipient,
                type=Notification.Type.CHAT,
                subject=f"New message from {sender.username}",
                message=content[:50] + "..." if len(content) > 50 else content,
                status=Notification.Status.SENT
            )
            
        return message, attachment_data, [r.id for r in recipients]
