from rest_framework import serializers
from .models import Bid
from contractors.serializers import ContractorProfileSerializer

class BidSerializer(serializers.ModelSerializer):
    contractor = ContractorProfileSerializer(read_only=True)
    contract_title = serializers.CharField(source='contract.title', read_only=True)
    
    class Meta:
        model = Bid
        fields = '__all__'
        read_only_fields = ['contractor', 'status', 'created_at'] # Contract is set via URL or Body, but usually we validate it.
