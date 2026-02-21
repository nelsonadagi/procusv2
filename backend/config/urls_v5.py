from django.urls import path, include
from rest_framework.routers import DefaultRouter
from regulation.views import InvestorProfileViewSet, InvestmentAgreementViewSet
from enterprise.views import OrganizationViewSet, ApprovalWorkflowViewSet
from government.views import PublicTenderViewSet
from compliance.views import KYCVerificationViewSet
from risk.views import RiskViewSet

router = DefaultRouter()
router.register(r'investors', InvestorProfileViewSet, basename='investor')
router.register(r'agreements', InvestmentAgreementViewSet, basename='agreement')
router.register(r'organizations', OrganizationViewSet, basename='organization')
router.register(r'workflows', ApprovalWorkflowViewSet, basename='workflow')
router.register(r'tenders', PublicTenderViewSet, basename='tender')
router.register(r'kyc', KYCVerificationViewSet, basename='kyc')
router.register(r'risk-alerts', RiskViewSet, basename='risk-alert')

urlpatterns = [
    path('', include(router.urls)),
]
