from rest_framework import serializers
from .models import ComplianceAlert

class ComplianceAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplianceAlert
        fields = '__all__'
