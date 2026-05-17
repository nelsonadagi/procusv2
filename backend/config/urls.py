from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

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
    path('api/platform_settings/', include('platform_settings.urls')),
    path('api/vendors/', include('vendors.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/reviews/', include('reviews.urls')),
    path('api/contractors/', include('contractors.urls')),
    path('api/contracts/', include('contracts.urls')),
    path('api/projects/', include('projects.urls')),
    path('api/bids/', include('bids.urls')),
    path('api/milestones/', include('milestones.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/property/', include('property.urls')),
    path('api/security/', include('security.urls')),
    path('api/logistics/', include('logistics.urls')),
    path('api/compliance/', include('compliance.urls')),
    path('api/chat/', include('chat.urls')), # Newly added chat app URLs
    # Add other apps here as we implement them
    # path('api/v1/', include('orders.urls')),
]

# Serve media files in both dev and production.
# NOTE: For high traffic, switch to nginx direct-serving or object storage.
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]
