from django.contrib import admin
from .models import Vendor

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'verified_status', 'location', 'created_at', 'fulfillment_rate')
    list_filter = ('verified_status', 'location')
    search_fields = ('business_name', 'registration_number', 'user__username', 'user__email')
    actions = ['approve_vendors', 'reject_vendors', 'suspend_vendors']

    def approve_vendors(self, request, queryset):
        queryset.update(verified_status='APPROVED')
    approve_vendors.short_description = "Approve selected vendors"

    def reject_vendors(self, request, queryset):
        queryset.update(verified_status='REJECTED')
    reject_vendors.short_description = "Reject selected vendors"
    
    def suspend_vendors(self, request, queryset):
        queryset.update(verified_status='SUSPENDED')
    suspend_vendors.short_description = "Suspend selected vendors"
