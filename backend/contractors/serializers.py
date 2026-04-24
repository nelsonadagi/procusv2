from rest_framework import serializers
from .models import ContractorProfile
from platform_settings.serializers import LocationSyncMixin

class ContractorProfileSerializer(LocationSyncMixin, serializers.ModelSerializer):
    class Meta:
        model = ContractorProfile
        fields = '__all__'
        read_only_fields = ['user', 'verified_status', 'rating_avg', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user:
            validated_data['user'] = request.user
        contractor = super().create(validated_data)
        self._sync_location_obj(contractor, validated_data)
        return contractor

    def update(self, instance, validated_data):
        contractor = super().update(instance, validated_data)
        self._sync_location_obj(contractor, validated_data)
        return contractor
