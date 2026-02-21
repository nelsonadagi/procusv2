from django.urls import path, include
from rest_framework.routers import DefaultRouter
from banking.views import BankAccountViewSet, SettlementTransactionViewSet
from reporting.views import RegulatoryReportViewSet
from ai_engine.views import PredictionViewSet
from liquidity.views import SecondaryTradeViewSet
from integrations.views import ERPConnectorViewSet

router = DefaultRouter()
router.register(r'bank-accounts', BankAccountViewSet, basename='bank-account')
router.register(r'settlements', SettlementTransactionViewSet, basename='settlement')
router.register(r'regulatory-reports', RegulatoryReportViewSet, basename='report')
router.register(r'ai-predictions', PredictionViewSet, basename='prediction')
router.register(r'secondary-trades', SecondaryTradeViewSet, basename='trade')
router.register(r'erp-connectors', ERPConnectorViewSet, basename='erp')

urlpatterns = [
    path('', include(router.urls)),
]
