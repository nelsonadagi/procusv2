from rest_framework import serializers
from .models import FinanceProduct, FinanceApplication

class FinanceProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceProduct
        fields = '__all__'

class FinanceApplicationSerializer(serializers.ModelSerializer):
    product_details = FinanceProductSerializer(source='product', read_only=True)
    
    class Meta:
        model = FinanceApplication
        fields = '__all__'
        read_only_fields = ['applicant', 'status', 'created_at']

    def validate(self, attrs):
        target_type = attrs.get('target_type') or getattr(self.instance, 'target_type', None)
        property_obj = attrs.get('property') if 'property' in attrs else getattr(self.instance, 'property', None)
        project_obj = attrs.get('project') if 'project' in attrs else getattr(self.instance, 'project', None)

        if target_type == FinanceApplication.TargetType.PROPERTY and not property_obj:
            raise serializers.ValidationError({'property': 'Property is required for property financing.'})
        if target_type == FinanceApplication.TargetType.PROJECT and not project_obj:
            raise serializers.ValidationError({'project': 'Project is required for project financing.'})
        if target_type == FinanceApplication.TargetType.PROPERTY and project_obj:
            raise serializers.ValidationError({'project': 'Project should be empty for property financing.'})
        if target_type == FinanceApplication.TargetType.PROJECT and property_obj:
            raise serializers.ValidationError({'property': 'Property should be empty for project financing.'})

        return attrs
