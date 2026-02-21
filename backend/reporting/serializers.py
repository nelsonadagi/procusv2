from rest_framework import serializers
from .models import RegulatoryReport, TaxFiling

class RegulatoryReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegulatoryReport
        fields = '__all__'
        read_only_fields = ['generated_at', 'status']

class TaxFilingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxFiling
        fields = '__all__'
