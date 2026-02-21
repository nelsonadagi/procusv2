from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, UserManagementViewSet, ProfileView, AddressViewSet

router = DefaultRouter()
router.register(r'management', UserManagementViewSet, basename='user-management')
router.register(r'addresses', AddressViewSet, basename='addresses')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('', include(router.urls)),
]
