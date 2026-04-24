from rest_framework import serializers
from .models import KYCVerification, JurisdictionRule

class KYCVerificationSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = KYCVerification
        fields = '__all__'
        read_only_fields = ['user', 'status', 'submitted_at', 'verified_at']

    def get_user_name(self, obj):
        return obj.user.get_full_name()

class JurisdictionRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = JurisdictionRule
        fields = '__all__'
