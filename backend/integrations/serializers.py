from rest_framework import serializers
from .models import ERPConnector, ExternalSystemSync

class ERPConnectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ERPConnector
        fields = '__all__'

class ExternalSystemSyncSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalSystemSync
        fields = '__all__'
        read_only_fields = ['timestamp']
