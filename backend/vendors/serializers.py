from rest_framework import serializers
from .models import Vendor

class VendorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Vendor
        fields = [
            'id', 'username', 'email', 'business_name', 
            'registration_number', 'verified_status', 'location', 
            'categories_served', 'fulfillment_rate', 'cancellation_rate', 
            'delivery_timeliness', 'average_rating', 'total_reviews', 'created_at'
        ]
        read_only_fields = [
            'fulfillment_rate', 'cancellation_rate', 
            'delivery_timeliness', 'average_rating', 'total_reviews', 'created_at'
        ]

class VendorOnboardingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = [
            'business_name', 'registration_number', 'location', 'categories_served'
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        if Vendor.objects.filter(user=user).exists():
            raise serializers.ValidationError("User already has a vendor profile.")
        return Vendor.objects.create(user=user, **validated_data)
