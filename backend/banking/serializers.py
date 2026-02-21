from rest_framework import serializers
from .models import BankAccount, SettlementTransaction

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'
        read_only_fields = ['user', 'is_verified', 'external_id']

class SettlementTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SettlementTransaction
        fields = '__all__'
        read_only_fields = ['status', 'created_at']
