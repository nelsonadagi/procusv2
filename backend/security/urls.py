from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ThrottledRequestViewSet

router = DefaultRouter()
router.register(r'violations', ThrottledRequestViewSet, basename='violation')

urlpatterns = [
    path('', include(router.urls)),
]
