from django.urls import path, include
from rest_framework.routers import DefaultRouter
from escrow.views import EscrowViewSet, EscrowReleaseViewSet
from disputes.views import DisputeViewSet
from finance.views import FinanceProductViewSet, FinanceApplicationViewSet
from scoring.views import ScoringViewSet

router = DefaultRouter()
router.register(r'escrow', EscrowViewSet, basename='escrow')
router.register(r'escrow-releases', EscrowReleaseViewSet, basename='escrow-release')
router.register(r'disputes', DisputeViewSet, basename='dispute')
router.register(r'finance/products', FinanceProductViewSet, basename='finance-product')
router.register(r'finance/applications', FinanceApplicationViewSet, basename='finance-application')
router.register(r'scoring', ScoringViewSet, basename='scoring')

urlpatterns = [
    path('', include(router.urls)),
]
