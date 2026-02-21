from rest_framework import serializers
from .models import ReliabilityScore

class ReliabilityScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReliabilityScore
        fields = '__all__'
