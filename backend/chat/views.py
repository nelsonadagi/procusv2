from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import ChatRoom, ChatMessage, ChatAttachment
from .serializers import ChatRoomSerializer, ChatMessageSerializer, ChatAttachmentSerializer
from orders.models import Order
from contracts.models import Contract
from notifications.models import Notification
from notifications.services import notify_users

class IsRoomParticipant(permissions.BasePermission):
    """
    Custom permission to only allow participants of a chat room to access it.
    """
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated:
            room = obj
            if isinstance(obj, ChatMessage):
                room = obj.room
            elif isinstance(obj, ChatAttachment):
                room = obj.message.room if obj.message else None
            if not room:
                return False
            return room.participants.filter(id=request.user.id).exists()
        return False

class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all().order_by('-created_at')
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated, IsRoomParticipant]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # Only return chat rooms where the user is a participant
            return ChatRoom.objects.filter(participants=user).order_by('-created_at')
        return ChatRoom.objects.none()

    def perform_create(self, serializer):
        # When creating a chat room via POST /api/chat/rooms/
        instance = serializer.save()
        instance.participants.add(self.request.user)
        
        order_id = self.request.data.get('order')
        contract_id = self.request.data.get('contract')

        if order_id:
            order = get_object_or_404(Order, pk=order_id)
            instance.order = order
            instance.participants.add(order.vendor.user)
            if order.buyer != self.request.user:
                instance.participants.add(order.buyer)
            instance.save()
        elif contract_id:
            contract = get_object_or_404(Contract, pk=contract_id)
            instance.contract = contract
            instance.participants.add(contract.owner)
            # If it's an awarded contract, add the contractor
            awarded_bid = contract.bids.filter(status='AWARDED').first()
            if awarded_bid:
                instance.participants.add(awarded_bid.contractor.user)
            instance.save()

    @action(detail=False, methods=['post'], url_path='get-or-create')
    def get_or_create(self, request):
        order_id = request.data.get('order')
        contract_id = request.data.get('contract')
        
        if not order_id and not contract_id:
            return Response({"error": "Order or Contract ID required"}, status=status.HTTP_400_BAD_REQUEST)
            
        room = None
        if order_id:
            order = get_object_or_404(Order, pk=order_id)
            if request.user != order.buyer and request.user != order.vendor.user:
                return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
            
            # Explicitly check for contract=None to avoid matching rooms with contracts
            room, created = ChatRoom.objects.get_or_create(order=order, contract=None)
            if created:
                room.participants.add(order.buyer, order.vendor.user)
                
        elif contract_id:
            contract = get_object_or_404(Contract, pk=contract_id)
            awarded_bid = contract.bids.filter(status='AWARDED').first()
            
            if not awarded_bid and request.user == contract.owner:
                 return Response({"error": "No awarded contractor to chat with yet"}, status=status.HTTP_400_BAD_REQUEST)
            
            # If a contractor who hasn't been awarded wants to chat, we might allow it if they have a bid?
            # For simplicity, let's keep it to awarded for now as per system design
            if awarded_bid:
                if request.user != contract.owner and request.user != awarded_bid.contractor.user:
                    return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
            else:
                # Contractor not awarded yet, maybe they can't chat yet or we need a bid_id
                return Response({"error": "Chat only available for awarded contracts"}, status=status.HTTP_400_BAD_REQUEST)
                
            room, created = ChatRoom.objects.get_or_create(contract=contract)
            if created:
                room.participants.add(contract.owner, awarded_bid.contractor.user)
                
        serializer = self.get_serializer(room)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        chat_room = self.get_object()
        messages = chat_room.messages.all()
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)

class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all().order_by('timestamp')
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsRoomParticipant]

    def perform_create(self, serializer):
        room = serializer.validated_data['room']
        # Ensure the creating user is a participant of the room
        if not self.request.user in room.participants.all():
            raise permissions.PermissionDenied("You are not a participant of this chat room.")
        message = serializer.save(sender=self.request.user)
        recipients = room.participants.exclude(id=self.request.user.id)
        notify_users(
            recipients,
            Notification.Type.CHAT,
            f"New message from {self.request.user.username}",
            message.content[:120] or "New chat message",
            data={"room_id": room.id, "message_id": message.id},
        )

    def get_queryset(self):
        # Custom queryset to ensure users only see messages from rooms they are part of
        user = self.request.user
        if user.is_authenticated:
            return ChatMessage.objects.filter(room__participants=user).order_by('timestamp')
        return ChatMessage.objects.none()

class ChatAttachmentViewSet(viewsets.ModelViewSet):
    queryset = ChatAttachment.objects.all()
    serializer_class = ChatAttachmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsRoomParticipant] # Need to check message's room for participant status

    def perform_create(self, serializer):
        # Handle message if provided (though it might be read-only in serializer)
        message = serializer.validated_data.get('message')
        if message:
            room = message.room
            if not self.request.user in room.participants.all():
                raise permissions.PermissionDenied("You are not a participant of the chat room associated with this message.")
        
        # If no message provided (orphaned upload), just save.
        # Ideally we should check permission via a room_id passed in context,
        # but for now we rely on IsAuthenticated.
        serializer.save()

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return ChatAttachment.objects.filter(message__room__participants=user)
        return ChatAttachment.objects.none()
