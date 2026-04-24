from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PropertyViewSet,
    PropertyInquiryViewSet,
    PropertyAvailabilityWindowViewSet,
    PropertyAppointmentViewSet,
)

router = DefaultRouter()
router.register(r'inquiries', PropertyInquiryViewSet, basename='property-inquiry')
router.register(r'availability-windows', PropertyAvailabilityWindowViewSet, basename='property-availability-window')
router.register(r'appointments', PropertyAppointmentViewSet, basename='property-appointment')
router.register(r'', PropertyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
