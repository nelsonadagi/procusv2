from rest_framework import serializers
from .models import QuoteRequest, QuoteItem, QuoteResponse, Order, OrderItem
from catalog.serializers import ProductSerializer

class QuoteItemSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)
    class Meta:
        model = QuoteItem
        fields = '__all__'
        read_only_fields = ['quote_request']

class QuoteResponseSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor.business_name', read_only=True)
    has_order = serializers.SerializerMethodField()
    order_id = serializers.SerializerMethodField()

    class Meta:
        model = QuoteResponse
        fields = '__all__'
        read_only_fields = ['vendor', 'quote_request', 'confirmed_at']

    def get_has_order(self, obj):
        return Order.objects.filter(quote_response=obj).exists()

    def get_order_id(self, obj):
        order = Order.objects.filter(quote_response=obj).first()
        return order.id if order else None

class QuoteRequestSerializer(serializers.ModelSerializer):
    items = QuoteItemSerializer(many=True)
    responses = QuoteResponseSerializer(many=True, read_only=True)
    buyer_name = serializers.CharField(source='buyer.username', read_only=True)
    
    class Meta:
        model = QuoteRequest
        fields = '__all__'
        read_only_fields = ['buyer', 'status', 'requested_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        request = self.context.get('request')
        quote_request = QuoteRequest.objects.create(buyer=request.user, **validated_data)
        for item_data in items_data:
            QuoteItem.objects.create(quote_request=quote_request, **item_data)
        return quote_request

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    vendor_name = serializers.CharField(source='vendor.business_name', read_only=True)
    buyer_name = serializers.CharField(source='buyer.username', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['buyer', 'total_amount', 'created_at', 'updated_at']
