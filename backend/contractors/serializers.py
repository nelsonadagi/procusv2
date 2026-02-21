from rest_framework import serializers
from .models import ContractorProfile

class ContractorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractorProfile
        fields = '__all__'
        read_only_fields = ['user', 'verified_status', 'rating_avg', 'created_at']
