from rest_framework import serializers
from .models import EscrowAccount, EscrowTransaction, EscrowRelease, EscrowHold

class EscrowTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EscrowTransaction
        fields = '__all__'

class EscrowReleaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = EscrowRelease
        fields = '__all__'

class EscrowHoldSerializer(serializers.ModelSerializer):
    class Meta:
        model = EscrowHold
        fields = '__all__'

class EscrowAccountSerializer(serializers.ModelSerializer):
    transactions = EscrowTransactionSerializer(many=True, read_only=True)
    holds = EscrowHoldSerializer(many=True, read_only=True)
    
    class Meta:
        model = EscrowAccount
        fields = '__all__'
