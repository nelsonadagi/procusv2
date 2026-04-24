from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views # Import views to access test_vendor_orders_view
from .views import OrderViewSet, QuoteRequestViewSet

quote_router = DefaultRouter()
quote_router.register(r'', QuoteRequestViewSet, basename='quote-requests')

order_router = DefaultRouter()
order_router.register(r'', OrderViewSet, basename='orders')

urlpatterns = [
    path('quote-requests/', include(quote_router.urls)),
    path('', include(order_router.urls)),
]
