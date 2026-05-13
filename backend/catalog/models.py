from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
import uuid


class Product(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    class Status(models.TextChoices):
        DRAFT = 'DRAFT', _('📝 Draft - Not Published')
        ACTIVE = 'ACTIVE', _('✅ Active - Available for Purchase')
        OUT_OF_STOCK = 'OUT_OF_STOCK', _('📭 Temporarily Out of Stock')
        DISABLED = 'DISABLED', _('🚫 Disabled - Not Available')

    # Basic Information
    vendor = models.ForeignKey(
        'vendors.Vendor',
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Sold By"
    )
    country = models.ForeignKey(
        'platform_settings.Country',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name="Product Country"
    )
    category = models.ForeignKey(
        'taxonomy.Category',
        on_delete=models.PROTECT,
        related_name='products',
        limit_choices_to={'taxonomy_type': 'MATERIAL'},
        verbose_name="Product Category"
    )
    name = models.CharField(
        max_length=255,
        help_text="Product name as customers will see it",
        verbose_name="Product Name"
    )
    slug = models.SlugField(
        max_length=300,
        unique=False,
        blank=True,
        help_text="Auto-generated from name",
        verbose_name="URL Slug"
    )
    short_description = models.CharField(
        max_length=500,
        blank=True,
        help_text="Brief summary for product listings",
        verbose_name="Short Description"
    )
    description = models.TextField(
        help_text="Full product description with details",
        verbose_name="Detailed Description"
    )

    # Pricing & Inventory
    unit = models.CharField(
        max_length=50,
        help_text="How it's sold, e.g. 'bag', 'ton', 'piece', 'meter'",
        verbose_name="Unit of Sale"
    )
    base_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Regular price per unit",
        verbose_name="Standard Price"
    )
    currency = models.CharField(
        max_length=10,
        default='KES',
        help_text="ISO 4217 currency code for all listed prices",
        verbose_name="Currency"
    )
    bulk_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Discounted price for large orders",
        verbose_name="Bulk Order Price"
    )
    bulk_threshold = models.IntegerField(
        null=True,
        blank=True,
        help_text="Minimum quantity to qualify for bulk price",
        verbose_name="Bulk Quantity Threshold"
    )
    stock_quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Current Stock Level"
    )
    min_order_quantity = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name="Minimum Order Quantity"
    )
    max_order_quantity = models.IntegerField(
        null=True,
        blank=True,
        help_text="Maximum quantity per order (leave blank for unlimited)",
        verbose_name="Maximum Order Quantity"
    )
    reorder_level = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Reorder Threshold"
    )

    # Product Specifications
    brand = models.CharField(
        max_length=100,
        blank=True,
        help_text="Manufacturer or brand name",
        verbose_name="Brand / Manufacturer"
    )
    model_number = models.CharField(
        max_length=100,
        blank=True,
        help_text="Model or SKU number",
        verbose_name="Model / SKU Number"
    )
    weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Weight per unit in kilograms",
        verbose_name="Unit Weight (kg)"
    )
    dimensions = models.CharField(
        max_length=100,
        blank=True,
        help_text="L x W x H in centimeters",
        verbose_name="Dimensions (cm)"
    )
    color = models.CharField(max_length=50, blank=True, verbose_name="Color / Finish")
    material_composition = models.TextField(
        blank=True,
        help_text="What it's made of",
        verbose_name="Material Composition"
    )
    country_of_origin = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Country of Origin"
    )
    packaging_details = models.CharField(
        max_length=255,
        blank=True,
        help_text="Packaging format, palletization, or bundle details",
        verbose_name="Packaging Details"
    )

    # Quality & Compliance
    quality_grade = models.CharField(
        max_length=50,
        blank=True,
        help_text="e.g. 'Grade A', 'Premium', 'Standard'",
        verbose_name="Quality Grade"
    )
    certifications = models.TextField(
        blank=True,
        help_text="e.g. 'KEBS Certified, ISO 9001, CE Marked'",
        verbose_name="Certifications & Standards"
    )
    warranty_period = models.CharField(
        max_length=100,
        blank=True,
        help_text="e.g. '12 months', '2 years manufacturer warranty'",
        verbose_name="Warranty Period"
    )
    manufacturing_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date of Manufacture"
    )
    expiry_date = models.DateField(
        null=True,
        blank=True,
        help_text="For perishable or time-sensitive materials",
        verbose_name="Expiry / Best Before Date"
    )

    # Delivery & Logistics
    delivery_regions = models.JSONField(
        default=list,
        blank=True,
        help_text="e.g. ['NAIROBI', 'MOMBASA', 'KISUMU']",
        verbose_name="Delivery Locations"
    )
    estimated_delivery_days = models.IntegerField(
        null=True,
        blank=True,
        help_text="Typical delivery time",
        verbose_name="Estimated Delivery Time (days)"
    )
    shipping_weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Shipping weight if different from unit weight",
        verbose_name="Shipping Weight (kg)"
    )
    requires_special_handling = models.BooleanField(
        default=False,
        help_text="Check if fragile, hazardous, or needs special care",
        verbose_name="Requires Special Handling"
    )
    handling_instructions = models.TextField(
        blank=True,
        help_text="Special storage or handling requirements",
        verbose_name="Handling Instructions"
    )

    # Additional Information
    features = models.TextField(
        blank=True,
        help_text="Key features, one per line",
        verbose_name="Product Features"
    )
    applications = models.TextField(
        blank=True,
        help_text="Common uses and applications",
        verbose_name="Recommended Applications"
    )
    technical_specifications = models.JSONField(
        default=dict,
        blank=True,
        help_text="Technical details as key-value pairs",
        verbose_name="Technical Specifications"
    )

    # SEO & Marketing
    meta_keywords = models.CharField(
        max_length=500,
        blank=True,
        help_text="Search keywords, comma-separated",
        verbose_name="Search Keywords"
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Show in featured products section",
        verbose_name="Featured Product"
    )
    is_new_arrival = models.BooleanField(
        default=False,
        verbose_name="Mark as New Arrival"
    )
    is_on_sale = models.BooleanField(
        default=False,
        verbose_name="Currently On Sale"
    )

    # Status & Timestamps
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name="Product Status"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Added On")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['vendor', 'status']),
            models.Index(fields=['category', 'status']),
            models.Index(fields=['slug']),
        ]

    @property
    def is_public(self):
        return self.status == self.Status.ACTIVE and self.vendor.verified_status == 'APPROVED'

    @property
    def effective_price(self):
        """Returns bulk price if available, otherwise base price"""
        return self.bulk_price if self.bulk_price else self.base_price

    @property
    def is_in_stock(self):
        return self.available_quantity > 0

    @property
    def available_quantity(self):
        try:
            return max(int(self.stock_quantity or 0), 0)
        except (TypeError, ValueError):
            return 0

    @property
    def inventory_signal(self):
        if self.available_quantity <= 0:
            return 'OUT_OF_STOCK'
        if self.reorder_level and self.available_quantity <= self.reorder_level:
            return 'LOW_STOCK'
        return 'IN_STOCK'

    @property
    def primary_image(self):
        """Returns the first image marked as primary, or the first image"""
        return self.images.filter(is_primary=True).first() or self.images.first()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Auto-generate slug from name if not provided
        if not self.slug:
            from django.utils.text import slugify
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        if self.status in [self.Status.ACTIVE, self.Status.OUT_OF_STOCK]:
            self.status = self.Status.OUT_OF_STOCK if self.available_quantity <= 0 else self.Status.ACTIVE
        super().save(*args, **kwargs)

    def record_inventory_movement(self, *, movement_type, quantity_delta, quantity_before, quantity_after, actor=None, note='', reference=''):
        return ProductInventoryMovement.objects.create(
            product=self,
            movement_type=movement_type,
            quantity_delta=quantity_delta,
            quantity_before=quantity_before,
            quantity_after=quantity_after,
            actor=actor,
            note=note,
            reference=reference,
        )


class ProductCertificationRegistry(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=50, blank=True, default='', unique=True)
    issuer = models.CharField(max_length=255, blank=True, default='')
    description = models.TextField(blank=True, default='')
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ProductCertification(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        EXPIRED = 'EXPIRED', 'Expired'
        PENDING = 'PENDING', 'Pending'
        REVOKED = 'REVOKED', 'Revoked'

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='certification_entries')
    registry = models.ForeignKey(
        ProductCertificationRegistry,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='product_entries',
    )
    display_name = models.CharField(max_length=255, blank=True, default='')
    certification_number = models.CharField(max_length=100, blank=True, default='')
    issuing_body = models.CharField(max_length=255, blank=True, default='')
    issued_on = models.DateField(null=True, blank=True)
    expires_on = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    verification_url = models.URLField(blank=True, default='')
    document_url = models.URLField(blank=True, default='')

    class Meta:
        ordering = ['display_name', 'id']

    def __str__(self):
        if self.display_name:
            return self.display_name
        if self.registry:
            return self.registry.name
        return f'Certification #{self.pk}'


class ProductAttribute(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attribute_entries')
    group = models.CharField(max_length=100, blank=True, default='')
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    unit = models.CharField(max_length=50, blank=True, default='')
    is_highlight = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'name']

    def __str__(self):
        return f'{self.product.name}: {self.name}'


class ProductDocument(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    class DocumentType(models.TextChoices):
        DATASHEET = 'DATASHEET', 'Datasheet'
        SAFETY = 'SAFETY', 'Safety Sheet'
        WARRANTY = 'WARRANTY', 'Warranty'
        BROCHURE = 'BROCHURE', 'Brochure'
        INSTALLATION = 'INSTALLATION', 'Installation Guide'
        OTHER = 'OTHER', 'Other'

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DocumentType.choices, default=DocumentType.DATASHEET)
    file = models.FileField(upload_to='products/documents/%Y/%m/', null=True, blank=True)
    external_url = models.URLField(blank=True, default='')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    is_public = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title', 'id']

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    """Multiple images per product"""
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="Product"
    )
    image = models.ImageField(
        upload_to='products/%Y/%m/',
        help_text="Upload product photo",
        verbose_name="Image File"
    )
    alt_text = models.CharField(
        max_length=255,
        blank=True,
        help_text="Describe the image for accessibility",
        verbose_name="Image Description"
    )
    is_primary = models.BooleanField(
        default=False,
        help_text="Main image shown in listings",
        verbose_name="Primary Image"
    )
    display_order = models.IntegerField(
        default=0,
        help_text="Order in gallery (0 = first)",
        verbose_name="Display Order"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Uploaded On")

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
        ordering = ['display_order', 'uploaded_at']
        indexes = [
            models.Index(fields=['product', 'is_primary']),
        ]

    def __str__(self):
        return f"{self.product.name} - Image {self.display_order}"

    def save(self, *args, **kwargs):
        # If this is set as primary, unset other primary images for this product
        if self.is_primary:
            ProductImage.objects.filter(product=self.product, is_primary=True).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)


class ProductInventoryMovement(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    class MovementType(models.TextChoices):
        INITIAL = 'INITIAL', 'Initial Stock'
        MANUAL_ADJUSTMENT = 'MANUAL_ADJUSTMENT', 'Manual Adjustment'
        IMPORT = 'IMPORT', 'CSV Import'
        ORDER_COMMIT = 'ORDER_COMMIT', 'Order Commit'
        ORDER_RESTOCK = 'ORDER_RESTOCK', 'Order Restock'

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventory_movements')
    movement_type = models.CharField(max_length=32, choices=MovementType.choices)
    quantity_delta = models.IntegerField()
    quantity_before = models.IntegerField()
    quantity_after = models.IntegerField()
    actor = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='inventory_movements',
    )
    note = models.TextField(blank=True)
    reference = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at', '-id']
        indexes = [
            models.Index(fields=['product', 'created_at']),
            models.Index(fields=['movement_type', 'created_at']),
        ]

    def __str__(self):
        return f"{self.product.name} {self.movement_type} {self.quantity_delta:+d}"
