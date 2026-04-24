from rest_framework import serializers
from .models import QuoteRequest, QuoteItem, QuoteResponse, QuoteResponseItem, Order, OrderItem
from catalog.serializers import ProductSerializer
from platform_settings.serializers import LocationSerializer

class QuoteItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    product = serializers.SlugRelatedField(
        queryset=QuoteItem._meta.get_field('product').remote_field.model.objects.all(),
        slug_field='uuid'
    )
    product_details = ProductSerializer(source='product', read_only=True)
    class Meta:
        model = QuoteItem
        fields = '__all__'
        read_only_fields = ['quote_request']

class QuoteResponseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuoteResponseItem
        fields = '__all__'
        read_only_fields = ['quote_response']

class QuoteResponseSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor.business_name', read_only=True)
    has_order = serializers.SerializerMethodField()
    order_id = serializers.SerializerMethodField()
    items = QuoteResponseItemSerializer(many=True, read_only=True)

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
        request = self.context.get('request')
        items_data = validated_data.pop('items')

        # Check for self-quoting if user is a vendor
        if hasattr(request.user, 'vendor_profile'):
            vendor = request.user.vendor_profile
            for item in items_data:
                # Assuming item['product'] is a Product object or ID that can be resolved
                # Ideally, we should check this before creating any objects
                # However, since we are iterating, we can raise ValidationError here
                # Or perform this check in `validate_items` method if it existed
                product = item.get('product') # This might be resolved instance or PK depending on DRF setup

                # If product is just PK, we might need to fetch it, but usually with ModelSerializer it is instance
                if product and product.vendor == vendor:
                    raise serializers.ValidationError("Vendors cannot request quotes for their own products.")

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
    delivery_location_details = LocationSerializer(source='delivery_location', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['buyer', 'total_amount', 'created_at', 'updated_at']
