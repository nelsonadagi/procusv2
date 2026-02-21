from rest_framework import serializers
from .models import InvestorProfile, InvestmentAgreement

class InvestorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestorProfile
        fields = '__all__'
        read_only_fields = ['user', 'kyc_status', 'accreditation_status', 'created_at']

class InvestmentAgreementSerializer(serializers.ModelSerializer):
    investor = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = InvestmentAgreement
        fields = '__all__'
        read_only_fields = ['investor', 'status', 'signed_at', 'created_at']
