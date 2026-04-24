from django.db import models
import uuid


class TaxonomyType(models.TextChoices):
    MATERIAL = "MATERIAL", "📦 Building Materials"
    SERVICE = "SERVICE", "🔧 Professional Services"
    PROJECT = "PROJECT", "🏗️ Project Types"
    PROPERTY = "PROPERTY", "🏠 Property Types"
    FINANCE = "FINANCE", "💰 Financial Products"
    GOVERNMENT = "GOVERNMENT", "🏛️ Government Categories"
    COMPLIANCE = "COMPLIANCE", "📋 Compliance Types"


class Category(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=255, verbose_name="Category Name")
    slug = models.SlugField(max_length=255, verbose_name="URL Slug")

    taxonomy_type = models.CharField(
        max_length=32,
        choices=TaxonomyType.choices,
        verbose_name="Category Type"
    )

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.CASCADE,
        verbose_name="Parent Category"
    )

    active = models.BooleanField(default=True, verbose_name="Active")
    region_code = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name="Region Code"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created On")

    class Meta:
        unique_together = ("slug", "taxonomy_type", "region_code")
        verbose_name_plural = "Categories"
        verbose_name = "Category"

    def __str__(self):
        return f"{self.name} ({self.get_taxonomy_type_display()})"
