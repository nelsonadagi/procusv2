from rest_framework import serializers
from .models import PlatformSettings, FeatureFlag, CurrencyRate, Country


class PlatformSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformSettings
        fields = [
            'id', 'platform_name', 'tagline', 'logo', 'favicon',
            'primary_color', 'secondary_color',
            'support_email', 'support_phone', 'address', 'website',
            'default_currency', 'default_region', 'active_languages',
            'is_active', 'updated_at',
        ]
        read_only_fields = ['id', 'is_active', 'updated_at']


class CurrencyRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyRate
        fields = ['id', 'currency_code', 'currency_name', 'symbol', 'rate_to_default', 'is_active', 'updated_at']
        read_only_fields = ['id', 'updated_at']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'iso_code', 'name', 'flag_emoji', 'phone_prefix', 'default_currency', 'is_active', 'is_default']
        read_only_fields = ['id']


class FeatureFlagSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureFlag
        fields = ['key', 'active', 'description', 'enabled_regions']
