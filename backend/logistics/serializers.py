from rest_framework import serializers
from .models import Carrier, PricingZone, Shipment, TrackingEvent, CourierProfile, CourierApiConfig, CourierDocument, PricingRule

class CourierDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourierDocument
        fields = '__all__'

class CourierApiConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourierApiConfig
        exclude = ('api_key', 'api_secret', 'webhook_secret') # Exclude sensitive fields by default

from platform_settings.serializers import LocationSyncMixin

class CourierProfileSerializer(LocationSyncMixin, serializers.ModelSerializer):
    documents = CourierDocumentSerializer(many=True, read_only=True)
    location = serializers.CharField(source='location_text', required=False, allow_blank=True)
    location_id = serializers.PrimaryKeyRelatedField(source='location', read_only=True)
    
    class Meta:
        model = CourierProfile
        fields = [
            'id', 'company_name', 'registration_number', 'tax_pin', 'website',
            'support_email', 'support_phone', 'status', 'is_active',
            'location', 'location_id', 'country', 'latitude', 'longitude', 'formatted_address',
            'documents', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'status', 'is_active', 'created_at', 'updated_at']

    def create(self, validated_data):
        user = self.context['request'].user
        if CourierProfile.objects.filter(user=user).exists():
            raise serializers.ValidationError("User already has a courier profile.")
        
        profile = CourierProfile.objects.create(user=user, **validated_data)
        self._sync_location_obj(profile, validated_data)
        return profile

    def update(self, instance, validated_data):
        profile = super().update(instance, validated_data)
        self._sync_location_obj(profile, validated_data)
        return profile

class CarrierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrier
        fields = '__all__'

class PricingRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingRule
        fields = '__all__'

class PricingZoneSerializer(serializers.ModelSerializer):
    rules = PricingRuleSerializer(many=True, read_only=True)
    
    class Meta:
        model = PricingZone
        fields = '__all__'

class TrackingEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackingEvent
        fields = '__all__'

class ShipmentSerializer(serializers.ModelSerializer):
    events = TrackingEventSerializer(many=True, read_only=True)
    carrier_name = serializers.CharField(source='carrier.name', read_only=True)
    courier_name = serializers.CharField(source='courier.company_name', read_only=True)
    
    class Meta:
        model = Shipment
        fields = '__all__'
