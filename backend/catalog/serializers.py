from rest_framework import serializers
from .models import (
    Product,
    ProductImage,
    ProductCertificationRegistry,
    ProductCertification,
    ProductAttribute,
    ProductDocument,
    ProductInventoryMovement,
)
from taxonomy.serializers import CategorySerializer


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for product images"""
    id = serializers.UUIDField(source='uuid', read_only=True)
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


class ProductCertificationRegistrySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='uuid', read_only=True)
    class Meta:
        model = ProductCertificationRegistry
        fields = ['id', 'name', 'code', 'issuer', 'description', 'active']


class ProductCertificationSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='uuid', read_only=True)
    registry = serializers.SlugRelatedField(
        queryset=ProductCertificationRegistry.objects.all(),
        slug_field='uuid',
        allow_null=True,
        required=False,
    )
    registry_name = serializers.CharField(source='registry.name', read_only=True)

    class Meta:
        model = ProductCertification
        fields = [
            'id', 'registry', 'registry_name', 'display_name', 'certification_number',
            'issuing_body', 'issued_on', 'expires_on', 'status',
            'verification_url', 'document_url',
        ]


class ProductAttributeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='uuid', read_only=True)
    class Meta:
        model = ProductAttribute
        fields = ['id', 'group', 'name', 'value', 'unit', 'is_highlight', 'sort_order']


class ProductDocumentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='uuid', read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductDocument
        fields = ['id', 'document_type', 'file', 'file_url', 'external_url', 'title', 'description', 'is_public', 'uploaded_at']
        read_only_fields = ['uploaded_at']

    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None


class ProductSerializer(serializers.ModelSerializer):
    """Comprehensive product serializer with all fields"""
    id = serializers.UUIDField(source='uuid', read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.SlugRelatedField(
        queryset=Product._meta.get_field('category').remote_field.model.objects.all(),
        slug_field='uuid',
        source='category',
        write_only=True
    )
    vendor_business_name = serializers.CharField(source='vendor.business_name', read_only=True)
    vendor_id = serializers.UUIDField(source='vendor.uuid', read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    certification_entries = ProductCertificationSerializer(many=True, read_only=True)
    attribute_entries = ProductAttributeSerializer(many=True, read_only=True)
    documents = ProductDocumentSerializer(many=True, read_only=True)
    primary_image_url = serializers.SerializerMethodField()
    effective_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)
    available_quantity = serializers.IntegerField(read_only=True)
    inventory_signal = serializers.CharField(read_only=True)
    vendor_location = serializers.CharField(source='vendor.location_text', read_only=True)
    vendor_country_name = serializers.CharField(source='vendor.country.name', read_only=True)
    vendor_formatted_address = serializers.CharField(source='vendor.formatted_address', read_only=True)

    class Meta:
        model = Product
        fields = [
            # IDs and relationships
            'id', 'vendor_id', 'vendor_business_name', 'category', 'category_id', 'slug',

            # Basic Information
            'name', 'short_description', 'description',

            # Pricing & Inventory
            'unit', 'base_price', 'bulk_price', 'bulk_threshold', 'effective_price',
            'stock_quantity', 'available_quantity', 'min_order_quantity', 'max_order_quantity', 'is_in_stock',

            # Product Specifications
            'brand', 'model_number', 'weight', 'dimensions', 'color', 'material_composition',
            'country_of_origin', 'packaging_details',

            # Quality & Compliance
            'quality_grade', 'certifications', 'warranty_period',
            'manufacturing_date', 'expiry_date',

            # Delivery & Logistics
            'delivery_regions', 'estimated_delivery_days', 'shipping_weight',
            'requires_special_handling', 'handling_instructions',

            # Additional Information
            'features', 'applications', 'technical_specifications',
            'attribute_entries', 'certification_entries', 'documents',

            # SEO & Marketing
            'meta_keywords', 'is_featured', 'is_new_arrival', 'is_on_sale',

            # Status & Media
            'status', 'images', 'primary_image_url', 'inventory_signal',
            'vendor_location', 'vendor_country_name', 'vendor_formatted_address',

            # Timestamps
            'created_at', 'updated_at', 'is_public', 'reorder_level'
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
    id = serializers.UUIDField(source='uuid', read_only=True)
    category_id = serializers.UUIDField(source='category.uuid', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    vendor_business_name = serializers.CharField(source='vendor.business_name', read_only=True)
    vendor_id = serializers.UUIDField(source='vendor.uuid', read_only=True)
    primary_image_url = serializers.SerializerMethodField()
    effective_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    available_quantity = serializers.IntegerField(read_only=True)
    vendor_location = serializers.CharField(source='vendor.location_text', read_only=True)
    vendor_country_name = serializers.CharField(source='vendor.country.name', read_only=True)
    inventory_signal = serializers.CharField(read_only=True)
    certification_highlights = serializers.SerializerMethodField()
    attribute_highlights = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'slug', 'name', 'short_description', 'vendor_id', 'vendor_business_name',
            'vendor_location', 'vendor_country_name',
            'category_id', 'category_name', 'unit', 'base_price', 'bulk_price', 'effective_price',
            'stock_quantity', 'available_quantity', 'min_order_quantity', 'is_in_stock',
            'brand', 'quality_grade', 'primary_image_url', 'inventory_signal',
            'country_of_origin', 'packaging_details',
            'certification_highlights', 'attribute_highlights',
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

    def get_certification_highlights(self, obj):
        entries = obj.certification_entries.all()[:3]
        return [entry.display_name or entry.registry_name or entry.registry.name for entry in entries if (entry.display_name or entry.registry)]

    def get_attribute_highlights(self, obj):
        entries = obj.attribute_entries.filter(is_highlight=True)[:4]
        return [
            {
                'name': entry.name,
                'value': entry.value,
                'unit': entry.unit,
            }
            for entry in entries
        ]


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating products (vendor use)"""
    id = serializers.UUIDField(source='uuid', read_only=True)
    category = serializers.SlugRelatedField(
        queryset=Product._meta.get_field('category').remote_field.model.objects.all(),
        slug_field='uuid'
    )
    certification_entries = ProductCertificationSerializer(many=True, required=False)
    attribute_entries = ProductAttributeSerializer(many=True, required=False)
    documents = ProductDocumentSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = [
            'id',
            # Basic Information
            'name', 'short_description', 'description', 'category',

            # Pricing & Inventory
            'unit', 'base_price', 'bulk_price', 'bulk_threshold',
            'stock_quantity', 'min_order_quantity', 'max_order_quantity',

            # Product Specifications
            'brand', 'model_number', 'weight', 'dimensions', 'color', 'material_composition',
            'country_of_origin', 'packaging_details',

            # Quality & Compliance
            'quality_grade', 'certifications', 'warranty_period',
            'manufacturing_date', 'expiry_date',

            # Delivery & Logistics
            'delivery_regions', 'estimated_delivery_days', 'shipping_weight',
            'requires_special_handling', 'handling_instructions',

            # Additional Information
            'features', 'applications', 'technical_specifications',
            'certification_entries', 'attribute_entries', 'documents',

            # SEO & Marketing
            'meta_keywords', 'is_featured', 'is_new_arrival', 'is_on_sale',

            # Status
            'status', 'reorder_level'
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

    def create(self, validated_data):
        certification_entries = validated_data.pop('certification_entries', [])
        attribute_entries = validated_data.pop('attribute_entries', [])
        documents = validated_data.pop('documents', [])
        product = super().create(validated_data)
        self._save_nested(product, certification_entries, attribute_entries, documents)
        return product

    def update(self, instance, validated_data):
        certification_entries = validated_data.pop('certification_entries', None)
        attribute_entries = validated_data.pop('attribute_entries', None)
        documents = validated_data.pop('documents', None)
        product = super().update(instance, validated_data)
        self._save_nested(product, certification_entries, attribute_entries, documents)
        return product

    def _save_nested(self, product, certification_entries, attribute_entries, documents):
        if certification_entries is not None:
            product.certification_entries.all().delete()
            ProductCertification.objects.bulk_create([
                ProductCertification(product=product, **entry)
                for entry in certification_entries
                if entry.get('display_name') or entry.get('registry')
            ])
        if attribute_entries is not None:
            product.attribute_entries.all().delete()
            ProductAttribute.objects.bulk_create([
                ProductAttribute(product=product, **entry)
                for entry in attribute_entries
                if entry.get('name') and entry.get('value')
            ])
        if documents is not None:
            product.documents.all().delete()
            ProductDocument.objects.bulk_create([
            ProductDocument(product=product, **entry)
                for entry in documents
                if entry.get('title') and (entry.get('external_url') or entry.get('file'))
            ])


class ProductInventoryMovementSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='uuid', read_only=True)
    actor_name = serializers.CharField(source='actor.username', read_only=True)

    class Meta:
        model = ProductInventoryMovement
        fields = [
            'id',
            'movement_type',
            'quantity_delta',
            'quantity_before',
            'quantity_after',
            'actor_name',
            'note',
            'reference',
            'created_at',
        ]


class ProductInventoryAdjustmentSerializer(serializers.Serializer):
    quantity_delta = serializers.IntegerField()
    note = serializers.CharField(required=False, allow_blank=True)
    reference = serializers.CharField(required=False, allow_blank=True)

    def validate_quantity_delta(self, value):
        if value == 0:
            raise serializers.ValidationError('Quantity delta cannot be zero.')
        return value
