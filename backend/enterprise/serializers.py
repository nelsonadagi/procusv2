from rest_framework import serializers
from .models import Organization, ApprovalWorkflow

class ApprovalWorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalWorkflow
        fields = '__all__'

class OrganizationSerializer(serializers.ModelSerializer):
    workflows = ApprovalWorkflowSerializer(many=True, read_only=True)
    
    class Meta:
        model = Organization
        fields = '__all__'
        read_only_fields = ['created_at']
