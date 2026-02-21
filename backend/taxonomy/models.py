from django.db import models


class TaxonomyType(models.TextChoices):
    MATERIAL = "MATERIAL", "Material"
    SERVICE = "SERVICE", "Service"
    PROJECT = "PROJECT", "Project"
    PROPERTY = "PROPERTY", "Property"
    FINANCE = "FINANCE", "Finance"
    GOVERNMENT = "GOVERNMENT", "Government"
    COMPLIANCE = "COMPLIANCE", "Compliance"


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    taxonomy_type = models.CharField(
        max_length=32,
        choices=TaxonomyType.choices,
    )

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.CASCADE,
    )

    active = models.BooleanField(default=True)
    region_code = models.CharField(max_length=10, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("slug", "taxonomy_type", "region_code")
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name} ({self.taxonomy_type})"
