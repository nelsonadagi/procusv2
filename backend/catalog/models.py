from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Product(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        ACTIVE = 'ACTIVE', 'Active'
        OUT_OF_STOCK = 'OUT_OF_STOCK', 'Out of Stock'
        DISABLED = 'DISABLED', 'Disabled'

    # Basic Information
    vendor = models.ForeignKey('vendors.Vendor', on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey('taxonomy.Category', on_delete=models.PROTECT, related_name='products', limit_choices_to={'taxonomy_type': 'MATERIAL'})
    name = models.CharField(max_length=255, help_text="Product name (e.g., 'Dangote Cement 50kg')")
    slug = models.SlugField(max_length=300, unique=False, blank=True, help_text="Auto-generated from name")  # Temporarily non-unique
    short_description = models.CharField(max_length=500, blank=True, help_text="Brief product summary for listings")
    description = models.TextField(help_text="Detailed product description")
    
    # Pricing & Inventory
    unit = models.CharField(max_length=50, help_text="Unit of measurement (e.g., 'bag', 'ton', 'piece')") 
    base_price = models.DecimalField(max_digits=12, decimal_places=2, help_text="Price per unit")
    bulk_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="Discounted price for bulk orders")
    bulk_threshold = models.IntegerField(null=True, blank=True, help_text="Minimum quantity for bulk pricing")
    stock_quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    min_order_quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    max_order_quantity = models.IntegerField(null=True, blank=True, help_text="Maximum quantity per order")
    
    # Product Specifications
    brand = models.CharField(max_length=100, blank=True, help_text="Brand or manufacturer name")
    model_number = models.CharField(max_length=100, blank=True, help_text="Model/SKU number")
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Weight per unit (kg)")
    dimensions = models.CharField(max_length=100, blank=True, help_text="Dimensions (L x W x H in cm)")
    color = models.CharField(max_length=50, blank=True)
    material_composition = models.TextField(blank=True, help_text="Material composition or ingredients")
    
    # Quality & Compliance
    quality_grade = models.CharField(max_length=50, blank=True, help_text="Quality grade (e.g., 'Grade A', 'Premium')")
    certifications = models.TextField(blank=True, help_text="Certifications (e.g., 'KEBS Certified, ISO 9001')")
    warranty_period = models.CharField(max_length=100, blank=True, help_text="Warranty period (e.g., '12 months', '2 years')")
    manufacturing_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True, help_text="For perishable materials")
    
    # Delivery & Logistics
    delivery_regions = models.JSONField(default=list, blank=True, help_text="e.g. ['NAIROBI', 'MOMBASA']")
    estimated_delivery_days = models.IntegerField(null=True, blank=True, help_text="Estimated delivery time in days")
    shipping_weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Shipping weight (kg)")
    requires_special_handling = models.BooleanField(default=False, help_text="Fragile, hazardous, or special care needed")
    handling_instructions = models.TextField(blank=True, help_text="Special handling or storage instructions")
    
    # Additional Information
    features = models.TextField(blank=True, help_text="Key features (one per line)")
    applications = models.TextField(blank=True, help_text="Common applications or use cases")
    technical_specifications = models.JSONField(default=dict, blank=True, help_text="Technical specs as key-value pairs")
    
    # SEO & Marketing
    meta_keywords = models.CharField(max_length=500, blank=True, help_text="SEO keywords (comma-separated)")
    is_featured = models.BooleanField(default=False, help_text="Show in featured products")
    is_new_arrival = models.BooleanField(default=False)
    is_on_sale = models.BooleanField(default=False)
    
    # Status & Timestamps
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
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
        return self.stock_quantity > 0
    
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
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    """Multiple images per product"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/%Y/%m/', help_text="Product image")
    alt_text = models.CharField(max_length=255, blank=True, help_text="Image description for accessibility")
    is_primary = models.BooleanField(default=False, help_text="Primary image shown in listings")
    display_order = models.IntegerField(default=0, help_text="Order in which images are displayed")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
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
