from rest_framework import serializers
from contracts.serializers import ContractSerializer
from .models import Project, ProjectRequirement, InvestmentCommitment, ProjectUpdate, ProjectContractLink
from platform_settings.serializers import LocationSyncMixin
from platform_settings.utils import resolve_request_country_code
from rbac.permissions import user_has_role


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


class ProjectContractLinkSerializer(serializers.ModelSerializer):
    contract = ContractSerializer(read_only=True)

    class Meta:
        model = ProjectContractLink
        fields = ['id', 'contract']
        read_only_fields = fields


class ProjectSerializer(LocationSyncMixin, serializers.ModelSerializer):
    requirements = ProjectRequirementSerializer(many=True, read_only=True)
    updates = ProjectUpdateSerializer(many=True, read_only=True)
    commitments = InvestmentCommitmentSerializer(many=True, read_only=True)
    linked_contracts = ProjectContractLinkSerializer(many=True, read_only=True)
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    category_label = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['owner', 'created_at']

    def validate_status(self, value):
        instance = getattr(self, 'instance', None)
        request = self.context.get('request')
        if instance and request:
            # Admins can bypass transition rules
            if request.user.is_superuser or user_has_role(request.user, 'ADMIN'):
                return value
            
            valid_transitions = {
                'LISTED': ['LISTED', 'FUNDING_OPEN'],
                'FUNDING_OPEN': ['FUNDING_OPEN', 'EXECUTION_STARTED'],
                'EXECUTION_STARTED': ['EXECUTION_STARTED', 'COMPLETED'],
                'COMPLETED': ['COMPLETED'],
            }
            current = instance.status
            allowed = valid_transitions.get(current, [])
            if value not in allowed:
                raise serializers.ValidationError(
                    f"Cannot transition from {current} to {value}. Allowed: {', '.join(allowed)}"
                )
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user:
            validated_data['owner'] = request.user
        if not validated_data.get('country'):
            from platform_settings.models import Country
            country_code = resolve_request_country_code(request)
            active_country = Country.objects.filter(iso_code__iexact=country_code, is_active=True).first()
            if active_country is None:
                active_country = Country.objects.filter(is_default=True, is_active=True).first()
            if active_country:
                validated_data['country'] = active_country
        project = super().create(validated_data)
        self._sync_location_obj(project, validated_data)
        return project

    def update(self, instance, validated_data):
        project = super().update(instance, validated_data)
        self._sync_location_obj(project, validated_data)
        return project
