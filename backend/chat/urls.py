from rest_framework.routers import DefaultRouter
from .views import ChatRoomViewSet, ChatMessageViewSet, ChatAttachmentViewSet

router = DefaultRouter()
router.register(r'rooms', ChatRoomViewSet)
router.register(r'messages', ChatMessageViewSet)
router.register(r'attachments', ChatAttachmentViewSet)

urlpatterns = router.urls
