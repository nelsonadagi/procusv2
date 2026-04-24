from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VendorViewSet

router = DefaultRouter()
router.register(r'', VendorViewSet, basename='vendors')

urlpatterns = [
    path('me/', VendorViewSet.as_view({'get': 'me'}), name='vendor-me'),
] + router.urls
