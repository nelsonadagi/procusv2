from rest_framework import serializers
from platform_settings.serializers import LocationSyncMixin
from .models import Vendor

class VendorSerializer(LocationSyncMixin, serializers.ModelSerializer):
    id = serializers.UUIDField(source='uuid', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    location = serializers.CharField(source='location_text', required=False, allow_blank=True)
    location_id = serializers.PrimaryKeyRelatedField(source='location', read_only=True)

    class Meta:
        model = Vendor
        fields = [
            'id', 'username', 'email', 'business_name',
            'registration_number', 'verified_status', 'country', 'location', 'location_id',
            'latitude', 'longitude', 'formatted_address', 'location_hierarchy',
            'provides_delivery', 'delivery_radius_km',
            'categories_served', 'fulfillment_rate', 'cancellation_rate',
            'delivery_timeliness', 'average_rating', 'total_reviews', 'created_at'
        ]
        read_only_fields = [
            'fulfillment_rate', 'cancellation_rate',
            'delivery_timeliness', 'average_rating', 'total_reviews', 'created_at'
        ]

    def update(self, instance, validated_data):
        vendor = super().update(instance, validated_data)
        self._sync_location_obj(vendor, validated_data)
        return vendor

class VendorOnboardingSerializer(LocationSyncMixin, serializers.ModelSerializer):
    id = serializers.UUIDField(source='uuid', read_only=True)
    location = serializers.CharField(source='location_text', required=False, allow_blank=True)
    location_id = serializers.PrimaryKeyRelatedField(source='location', read_only=True)

    class Meta:
        model = Vendor
        fields = [
            'id',
            'business_name', 'registration_number', 'country', 'location',
            'location_id',
            'latitude', 'longitude', 'formatted_address', 'location_hierarchy',
            'provides_delivery', 'delivery_radius_km',
            'categories_served'
        ]
        read_only_fields = ['id', 'location_id']

    def create(self, validated_data):
        user = self.context['request'].user
        if Vendor.objects.filter(user=user).exists():
            raise serializers.ValidationError("User already has a vendor profile.")

        vendor = Vendor.objects.create(user=user, **validated_data)
        self._sync_location_obj(vendor, validated_data)
        return vendor

    def update(self, instance, validated_data):
        vendor = super().update(instance, validated_data)
        self._sync_location_obj(vendor, validated_data)
        return vendor
