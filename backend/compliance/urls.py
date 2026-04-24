from rest_framework.routers import DefaultRouter
from compliance.views import KYCVerificationViewSet, JurisdictionRuleViewSet

router = DefaultRouter()
router.register(r'kyc-verifications', KYCVerificationViewSet)
router.register(r'jurisdiction-rules', JurisdictionRuleViewSet)

urlpatterns = router.urls
