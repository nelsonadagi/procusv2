from django.urls import path, include
from rest_framework.routers import DefaultRouter
from projects.views import ProjectViewSet
from property.views import PropertyViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'property', PropertyViewSet, basename='property')

urlpatterns = [
    path('', include(router.urls)),
]
