from django.db import models
from django.conf import settings
from cryptography.fernet import Fernet
import base64
import os

# Utility for encryption
def get_cipher():
    # In production, this key should be in environment variables
    key = getattr(settings, 'PLATFORM_ENCRYPTION_KEY', None)
    if not key:
        # Fallback or generate for dev (not for production!)
        key = base64.urlsafe_b64encode(settings.SECRET_KEY[:32].encode().ljust(32))
    return Fernet(key)

def encrypt_value(value):
    if not value: return None
    cipher = get_cipher()
    return cipher.encrypt(value.encode()).decode()

def decrypt_value(value):
    if not value: return None
    cipher = get_cipher()
    try:
        return cipher.decrypt(value.encode()).decode()
    except Exception:
        return "[Decryption Error]"

class PlatformSettings(models.Model):
    # Identity & Branding
    platform_name = models.CharField(max_length=255, default="Ujenzi Marketplace")
    tagline = models.CharField(max_length=255, blank=True, help_text="Short platform tagline")
    logo = models.ImageField(upload_to='platform/branding/', null=True, blank=True)
    favicon = models.ImageField(upload_to='platform/branding/', null=True, blank=True)
    primary_color = models.CharField(max_length=7, default="#FF6B2B", help_text="Brand primary hex color")
    secondary_color = models.CharField(max_length=7, default="#1A1A2E", help_text="Brand secondary hex color")

    # Contact & Legal
    support_email = models.EmailField(default="support@ujenzi.com")
    support_phone = models.CharField(max_length=32, default="+254 700 000000")
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)

    # Regional & Currency
    default_currency = models.CharField(max_length=10, default="KES")
    default_region = models.CharField(max_length=10, default="KE")
    active_languages = models.JSONField(default=list, help_text="e.g. ['en', 'sw']")

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Platform Settings"
        verbose_name_plural = "Platform Settings"

    def __str__(self):
        return self.platform_name

    def save(self, *args, **kwargs):
        if self.is_active:
            PlatformSettings.objects.exclude(id=self.id).update(is_active=False)
        super().save(*args, **kwargs)


class CurrencyRate(models.Model):
    """Exchange rates relative to the platform's default currency."""
    currency_code = models.CharField(max_length=10, unique=True, help_text="ISO 4217 code e.g. USD, EUR, TZS")
    currency_name = models.CharField(max_length=100, help_text="e.g. US Dollar")
    symbol = models.CharField(max_length=10, help_text="e.g. $, €, KSh")
    rate_to_default = models.DecimalField(max_digits=18, decimal_places=6,
        help_text="How many units of this currency equal 1 unit of the default currency")
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['currency_code']

    def __str__(self):
        return f"{self.currency_code} – {self.currency_name} ({self.rate_to_default})"

class OrganizationSettings(models.Model):
    organization = models.OneToOneField('accounts.Organization', on_delete=models.CASCADE, related_name='settings')
    logo_override = models.ImageField(upload_to='org/branding/', null=True, blank=True)
    primary_color = models.CharField(max_length=7, default="#0052cc")
    secondary_color = models.CharField(max_length=7, default="#f4f5f7")
    
    procurement_rules = models.JSONField(default=dict, blank=True)
    enabled_modules = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"Settings for {self.organization.name}"

class PaymentGatewayConfig(models.Model):
    class Provider(models.TextChoices):
        STRIPE = "STRIPE", "Stripe"
        FLUTTERWAVE = "FLUTTERWAVE", "Flutterwave"
        MPESA = "MPESA", "M-Pesa"
        PAYPAL = "PAYPAL", "PayPal"

    provider = models.CharField(max_length=32, choices=Provider.choices)
    label = models.CharField(max_length=100)
    public_key = models.CharField(max_length=255)
    _secret_key = models.TextField(db_column='secret_key') # Encrypted
    webhook_secret = models.CharField(max_length=255, blank=True, null=True)
    
    enabled_regions = models.JSONField(default=list, help_text="List of region codes e.g. ['KE', 'UG']")
    active = models.BooleanField(default=True)
    is_test_mode = models.BooleanField(default=True)

    @property
    def secret_key(self):
        return decrypt_value(self._secret_key)

    @secret_key.setter
    def secret_key(self, value):
        self._secret_key = encrypt_value(value)

    def __str__(self):
        return f"{self.label} ({self.provider})"

class MessagingGatewayConfig(models.Model):
    class Provider(models.TextChoices):
        TWILIO = "TWILIO", "Twilio"
        AFRICASTALKING = "AFRICASTALKING", "AfricaTalking"
        META_WHATSAPP = "META_WHATSAPP", "Meta WhatsApp Cloud"

    provider = models.CharField(max_length=32, choices=Provider.choices)
    label = models.CharField(max_length=100)
    api_key_or_token = models.TextField() # Should be encrypted too
    sender_id_or_number = models.CharField(max_length=100)
    
    enabled_channels = models.JSONField(default=list, help_text="['SMS', 'WHATSAPP']")
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.label} ({self.provider})"

class FeatureFlag(models.Model):
    key = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    
    enabled_regions = models.JSONField(default=list, blank=True)
    enabled_for_orgs = models.ManyToManyField('accounts.Organization', blank=True)

    def __str__(self):
        return self.key


class Country(models.Model):
    """Active countries the platform operates in."""
    iso_code = models.CharField(max_length=3, unique=True, help_text="ISO 3166-1 alpha-2/3 code e.g. KE, UG, TZ")
    name = models.CharField(max_length=100)
    flag_emoji = models.CharField(max_length=10, blank=True, help_text="e.g. 🇰🇪")
    phone_prefix = models.CharField(max_length=10, blank=True, help_text="e.g. +254")
    default_currency = models.CharField(max_length=10, blank=True, help_text="ISO 4217 code")
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False, help_text="The platform's primary country")

    class Meta:
        ordering = ['-is_default', 'name']
        verbose_name_plural = 'Countries'

    def __str__(self):
        return f"{self.flag_emoji} {self.name} ({self.iso_code})"

    def save(self, *args, **kwargs):
        if self.is_default:
            # Only one default at a time
            Country.objects.exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)

