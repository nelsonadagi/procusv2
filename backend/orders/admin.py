from django.contrib import admin
from .models import Order, OrderItem, QuoteRequest, QuoteResponse

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name_snapshot', 'unit_price_snapshot', 'quantity')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'vendor', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'buyer__username', 'vendor__business_name')
    inlines = [OrderItemInline]
    readonly_fields = ('total_amount', 'created_at', 'updated_at')

admin.site.register(QuoteRequest)
admin.site.register(QuoteResponse)
