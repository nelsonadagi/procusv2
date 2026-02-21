from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MilestoneViewSet

router = DefaultRouter()
router.register(r'', MilestoneViewSet, basename='milestone')

urlpatterns = [
    path('', include(router.urls)),
]
