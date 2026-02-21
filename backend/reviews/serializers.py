from rest_framework import serializers
from .models import Rating

class RatingSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor.business_name', read_only=True)

    class Meta:
        model = Rating
        fields = '__all__'
        read_only_fields = ['buyer', 'vendor', 'created_at']

    def validate(self, data):
        # Ensure only one rating per order
        order = data.get('order')
        if Rating.objects.filter(order=order).exists():
            raise serializers.ValidationError("Order already has a rating.")
        # Ensure buyer is the one who placed the order
        if order.buyer != self.context['request'].user:
            raise serializers.ValidationError("Only the buyer of the order can leave a rating.")
        # Ensure order is completed
        if order.status != 'COMPLETED':
            raise serializers.ValidationError(f"Only completed orders can be rated. This order is '{order.status}'.")
        return data

from .models import ContractorReview

class ContractorReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractorReview
        fields = '__all__'
        read_only_fields = ['owner', 'created_at']
