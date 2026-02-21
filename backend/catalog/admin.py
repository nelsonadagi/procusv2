from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor', 'category', 'base_price', 'stock_quantity', 'status', 'is_public')
    list_filter = ('status', 'category', 'vendor')
    search_fields = ('name', 'description', 'vendor__business_name')
    actions = ['make_active', 'make_disabled']

    def make_active(self, request, queryset):
        queryset.update(status='ACTIVE')
    make_active.short_description = "Set status to ACTIVE"

    def make_disabled(self, request, queryset):
        queryset.update(status='DISABLED')
    make_disabled.short_description = "Set status to DISABLED"
