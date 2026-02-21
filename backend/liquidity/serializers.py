from rest_framework import serializers
from .models import SecondaryTrade, StakeTransfer

class SecondaryTradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecondaryTrade
        fields = '__all__'
        read_only_fields = ['seller', 'status', 'created_at']

class StakeTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = StakeTransfer
        fields = '__all__'
