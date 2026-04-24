from django.db import models
from django.conf import settings

class ChatRoom(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, help_text="Optional name for the chat room")
    order = models.ForeignKey('orders.Order', on_delete=models.SET_NULL, null=True, blank=True, related_name='chat_rooms')
    contract = models.ForeignKey('contracts.Contract', on_delete=models.SET_NULL, null=True, blank=True, related_name='chat_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chat_rooms')

    class Meta:
        unique_together = ('order', 'contract',) # Ensures one chat per order/contract
        verbose_name = "Chat Room"
        verbose_name_plural = "Chat Rooms"

    def __str__(self):
        if self.name:
            return self.name
        elif self.order:
            return f"Chat for Order: {self.order.id}"
        elif self.contract:
            return f"Chat for Contract: {self.contract.id}"
        return f"Chat Room {self.id}"

class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        verbose_name = "Chat Message"
        verbose_name_plural = "Chat Messages"

    def __str__(self):
        return f"Message from {self.sender.username} in {self.room}"

class ChatAttachment(models.Model):
    message = models.ForeignKey(ChatMessage, on_delete=models.CASCADE, related_name='attachments', null=True, blank=True)
    file = models.FileField(upload_to='chat_attachments/')
    file_type = models.CharField(max_length=50, blank=True, help_text="e.g., image, document, video")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Chat Attachment"
        verbose_name_plural = "Chat Attachments"

    def __str__(self):
        return f"Attachment for message {self.message.id}"