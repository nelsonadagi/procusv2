from rest_framework import serializers
from .models import UnderwritingPrediction

class UnderwritingPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnderwritingPrediction
        fields = '__all__'
        read_only_fields = ['user', 'created_at']
