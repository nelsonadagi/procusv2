from rest_framework import serializers
from .models import PlatformSettings, FeatureFlag, CurrencyRate, Country, Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'address', 'city', 'state', 'country', 'latitude', 'longitude', 'metadata']


class LocationSyncMixin:
    """Mixin to synchronize Location model from validated data coords"""
    def _sync_location_obj(self, instance, validated_data):
        from django.contrib.gis.geos import Point
        
        lat = validated_data.get('latitude')
        lng = validated_data.get('longitude')
        
        # Precision Guard: Truncate to 6 decimal places (approx 10cm accuracy)
        # This ensures we stay comfortably within the max_digits=12 limit.
        if lat is not None: lat = round(float(lat), 6)
        if lng is not None: lng = round(float(lng), 6)
        
        # Use formatted_address if available, otherwise fallback
        address = validated_data.get('formatted_address') or validated_data.get('location_text', '')
        
        # City resolution: priority to explicit fields, then fallback to location_text if the address is already set
        city = (
            validated_data.get('location_city') or 
            validated_data.get('city') or 
            validated_data.get('location_text')
        )
        country = validated_data.get('country')
        
        if lat and lng:
            try:
                point = Point(float(lng), float(lat))
                # If instance already has a location, update it
                loc = getattr(instance, 'location', None)
                
                if loc:
                    loc.point = point
                    loc.address = address
                    if city: loc.city = city
                    if country: loc.country = country
                    loc.latitude = lat
                    loc.longitude = lng
                    loc.save()
                else:
                    # Create new location
                    loc = Location.objects.create(
                        point=point,
                        address=address,
                        city=city or '',
                        country=country,
                        latitude=lat,
                        longitude=lng
                    )
                    instance.location = loc
                    instance.save()
            except (ValueError, TypeError, Exception) as e:
                print(f"Location sync error: {e}")


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
