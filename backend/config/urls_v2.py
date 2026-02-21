from django.urls import path, include
from rest_framework.routers import DefaultRouter
from contractors.views import ContractorViewSet
from contracts.views import ContractViewSet
from bids.views import BidViewSet
from milestones.views import MilestoneViewSet

router = DefaultRouter()
router.register(r'contractors', ContractorViewSet, basename='contractor')
router.register(r'contracts', ContractViewSet, basename='contract')
router.register(r'bids', BidViewSet, basename='bid')
router.register(r'milestones', MilestoneViewSet, basename='milestone')

urlpatterns = [
    path('', include(router.urls)),
]
