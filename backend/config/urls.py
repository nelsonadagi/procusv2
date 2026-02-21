from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('catalog.urls')),
    path('api/v2/', include('config.urls_v2')),
    path('api/v3/', include('config.urls_v3')),
    path('api/v4/', include('config.urls_v4')),
    path('api/v5/', include('config.urls_v5')),
    path('api/v6/', include('config.urls_v6')),
    path('api/accounts/', include('accounts.urls')),
    path('api/rbac/', include('rbac.urls')),
    path('api/taxonomy/', include('taxonomy.urls')),
    path('api/config/', include('platform_settings.urls')),
    path('api/vendors/', include('vendors.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/reviews/', include('reviews.urls')),
    path('api/contractors/', include('contractors.urls')),
    path('api/contracts/', include('contracts.urls')),
    path('api/projects/', include('projects.urls')),
    path('api/bids/', include('bids.urls')),
    path('api/milestones/', include('milestones.urls')),
    # Add other apps here as we implement them
    # path('api/v1/', include('orders.urls')),
]
