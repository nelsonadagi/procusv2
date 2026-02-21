from rest_framework import serializers
from .models import Dispute, EvidenceSubmission

class EvidenceSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvidenceSubmission
        fields = '__all__'
        read_only_fields = ['submitted_by', 'timestamp']

class DisputeSerializer(serializers.ModelSerializer):
    evidence = EvidenceSubmissionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Dispute
        fields = '__all__'
        read_only_fields = ['opened_by', 'status', 'created_at']
