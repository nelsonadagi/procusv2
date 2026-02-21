from django.contrib import admin
from django import forms
from .models import PlatformSettings, OrganizationSettings, PaymentGatewayConfig, MessagingGatewayConfig, FeatureFlag

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
    list_display = ('label', 'provider', 'active', 'is_test_mode')
    list_filter = ('provider', 'active', 'is_test_mode')

class MessagingGatewayConfigAdmin(admin.ModelAdmin):
    list_display = ('label', 'provider', 'active')
    list_filter = ('provider', 'active')

class FeatureFlagAdmin(admin.ModelAdmin):
    list_display = ('key', 'active')
    filter_horizontal = ('enabled_for_orgs',)

admin.site.register(PlatformSettings, PlatformSettingsAdmin)
admin.site.register(OrganizationSettings)
admin.site.register(PaymentGatewayConfig, PaymentGatewayConfigAdmin)
admin.site.register(MessagingGatewayConfig, MessagingGatewayConfigAdmin)
admin.site.register(FeatureFlag, FeatureFlagAdmin)
