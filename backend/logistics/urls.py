from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarrierViewSet, PricingZoneViewSet, PricingRuleViewSet, ShipmentViewSet, CarrierWebhookView, CourierProfileViewSet

router = DefaultRouter()
router.register(r'carriers', CarrierViewSet)
router.register(r'couriers', CourierProfileViewSet)
router.register(r'pricing-zones', PricingZoneViewSet)
router.register(r'pricing-rules', PricingRuleViewSet)
router.register(r'shipments', ShipmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('webhooks/', CarrierWebhookView.as_view({'post': 'status_update'}), name='webhook-status'),
]
