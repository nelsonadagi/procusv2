from rest_framework import serializers
from .models import PublicTender

class PublicTenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicTender
        fields = '__all__'
        read_only_fields = ['status', 'created_at']
