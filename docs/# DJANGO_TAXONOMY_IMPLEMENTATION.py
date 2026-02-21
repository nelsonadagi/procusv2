# DJANGO_TAXONOMY_IMPLEMENTATION.md

## Django Taxonomy Implementation Scaffold

This document provides the production-ready scaffold to implement taxonomy in Django.

---

# 1. Create Taxonomy App

```bash
python manage.py startapp taxonomy
```

Add to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...,
    "taxonomy",
]
```

---

# 2. Taxonomy Model (Hierarchical Categories)

## `taxonomy/models.py`

```python
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

    def __str__(self):
        return f"{self.name} ({self.taxonomy_type})"
```

---

# 3. Admin Registration

## `taxonomy/admin.py`

```python
from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "taxonomy_type", "parent", "active")
    list_filter = ("taxonomy_type", "active")
    search_fields = ("name", "slug")
```

---

# 4. Seed Files Structure

Create folder:

```
taxonomy/seeds/
  materials.yaml
  services.yaml
  projects.yaml
  property.yaml
  finance.yaml
```

Example YAML:

```yaml
materials:
  - Cement:
      - Portland Cement
      - Rapid Set Cement
```

---

# 5. Management Command: Seed Taxonomies

## `taxonomy/management/commands/seed_taxonomies.py`

```python
import yaml
from django.core.management.base import BaseCommand
from taxonomy.models import Category, TaxonomyType
from django.utils.text import slugify


class Command(BaseCommand):
    help = "Seed taxonomy categories from YAML files"

    def handle(self, *args, **options):
        self.stdout.write("Seeding taxonomies...")

        self.seed_file("materials.yaml", TaxonomyType.MATERIAL)
        self.seed_file("services.yaml", TaxonomyType.SERVICE)
        self.seed_file("projects.yaml", TaxonomyType.PROJECT)
        self.seed_file("property.yaml", TaxonomyType.PROPERTY)
        self.seed_file("finance.yaml", TaxonomyType.FINANCE)

        self.stdout.write(self.style.SUCCESS("Taxonomy seeding complete."))

    def seed_file(self, filename, taxonomy_type):
        path = f"taxonomy/seeds/{filename}"
        with open(path) as f:
            data = yaml.safe_load(f)

        root_key = list(data.keys())[0]
        categories = data[root_key]

        for item in categories:
            for parent_name, children in item.items():
                parent_obj, _ = Category.objects.get_or_create(
                    name=parent_name,
                    slug=slugify(parent_name),
                    taxonomy_type=taxonomy_type,
                    parent=None,
                )

                for child_name in children:
                    Category.objects.get_or_create(
                        name=child_name,
                        slug=slugify(child_name),
                        taxonomy_type=taxonomy_type,
                        parent=parent_obj,
                    )
```

Run:

```bash
python manage.py seed_taxonomies
```

---

# 6. API Endpoint (Read-Only)

## `taxonomy/serializers.py`

```python
from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "taxonomy_type", "parent", "children"]

    def get_children(self, obj):
        return CategorySerializer(obj.children.all(), many=True).data
```

---

## `taxonomy/views.py`

```python
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Category
from .serializers import CategorySerializer


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.filter(active=True)
    serializer_class = CategorySerializer
```

---

## `taxonomy/urls.py`

```python
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet)

urlpatterns = router.urls
```

Include in main API:

```python
path("api/taxonomy/", include("taxonomy.urls"))
```

---

# 7. Integration Example

Products should reference categories:

```python
category = models.ForeignKey(
    "taxonomy.Category",
    on_delete=models.PROTECT,
    limit_choices_to={"taxonomy_type": "MATERIAL"}
)
```

---

# 8. Production Notes

* Taxonomies are data, not code
* Must support regional overrides
* Must be editable via admin
* Required for search, analytics, RBAC enforcement

---

**Django Taxonomy Implementation Scaffold Complete.**
