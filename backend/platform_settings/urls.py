from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PlatformConfigView, FeatureFlagViewSet, CurrencyRateViewSet,
    CountryViewSet, AdminUserViewSet, AdminRoleViewSet, PaymentGatewayConfigViewSet,
    PaymentMethodCatalogView, ExchangeRateConfigViewSet
)

router = DefaultRouter()
router.register(r'features', FeatureFlagViewSet, basename='features')
router.register(r'currencies', CurrencyRateViewSet, basename='currencies')
router.register(r'countries', CountryViewSet, basename='countries')
router.register(r'admin-users', AdminUserViewSet, basename='admin-users')
router.register(r'roles', AdminRoleViewSet, basename='roles')
router.register(r'payment-gateways', PaymentGatewayConfigViewSet, basename='payment-gateways')
router.register(r'exchange-rate-configs', ExchangeRateConfigViewSet, basename='exchange-rate-configs')

urlpatterns = [
    path('platform/', PlatformConfigView.as_view(), name='platform-config'),
    path('payment-methods/', PaymentMethodCatalogView.as_view(), name='payment-methods'),
    path('', include(router.urls)),
]
