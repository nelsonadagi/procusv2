from rest_framework import serializers
from .models import Contract
from contractors.serializers import ContractorProfileSerializer

class ContractSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    
    class Meta:
        model = Contract
        fields = '__all__'
        read_only_fields = ['owner', 'status', 'created_at']
