from rest_framework import serializers
from .models import Project, ProjectRequirement, InvestmentCommitment, ProjectUpdate
from platform_settings.serializers import LocationSyncMixin

class ProjectRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectRequirement
        fields = '__all__'
        read_only_fields = ['project']

class InvestmentCommitmentSerializer(serializers.ModelSerializer):
    investor = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = InvestmentCommitment
        fields = '__all__'
        read_only_fields = ['investor', 'project', 'status', 'created_at']

class ProjectUpdateSerializer(serializers.ModelSerializer):
    posted_by = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = ProjectUpdate
        fields = '__all__'
        read_only_fields = ['project', 'posted_by', 'created_at']

class ProjectSerializer(LocationSyncMixin, serializers.ModelSerializer):
    requirements = ProjectRequirementSerializer(many=True, read_only=True)
    updates = ProjectUpdateSerializer(many=True, read_only=True)
    commitments = InvestmentCommitmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['owner', 'status', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user:
            validated_data['owner'] = request.user
        project = super().create(validated_data)
        self._sync_location_obj(project, validated_data)
        return project

    def update(self, instance, validated_data):
        project = super().update(instance, validated_data)
        self._sync_location_obj(project, validated_data)
        return project
