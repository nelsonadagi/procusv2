from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, QuoteRequestViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'quote-requests', QuoteRequestViewSet, basename='quote-requests')

urlpatterns = [
    path('', include(router.urls)),
]
