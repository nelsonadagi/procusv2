from rest_framework import serializers
from .models import FinanceProduct, FinanceApplication

class FinanceProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceProduct
        fields = '__all__'

class FinanceApplicationSerializer(serializers.ModelSerializer):
    product_details = FinanceProductSerializer(source='product', read_only=True)
    
    class Meta:
        model = FinanceApplication
        fields = '__all__'
        read_only_fields = ['applicant', 'status', 'created_at']
