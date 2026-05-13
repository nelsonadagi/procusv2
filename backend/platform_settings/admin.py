from django.contrib import admin, messages
from django import forms
from .models import (
    PlatformSettings, OrganizationSettings, PaymentGatewayConfig, 
    MessagingGatewayConfig, FeatureFlag, CurrencyRate, Country, ExchangeRateConfig
)
from .services import update_currency_rates

class PlatformSettingsAdmin(admin.ModelAdmin):
    list_display = ('platform_name', 'default_currency', 'default_region', 'is_active')
    fieldsets = (
        ('Branding & Identity', {
            'fields': ('platform_name', 'logo', 'favicon')
        }),
        ('Contact Info', {
            'fields': ('support_email', 'support_phone')
        }),
        ('Localization & Defaults', {
            'fields': ('default_currency', 'default_region', 'active_languages')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

class PaymentGatewayConfigForm(forms.ModelForm):
    secret_key = forms.CharField(widget=forms.PasswordInput(), required=False, help_text="Leave blank to keep existing key")

    class Meta:
        model = PaymentGatewayConfig
        fields = '__all__'
        exclude = ('_secret_key',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['secret_key'].initial = self.instance.secret_key

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data.get('secret_key'):
            instance.secret_key = self.cleaned_data['secret_key']
        if commit:
            instance.save()
        return instance

class PaymentGatewayConfigAdmin(admin.ModelAdmin):
    form = PaymentGatewayConfigForm
    list_display = ('label', 'provider', 'active', 'is_default', 'is_test_mode', 'display_order')
    list_filter = ('provider', 'active', 'is_default', 'is_test_mode')
    search_fields = ('label', 'provider', 'instructions')

class ExchangeRateConfigForm(forms.ModelForm):
    api_key = forms.CharField(widget=forms.PasswordInput(), required=False, help_text="Encrypted API key if required")

    class Meta:
        model = ExchangeRateConfig
        fields = '__all__'
        exclude = ('_api_key',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['api_key'].initial = self.instance.api_key

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data.get('api_key'):
            instance.api_key = self.cleaned_data['api_key']
        if commit:
            instance.save()
        return instance

class ExchangeRateConfigAdmin(admin.ModelAdmin):
    form = ExchangeRateConfigForm
    list_display = ('label', 'provider', 'active', 'is_default', 'last_sync')
    list_filter = ('provider', 'active', 'is_default')
    actions = ['sync_rates_action']

    def sync_rates_action(self, request, queryset):
        if queryset.count() > 1:
            self.message_user(request, "Please select only one config to sync.", messages.WARNING)
            return
        
        config = queryset.first()
        if not config.active:
            self.message_user(request, "Cannot sync an inactive configuration.", messages.WARNING)
            return

        success = update_currency_rates()
        if success:
            self.message_user(request, "Currency rates synchronized successfully.", messages.SUCCESS)
        else:
            self.message_user(request, "Synchronization failed. Check logs for details.", messages.ERROR)

    sync_rates_action.short_description = "Sync currency rates now"

class MessagingGatewayConfigAdmin(admin.ModelAdmin):
    list_display = ('label', 'provider', 'active')
    list_filter = ('provider', 'active')

class FeatureFlagAdmin(admin.ModelAdmin):
    list_display = ('key', 'active')
    filter_horizontal = ('enabled_for_orgs',)

class CurrencyRateAdmin(admin.ModelAdmin):
    list_display = ('currency_code', 'currency_name', 'symbol', 'rate_to_default', 'is_active', 'updated_at')
    list_editable = ('rate_to_default', 'is_active')
    search_fields = ('currency_code', 'currency_name')

class CountryAdmin(admin.ModelAdmin):
    list_display = ('flag_emoji', 'name', 'iso_code', 'default_currency', 'is_default', 'is_active')
    list_filter = ('is_active', 'is_default')
    search_fields = ('name', 'iso_code')

admin.site.register(PlatformSettings, PlatformSettingsAdmin)
admin.site.register(OrganizationSettings)
admin.site.register(PaymentGatewayConfig, PaymentGatewayConfigAdmin)
admin.site.register(MessagingGatewayConfig, MessagingGatewayConfigAdmin)
admin.site.register(FeatureFlag, FeatureFlagAdmin)
admin.site.register(CurrencyRate, CurrencyRateAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(ExchangeRateConfig, ExchangeRateConfigAdmin)
