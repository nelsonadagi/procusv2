from rest_framework import serializers
from .models import Product, ProductImage
from taxonomy.serializers import CategorySerializer


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for product images"""
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'image_url', 'alt_text', 'is_primary', 'display_order', 'uploaded_at']
        read_only_fields = ['uploaded_at']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class ProductSerializer(serializers.ModelSerializer):
    """Comprehensive product serializer with all fields"""
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Product._meta.get_field('category').remote_field.model.objects.all(),
        source='category',
        write_only=True
    )
    vendor_business_name = serializers.CharField(source='vendor.business_name', read_only=True)
    vendor_id = serializers.PrimaryKeyRelatedField(source='vendor', read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    primary_image_url = serializers.SerializerMethodField()
    effective_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            # IDs and relationships
            'id', 'vendor_id', 'vendor_business_name', 'category', 'category_id', 'slug',
            
            # Basic Information
            'name', 'short_description', 'description',
            
            # Pricing & Inventory
            'unit', 'base_price', 'bulk_price', 'bulk_threshold', 'effective_price',
            'stock_quantity', 'min_order_quantity', 'max_order_quantity', 'is_in_stock',
            
            # Product Specifications
            'brand', 'model_number', 'weight', 'dimensions', 'color', 'material_composition',
            
            # Quality & Compliance
            'quality_grade', 'certifications', 'warranty_period', 
            'manufacturing_date', 'expiry_date',
            
            # Delivery & Logistics
            'delivery_regions', 'estimated_delivery_days', 'shipping_weight',
            'requires_special_handling', 'handling_instructions',
            
            # Additional Information
            'features', 'applications', 'technical_specifications',
            
            # SEO & Marketing
            'meta_keywords', 'is_featured', 'is_new_arrival', 'is_on_sale',
            
            # Status & Media
            'status', 'images', 'primary_image_url',
            
            # Timestamps
            'created_at', 'updated_at', 'is_public'
        ]
        read_only_fields = ['created_at', 'updated_at', 'slug']
    
    def get_primary_image_url(self, obj):
        primary_image = obj.primary_image
        if primary_image and primary_image.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(primary_image.image.url)
            return primary_image.image.url
        return None


class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for product listings"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    vendor_business_name = serializers.CharField(source='vendor.business_name', read_only=True)
    primary_image_url = serializers.SerializerMethodField()
    effective_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'slug', 'name', 'short_description', 'vendor_business_name',
            'category_name', 'unit', 'base_price', 'bulk_price', 'effective_price',
            'stock_quantity', 'min_order_quantity', 'is_in_stock',
            'brand', 'quality_grade', 'primary_image_url',
            'is_featured', 'is_new_arrival', 'is_on_sale',
            'status', 'created_at'
        ]
    
    def get_primary_image_url(self, obj):
        primary_image = obj.primary_image
        if primary_image and primary_image.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(primary_image.image.url)
            return primary_image.image.url
        return None


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating products (vendor use)"""
    
    class Meta:
        model = Product
        fields = [
            # Basic Information
            'name', 'short_description', 'description', 'category',
            
            # Pricing & Inventory
            'unit', 'base_price', 'bulk_price', 'bulk_threshold',
            'stock_quantity', 'min_order_quantity', 'max_order_quantity',
            
            # Product Specifications
            'brand', 'model_number', 'weight', 'dimensions', 'color', 'material_composition',
            
            # Quality & Compliance
            'quality_grade', 'certifications', 'warranty_period',
            'manufacturing_date', 'expiry_date',
            
            # Delivery & Logistics
            'delivery_regions', 'estimated_delivery_days', 'shipping_weight',
            'requires_special_handling', 'handling_instructions',
            
            # Additional Information
            'features', 'applications', 'technical_specifications',
            
            # SEO & Marketing
            'meta_keywords', 'is_featured', 'is_new_arrival', 'is_on_sale',
            
            # Status
            'status'
        ]
    
    def validate(self, data):
        # Ensure bulk price is less than base price
        if data.get('bulk_price') and data.get('base_price'):
            if data['bulk_price'] >= data['base_price']:
                raise serializers.ValidationError({
                    'bulk_price': 'Bulk price must be less than base price'
                })
        
        # Ensure bulk threshold is set if bulk price is provided
        if data.get('bulk_price') and not data.get('bulk_threshold'):
            raise serializers.ValidationError({
                'bulk_threshold': 'Bulk threshold is required when bulk price is set'
            })
        
        return data
